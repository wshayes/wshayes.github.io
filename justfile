# Hugo site management and migration commands

# Run Blogger migration
migrate-blogger *ARGS:
    uv run python scripts/migrate_blogger.py {{ARGS}}

# Generate Medium manifest for review
medium-manifest:
    uv run python scripts/medium_manifest.py

# Scrape Medium tags via Playwright
medium-scrape:
    uv run python scripts/medium_scrape.py

# Run Medium migration
migrate-medium *ARGS:
    uv run python scripts/migrate_medium.py {{ARGS}}

# Start Hugo dev server
serve:
    hugo server -D --navigateToChanged

# Build site
build:
    hugo --minify
