#!/usr/bin/env python3
"""Fix problematic image filenames in content/posts."""

import re
from pathlib import Path


def detect_image_type(filepath):
    """Detect image type from file header bytes."""
    with open(filepath, "rb") as f:
        header = f.read(16)
    if header[:3] == b"\xff\xd8\xff":
        return "jpg"
    elif header[:8] == b"\x89PNG\r\n\x1a\n":
        return "png"
    elif header[:4] == b"GIF8":
        return "gif"
    elif header[:4] == b"RIFF" and header[8:12] == b"WEBP":
        return "webp"
    return "jpg"


def sanitize_filename(name):
    """Create a safe filename."""
    safe = re.sub(r'[*?\"<>|]', "", name)
    safe = re.sub(r"[^a-zA-Z0-9._-]", "_", safe)
    safe = safe.lstrip("._")
    return safe


def main():
    content_dir = Path("content/posts")
    renames = []

    for post_dir in sorted(content_dir.iterdir()):
        if not post_dir.is_dir():
            continue
        for f in post_dir.iterdir():
            if f.name == "index.md":
                continue

            old_name = f.name
            new_name = sanitize_filename(old_name)

            # Fix missing/bad extension
            suffix = Path(new_name).suffix
            if not suffix or suffix == ".":
                ext = detect_image_type(f)
                new_name = new_name.rstrip(".") + "." + ext

            if old_name != new_name:
                new_path = f.parent / new_name
                f.rename(new_path)
                renames.append((post_dir.name, old_name, new_name))

                # Update index.md references
                index_md = post_dir / "index.md"
                content = index_md.read_text()
                content = content.replace(old_name, new_name)
                index_md.write_text(content)

    print(f"Renamed {len(renames)} files:")
    for d, old, new in renames:
        print(f"  {d}: {old} -> {new}")


if __name__ == "__main__":
    main()
