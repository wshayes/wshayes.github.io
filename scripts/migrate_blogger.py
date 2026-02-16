#!/usr/bin/env python3
"""Migrate Blogger posts from feed.atom to Hugo page bundles."""

import argparse
import html
import re
import xml.etree.ElementTree as ET
from pathlib import Path

import httpx
from markdownify import markdownify as md
from rich.console import Console

console = Console()

FEED_PATH = Path("add_content/Blogger/Blogs/Through the Haze/feed.atom")
CONTENT_DIR = Path("content/posts")

NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "blogger": "http://schemas.google.com/blogger/2018",
}


def slug_from_filename(filename: str) -> str:
    """Extract slug from blogger filename like /2016/03/aurelia-delegate-vs-trigger.html."""
    if not filename:
        return ""
    # Get just the last segment without .html
    name = filename.rstrip("/").split("/")[-1]
    return name.removesuffix(".html")


def slug_from_title(title: str) -> str:
    """Generate slug from title as fallback."""
    slug = title.lower().strip()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"[\s]+", "-", slug)
    slug = re.sub(r"-+", "-", slug)
    return slug.strip("-")


def convert_gist_embeds(html_content: str) -> str:
    """Convert gist script tags to Hugo shortcodes before markdownify."""
    # Match <script src="https://gist.github.com/USER/HASH.js"></script>
    pattern = r'<script\s+src="https://gist\.github\.com/([^/]+)/([^"\.]+)\.js">\s*</script>'

    def replace_gist(match):
        user = match.group(1)
        gist_hash = match.group(2)
        return f'{{{{% gist {user} {gist_hash} %}}}}'

    return re.sub(pattern, replace_gist, html_content)


def strip_inline_styles(html_content: str) -> str:
    """Remove inline style attributes."""
    return re.sub(r'\s+style="[^"]*"', "", html_content)


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
            filename = f"image{ext}"
        dest = dest_dir / filename
        dest.write_bytes(resp.content)
        return filename
    except Exception as e:
        console.print(f"  [yellow]Warning: Could not download {url}: {e}[/yellow]")
        return None


def process_images(html_content: str, dest_dir: Path) -> str:
    """Download embedded images and update references."""
    img_pattern = r'<img[^>]+src="([^"]+)"[^>]*>'
    images_found = set()

    def replace_img(match):
        url = match.group(1)
        if url in images_found:
            return match.group(0)
        images_found.add(url)

        if url.startswith("http"):
            filename = download_image(url, dest_dir)
            if filename:
                return f'<img src="{filename}">'
        return match.group(0)

    return re.sub(img_pattern, replace_img, html_content)


def html_to_markdown(html_content: str) -> str:
    """Convert HTML to Markdown with cleanup."""
    # Convert gist embeds first (preserve shortcodes)
    content = convert_gist_embeds(html_content)
    content = strip_inline_styles(content)

    # Extract gist shortcodes before markdownify
    gist_placeholder = {}
    gist_pattern = r'\{\{%\s*gist\s+\S+\s+\S+\s*%\}\}'
    for i, match in enumerate(re.finditer(gist_pattern, content)):
        placeholder = f"GISTPLACEHOLDER{i}ENDGIST"
        gist_placeholder[placeholder] = match.group(0)
        content = content.replace(match.group(0), placeholder, 1)

    # Convert to markdown
    markdown = md(content, heading_style="ATX", bullets="-", strip=["style"])

    # Restore gist shortcodes
    for placeholder, shortcode in gist_placeholder.items():
        markdown = markdown.replace(placeholder, f"\n\n{shortcode}\n\n")

    # Clean up excessive blank lines
    markdown = re.sub(r"\n{3,}", "\n\n", markdown)
    return markdown.strip()


def parse_feed(include_drafts: bool = False) -> list[dict]:
    """Parse feed.atom and return list of post data."""
    tree = ET.parse(FEED_PATH)
    root = tree.getroot()

    posts = []
    for entry in root.findall("atom:entry", NS):
        btype = entry.find("blogger:type", NS)
        bstatus = entry.find("blogger:status", NS)

        if btype is None or btype.text != "POST":
            continue

        status = bstatus.text if bstatus is not None else ""
        is_draft = status != "LIVE"

        if is_draft and not include_drafts:
            continue

        title_el = entry.find("atom:title", NS)
        title = title_el.text if title_el is not None and title_el.text else "Untitled"
        title = html.unescape(title)

        published = entry.find("atom:published", NS)
        pub_date = published.text if published is not None and published.text else ""

        content_el = entry.find("atom:content", NS)
        content_html = html.unescape(content_el.text) if content_el is not None and content_el.text else ""

        categories = []
        for cat in entry.findall("atom:category", NS):
            term = cat.get("term")
            if term:
                categories.append(term)

        filename_el = entry.find("blogger:filename", NS)
        filename = filename_el.text if filename_el is not None and filename_el.text else ""

        slug = slug_from_filename(filename) or slug_from_title(title)

        posts.append({
            "title": title,
            "date": pub_date,
            "slug": slug,
            "content_html": content_html,
            "tags": categories,
            "draft": is_draft,
        })

    return posts


def create_page_bundle(post: dict) -> None:
    """Create a Hugo page bundle for a post."""
    bundle_dir = CONTENT_DIR / post["slug"]
    bundle_dir.mkdir(parents=True, exist_ok=True)

    # Process images (download to bundle dir)
    processed_html = process_images(post["content_html"], bundle_dir)

    # Convert to markdown
    markdown = html_to_markdown(processed_html)

    # Build front matter
    fm_lines = ["---"]
    # Escape title for YAML
    safe_title = post["title"].replace('"', '\\"')
    fm_lines.append(f'title: "{safe_title}"')
    if post["date"]:
        fm_lines.append(f'date: {post["date"]}')
    if post["draft"]:
        fm_lines.append("draft: true")
    if post["tags"]:
        tags_str = ", ".join(f'"{t}"' for t in post["tags"])
        fm_lines.append(f"tags: [{tags_str}]")
    fm_lines.append('categories: ["Blogger Archive"]')
    fm_lines.append('series: ["Through the Haze"]')
    fm_lines.append("---")

    front_matter = "\n".join(fm_lines)
    index_md = bundle_dir / "index.md"
    index_md.write_text(f"{front_matter}\n\n{markdown}\n")


def main():
    parser = argparse.ArgumentParser(description="Migrate Blogger posts to Hugo")
    parser.add_argument("--include-drafts", action="store_true", help="Include draft posts")
    args = parser.parse_args()

    posts = parse_feed(include_drafts=args.include_drafts)
    console.print(f"[bold]Found {len(posts)} posts to migrate[/bold]")

    for post in posts:
        status = " [dim](draft)[/dim]" if post["draft"] else ""
        console.print(f"  Migrating: {post['title']}{status}")
        create_page_bundle(post)

    console.print(f"\n[bold green]Done! Created {len(posts)} page bundles in {CONTENT_DIR}[/bold green]")


if __name__ == "__main__":
    main()
