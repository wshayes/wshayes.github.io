#!/usr/bin/env python3
"""Scrape Medium tags from canonical URLs using Playwright."""

import asyncio
import json
import time
from pathlib import Path

from playwright.async_api import async_playwright
from rich.console import Console

console = Console()

MANIFEST_PATH = Path("scripts/medium_manifest.json")
TAGS_PATH = Path("scripts/medium_tags.json")


async def scrape_tags(url: str, page) -> list[str]:
    """Scrape tags from a Medium article page."""
    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(2000)  # Let page load

        # Medium tags are in links containing /tag/
        tag_elements = await page.query_selector_all('a[href*="/tag/"]')
        tags = set()
        for el in tag_elements:
            href = await el.get_attribute("href")
            if href and "/tag/" in href:
                # Extract tag name from URL
                tag = href.split("/tag/")[-1].split("?")[0].split("/")[0]
                if tag and len(tag) > 1:
                    # Convert kebab-case to Title Case
                    tag = tag.replace("-", " ").title()
                    tags.add(tag)
        return sorted(tags)
    except Exception as e:
        console.print(f"  [yellow]Warning: Could not scrape {url}: {e}[/yellow]")
        return []


async def main():
    manifest = json.loads(MANIFEST_PATH.read_text())
    articles = [m for m in manifest if m["classification"] == "article" and not m["is_draft"]]

    # Only scrape published articles with canonical URLs
    articles_with_urls = [a for a in articles if a.get("canonical_url")]
    console.print(f"[bold]Scraping tags for {len(articles_with_urls)} Medium articles...[/bold]\n")

    tags_data = {}

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        for i, article in enumerate(articles_with_urls):
            url = article["canonical_url"]
            console.print(f"  [{i+1}/{len(articles_with_urls)}] {article['title'][:50]}...")
            tags = await scrape_tags(url, page)
            tags_data[article["filename"]] = tags
            if tags:
                console.print(f"    Tags: {', '.join(tags)}")
            else:
                console.print(f"    [dim]No tags found[/dim]")

            # Rate limit
            if i < len(articles_with_urls) - 1:
                await asyncio.sleep(2)

        await browser.close()

    TAGS_PATH.write_text(json.dumps(tags_data, indent=2))
    console.print(f"\n[bold green]Tags saved to {TAGS_PATH}[/bold green]")


if __name__ == "__main__":
    asyncio.run(main())
