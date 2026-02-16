---
title: "Exporting Intercom Help documents"
date: 2020-10-29T20:18:55.417Z
categories: ["Medium Archive"]
---

---

![Photo by Barth Bailey on Unsplash](image.jpg)
*Photo by Barth Bailey on Unsplash*

[Intercom](https://www.intercom.com/), the customer support tool, is really good at a lot of things — their help documents (Articles) tool is not one of those things. I didn’t see any easy way to extract the documents we had created in Intercom so I had to find another way to liberate them.

I looked into their API, but it was not apparent how to access it as a customer instead of an integration application developer. I created a web-scraping script to extract our content and associated screenshots/images.

> This is a quick hacked together script to do what I needed (migrating the HTML content into [MkDocs](https://www.mkdocs.org/) (a markdown static site documentation tool). Feel free to use it, extract some code from it, or run away screaming :)
