#!/usr/bin/env python3
"""Generate a manifest of Medium export files, classifying as article vs comment."""

import json
from pathlib import Path

from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table

console = Console()

MEDIUM_EXPORT_DIR = Path("/tmp/medium-export/posts")
MANIFEST_PATH = Path("scripts/medium_manifest.json")

MIN_ARTICLE_SIZE = 4096  # 4KB threshold


def classify_post(filepath: Path) -> dict:
    """Classify a Medium export HTML file."""
    soup = BeautifulSoup(filepath.read_text(encoding="utf-8"), "html.parser")
    size = filepath.stat().st_size

    title_el = soup.find("h1", class_="p-name")
    title = title_el.text.strip() if title_el else filepath.stem

    time_el = soup.find("time", class_="dt-published")
    date = time_el["datetime"] if time_el and time_el.has_attr("datetime") else ""

    canonical_el = soup.find("a", class_="p-canonical")
    canonical_url = canonical_el["href"] if canonical_el and canonical_el.has_attr("href") else ""

    summary_el = soup.find("p", class_="p-summary")
    summary = summary_el.text.strip() if summary_el else ""

    body = soup.find("section", {"data-field": "body"})
    headings = body.find_all(["h2", "h3", "h4"]) if body else []
    paragraphs = body.find_all("p") if body else []

    is_draft = filepath.name.startswith("draft_")

    # Classification: article if large enough AND has structural elements
    has_structure = len(headings) >= 1 or len(paragraphs) >= 4
    is_article = size >= MIN_ARTICLE_SIZE and has_structure

    # Override: titles that start with a sentence fragment are likely comments
    comment_indicators = [
        title.startswith("I ") and "'" not in title[:30],
        title.startswith("Thanks"),
        title.startswith("Yes"),
        title.startswith("No "),
        title.startswith("Ah,"),
        title.startswith("Wow"),
        title.startswith("So "),
        title.startswith("Also"),
        title.startswith("Fully agree"),
        title.startswith("Incredibly"),
        title.startswith("Definitely"),
        title.startswith("Regarding"),
        title.startswith("Unless"),
        title.startswith("Around which"),
        title.startswith("Look at"),
        title.startswith("Conclusion for"),
        title.startswith("Most of the"),
        title.startswith("Overall"),
    ]
    if any(comment_indicators) and len(headings) == 0:
        is_article = False

    return {
        "filename": filepath.name,
        "title": title,
        "date": date,
        "canonical_url": canonical_url,
        "summary": summary[:200] if summary else "",
        "size": size,
        "headings": len(headings),
        "paragraphs": len(paragraphs),
        "is_draft": is_draft,
        "classification": "article" if is_article else "comment",
    }


def main():
    files = sorted(MEDIUM_EXPORT_DIR.glob("*.html"))
    console.print(f"[bold]Analyzing {len(files)} Medium export files...[/bold]\n")

    manifest = []
    for f in files:
        entry = classify_post(f)
        manifest.append(entry)

    # Summary
    articles = [m for m in manifest if m["classification"] == "article"]
    comments = [m for m in manifest if m["classification"] == "comment"]
    published_articles = [a for a in articles if not a["is_draft"]]
    draft_articles = [a for a in articles if a["is_draft"]]

    console.print(f"[bold green]Articles:[/bold green] {len(published_articles)} published, {len(draft_articles)} drafts")
    console.print(f"[bold yellow]Comments/Responses:[/bold yellow] {len(comments)} (will be skipped)\n")

    # Show articles
    table = Table(title="Articles to Migrate")
    table.add_column("Date", style="cyan", width=12)
    table.add_column("Title", style="white", max_width=60)
    table.add_column("Size", style="green", width=8)
    table.add_column("Draft", style="yellow", width=6)

    for a in sorted(articles, key=lambda x: x["date"]):
        table.add_row(
            a["date"][:10],
            a["title"][:60],
            f"{a['size']//1024}KB",
            "Yes" if a["is_draft"] else "",
        )
    console.print(table)

    # Show comments
    console.print(f"\n[dim]Skipping {len(comments)} comments/responses[/dim]")

    # Save manifest
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2))
    console.print(f"\n[bold]Manifest saved to {MANIFEST_PATH}[/bold]")


if __name__ == "__main__":
    main()
