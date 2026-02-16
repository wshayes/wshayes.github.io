# Blowfish Theme Guide

Quick reference for Blowfish features available on this site. Full docs: https://blowfish.page/docs/

## Currently Enabled

These features are already configured in `config/_default/params.toml`:

- **Search** (`enableSearch = true`) — built-in site search at `/search/`
- **Code copy buttons** (`enableCodeCopy = true`) — one-click copy on code blocks
- **Table of contents** on articles (`showTableOfContents = true`)
- **Reading time** on articles
- **Sharing links** — LinkedIn, Twitter, Reddit, Email
- **Tag card view** — tags page displays as a card grid with post counts
- **Term group-by-year** — individual tag pages group articles by year
- **RSS + JSON** output — feed at `/posts/index.xml`
- **Series support** — Blogger posts use the "Through the Haze" series

## Features Worth Enabling

### Zen Mode (distraction-free reading)

Add to `[article]` in `params.toml`:
```toml
showZenMode = true
```
Adds a button that hides navigation and sidebars for focused reading.

### Related Content

Add to `[article]` in `params.toml`:
```toml
showRelatedContent = true
relatedContentLimit = 3
```
Then add to `config/_default/hugo.toml`:
```toml
[related]
  includeNewer = true
  threshold = 80
  toLower = false
  [[related.indices]]
    name = "tags"
    weight = 100
  [[related.indices]]
    name = "categories"
    weight = 80
  [[related.indices]]
    name = "series"
    weight = 60
  [[related.indices]]
    name = "date"
    weight = 10
```
Shows "Related Articles" at the bottom of each post.

### Edit on GitHub Link

Add to `[article]` in `params.toml`:
```toml
showEdit = true
editURL = "https://github.com/wshayes/wshayes.github.io/edit/main/content/"
```
Adds an "Edit this page" link to each article.

### Hero Images on Articles

Add to `[article]` in `params.toml`:
```toml
showHero = true
heroStyle = "background"  # options: basic, big, background, thumbAndBackground
```
Then add a `feature*` or `thumb*` image (e.g. `feature.jpg`) to any post's page bundle directory to use it as a hero banner.

### Series Navigation Module

Add to `[article]` in `params.toml`:
```toml
seriesOpened = true
```
Displays an expandable navigation module on posts that belong to a series, showing all other posts in that series.

## Shortcodes for Writing Posts

Use these inside your markdown content files.

### Alert Boxes
```md
{{</* alert */>}}
**Warning!** This action is destructive!
{{</* /alert */>}}

{{</* alert icon="fire" cardColor="#e63946" textColor="#f1faee" */>}}
This is an error!
{{</* /alert */>}}
```

### Badges
```md
{{</* badge */>}}New!{{</* /badge */>}}
```

### Mermaid Diagrams
```md
{{</* mermaid */>}}
graph LR;
A[Input]-->B[Process];
B-->C[Output]
{{</* /mermaid */>}}
```

### Charts (Chart.js)
```md
{{</* chart */>}}
type: 'bar',
data: {
  labels: ['Jan', 'Feb', 'Mar'],
  datasets: [{
    label: 'Posts',
    data: [12, 19, 3],
  }]
}
{{</* /chart */>}}
```

### KaTeX Math
```md
{{</* katex */>}}
\(f(x) = x^2 + 2x + 1\)
```

### Image Gallery
```md
{{</* gallery */>}}
  <img src="photo1.jpg" class="grid-w33" />
  <img src="photo2.jpg" class="grid-w33" />
  <img src="photo3.jpg" class="grid-w33" />
{{</* /gallery */>}}
```

### GitHub Repo Card
```md
{{</* github repo="wshayes/wshayes.github.io" */>}}
```

### Timeline
```md
{{</* timeline */>}}

{{</* timelineItem icon="code" header="Started Blog" badge="2008" */>}}
First post on Blogger.
{{</* /timelineItem */>}}

{{</* timelineItem icon="star" header="Migrated to Hugo" badge="2026" */>}}
Moved everything to Blowfish.
{{</* /timelineItem */>}}

{{</* /timeline */>}}
```

### Icons
```md
{{</* icon "github" */>}}  {{</* icon "linkedin" */>}}  {{</* icon "rss" */>}}
```
Full list: https://blowfish.page/samples/icons/

### Lead Paragraph (larger intro text)
```md
{{</* lead */>}}
This paragraph will be displayed larger as an article introduction.
{{</* /lead */>}}
```

## Front Matter Options for Posts

Add these to the YAML front matter of any `index.md`:

```yaml
---
title: "My Post"
date: 2026-01-15
tags: ["python", "docker"]
categories: ["Medium Archive"]
series: ["Through the Haze"]
description: "Short description for SEO and cards"
summary: "Custom summary for list pages"
draft: true                    # hide from production
showTableOfContents: true      # per-post override
showReadingTime: false         # per-post override
showHero: true                 # show feature image as hero
heroStyle: "big"               # basic, big, background, thumbAndBackground
featureimage: "https://..."    # external hero image URL
---
```

To use a local hero image, place a file named `feature.jpg` (or `feature.png`, `thumb.*`) in the post's page bundle directory alongside `index.md`.

## Color Schemes

Change `colorScheme` in `params.toml`. Built-in options:
`blowfish`, `avocado`, `fire`, `ocean`, `forest`, `princess`, `neon`, `bloody`, `terminal`, `marvel`, `noir`, `autumn`, `congo`, `slate`

You can also set `defaultAppearance = "dark"` for dark mode by default, or keep `autoSwitchAppearance = true` to follow the user's OS preference.
