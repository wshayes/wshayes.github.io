#!/usr/bin/env python3
"""Migrate Medium articles to Hugo page bundles."""

import argparse
import json
import re
from pathlib import Path

import httpx
from bs4 import BeautifulSoup
from markdownify import MarkdownConverter
from rich.console import Console

console = Console()

MEDIUM_EXPORT_DIR = Path("/tmp/medium-export/posts")
CONTENT_DIR = Path("content/posts")
MANIFEST_PATH = Path("scripts/medium_manifest.json")
TAGS_PATH = Path("scripts/medium_tags.json")

MIN_DRAFT_SIZE = 4096  # Only include drafts >= 4KB


class MediumConverter(MarkdownConverter):
    """Custom markdownify converter for Medium HTML."""

    def convert_pre(self, el, text, **kwargs):
        """Handle Medium code blocks."""
        code = el.get_text()
        # Try to detect language from class
        classes = el.get("class", [])
        lang = ""
        for c in classes:
            if c.startswith("lang-"):
                lang = c[5:]
                break
        return f"\n\n```{lang}\n{code}\n```\n\n"

    def convert_figure(self, el, text, **kwargs):
        """Handle figures with captions."""
        img = el.find("img")
        figcaption = el.find("figcaption")

        if img:
            src = img.get("src", "")
            alt = img.get("alt", "")
            caption = figcaption.get_text().strip() if figcaption else alt
            if caption:
                return f"\n\n![{caption}]({src})\n*{caption}*\n\n"
            return f"\n\n![{alt}]({src})\n\n"
        return text


def slug_from_filename(filename: str) -> str:
    """Generate slug from Medium filename.

    Input: 2018-01-30_My-love-affair-with-JSON-edaca39e8320.html
    Output: my-love-affair-with-json

    Or for drafts:
    Input: draft_Docker-Tips-c662466da582.html
    Output: docker-tips
    """
    name = filename.removesuffix(".html")

    # Remove draft_ prefix
    if name.startswith("draft_"):
        name = name[6:]

    # Remove date prefix (YYYY-MM-DD_)
    name = re.sub(r"^\d{4}-\d{2}-\d{2}_", "", name)

    # Remove Medium hash suffix (last segment after final -)
    # Medium hashes are typically 10-12 hex chars
    name = re.sub(r"-[a-f0-9]{8,14}$", "", name)

    # Convert to lowercase slug
    slug = name.lower()
    # Replace multiple dashes
    slug = re.sub(r"-+", "-", slug)
    slug = slug.strip("-")

    return slug


def download_image(url: str, dest_dir: Path) -> str | None:
    """Download an image and return the local filename."""
    try:
        resp = httpx.get(url, follow_redirects=True, timeout=30)
        resp.raise_for_status()
        # Get filename from URL
        filename = url.split("/")[-1].split("?")[0]
        if not filename or "." not in filename:
            content_type = resp.headers.get("content-type", "")
            ext = ".jpg"
            if "png" in content_type:
                ext = ".png"
            elif "gif" in content_type:
                ext = ".gif"
            elif "webp" in content_type:
                ext = ".webp"
            filename = f"image{ext}"

        # Ensure unique filename
        dest = dest_dir / filename
        counter = 1
        while dest.exists():
            stem = Path(filename).stem
            suffix = Path(filename).suffix
            dest = dest_dir / f"{stem}_{counter}{suffix}"
            counter += 1

        dest.write_bytes(resp.content)
        return dest.name
    except Exception as e:
        console.print(f"  [yellow]Warning: Could not download {url}: {e}[/yellow]")
        return None


def process_medium_html(filepath: Path, dest_dir: Path) -> str:
    """Parse Medium HTML and convert to Markdown with local images."""
    soup = BeautifulSoup(filepath.read_text(encoding="utf-8"), "html.parser")
    body = soup.find("section", {"data-field": "body"})

    if not body:
        return ""

    # Remove the title h3/h4 that Medium puts at top (it's in front matter)
    first_heading = body.find(["h1", "h2", "h3", "h4"])
    if first_heading:
        # Check if it's the title (usually the first element)
        title_el = soup.find("h1", class_="p-name")
        if title_el and first_heading.text.strip() == title_el.text.strip():
            first_heading.decompose()

    # Remove Medium-specific subtitle if it duplicates summary
    subtitle = body.find("h4", class_="graf--subtitle")
    if subtitle:
        # Keep it, will be part of content
        pass

    # Download images
    for img in body.find_all("img"):
        src = img.get("src", "")
        if src and ("cdn-images-1.medium.com" in src or "miro.medium.com" in src):
            local_name = download_image(src, dest_dir)
            if local_name:
                img["src"] = local_name

    # Strip Medium CSS classes to avoid markdownify confusion
    for tag in body.find_all(True):
        if tag.get("class"):
            del tag["class"]
        if tag.get("id"):
            del tag["id"]
        if tag.get("data-href"):
            del tag["data-href"]

    # Convert to markdown
    converter = MediumConverter(heading_style="ATX", bullets="-")
    html_str = str(body)
    markdown = converter.convert(html_str)

    # Clean up excessive blank lines
    markdown = re.sub(r"\n{3,}", "\n\n", markdown)
    return markdown.strip()


def create_page_bundle(entry: dict, tags: list[str]) -> None:
    """Create a Hugo page bundle for a Medium article."""
    filepath = MEDIUM_EXPORT_DIR / entry["filename"]
    slug = slug_from_filename(entry["filename"])

    bundle_dir = CONTENT_DIR / slug
    bundle_dir.mkdir(parents=True, exist_ok=True)

    # Convert content
    markdown = process_medium_html(filepath, bundle_dir)

    # Build front matter
    fm_lines = ["---"]
    safe_title = entry["title"].replace('"', '\\"')
    fm_lines.append(f'title: "{safe_title}"')
    if entry.get("date"):
        fm_lines.append(f'date: {entry["date"]}')
    if entry.get("is_draft"):
        fm_lines.append("draft: true")
    if tags:
        tags_str = ", ".join(f'"{t}"' for t in tags)
        fm_lines.append(f"tags: [{tags_str}]")
    fm_lines.append('categories: ["Medium Archive"]')
    if entry.get("summary"):
        safe_desc = entry["summary"][:200].replace('"', '\\"')
        fm_lines.append(f'description: "{safe_desc}"')
    fm_lines.append("---")

    front_matter = "\n".join(fm_lines)
    index_md = bundle_dir / "index.md"
    index_md.write_text(f"{front_matter}\n\n{markdown}\n")


def main():
    parser = argparse.ArgumentParser(description="Migrate Medium articles to Hugo")
    parser.add_argument("--include-drafts", action="store_true", help="Include substantial drafts")
    args = parser.parse_args()

    if not MANIFEST_PATH.exists():
        console.print("[red]Error: Run medium_manifest.py first[/red]")
        return

    manifest = json.loads(MANIFEST_PATH.read_text())

    # Load tags if available
    tags_data = {}
    if TAGS_PATH.exists():
        tags_data = json.loads(TAGS_PATH.read_text())

    # Filter to articles only
    articles = [m for m in manifest if m["classification"] == "article" and not m["is_draft"]]

    if args.include_drafts:
        draft_articles = [
            m for m in manifest
            if m["classification"] == "article" and m["is_draft"] and m["size"] >= MIN_DRAFT_SIZE
        ]
        articles.extend(draft_articles)

    console.print(f"[bold]Migrating {len(articles)} Medium articles...[/bold]")

    for article in articles:
        tags = tags_data.get(article["filename"], [])
        status = " [dim](draft)[/dim]" if article.get("is_draft") else ""
        console.print(f"  Migrating: {article['title'][:60]}{status}")
        create_page_bundle(article, tags)

    console.print(f"\n[bold green]Done! Migrated {len(articles)} articles to {CONTENT_DIR}[/bold green]")


if __name__ == "__main__":
    main()
