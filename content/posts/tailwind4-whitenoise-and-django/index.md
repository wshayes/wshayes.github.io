---
title: "Tailwind4, Whitenoise and Django"
draft: true
categories: ["Medium Archive"]
---

---

### Tailwind4, Whitenoise and Django

![Photo by Rune Haugseng on Unsplash](https://cdn-images-1.medium.com/max/800/0*QOemE_pPIg7UZ8H6)
*Photo by Rune Haugseng on Unsplash*

Another note to remind me of how to set up [Tailwind4](https://tailwindcss.com/), [Whitenoise](https://whitenoise.readthedocs.io/en/stable/django.html) and [Django](https://www.djangoproject.com/) for future me :)

The best way to appreciate this stack (which has to include HTMX and AlpineJS) is to develop using any other framework :) Not having to build two separate applications (front-end JS SPA and a backend API server) and keep them in sync, along with re-doing every bit of permission protection, route mgmt, and view protection in both ‘applications,’ makes me appreciate an AJAX-friendly Multi-Page Application (MPA) web framework like Django with HTMX.

It boggles my mind that people deploy Django as a backend API to serve a Javascript SPA when there usually is no significant client-side functionality needed. I’m not saying every application can be built as an MPA, but unless you are in a very unusual niche of web development, it’s likely much greater than 80%.

**Tailwind notes**

Whitenoise is configured to serve the static files in Django without having to use a separate web server for serving static files. Tailwind is configured to watch for changes in your HTML files and templates, and build your css file with only the CSS elements required in development.

We need to put the tailwind input.css in the static\_src directory so Whitenoise doesn’t try to build it when running collectstatic. If you don’t do this, you’ll get the following error when running ./manage.py collectstatic

```
The CSS file 'styles/input.css' references a file which could not be found:  styles/tailwindcss
```

The base.html template has the line `<link href=”{% static ‘styles/output.css’ %}” rel=”stylesheet”>` which is the output of the tailwind build. However, Whitenoise will rename the file for use in the application in production for cache-busting purposes. You can check this by viewing the source of the page in the browser. It should look something like this: *output.40051257adcf.css.gz*

These are run by `honcho start` for local development and `build.sh` for deployment.

```
For dev:tailwind -i static_src/styles/input.css -o static/styles/output.css - watchFor deployment:tailwind -i static_src/styles/input.css -o static/styles/output.css - minify
```

### Honcho

I can’t talk about Django and Tailwind without talking about the wonderful tool that is [Honcho](https://honcho.readthedocs.io/en/latest/#).

Example Procfile

```
tailwind: /usr/local/bin/tailwind -i static/styles/input.css  -o static/styles/output.css -wdjango: python manage.py runserver_plusworker: python manage.py procrastinate worker --concurrency 5help: cd help; mkdocs serve -a 127.0.0.1:8001
```

Install Honcho, create your ‘Procfile’, and then run ‘honcho start’ to start up all four processes in the terminal at once. When using tailwind with Django, you have to run both the tailwind watcher and Django runserver (I personally prefer runserver\_plus from django-extensions) whenever you are developing. If you forget to run the tailwind watcher and add a new tailwind element in your HTML, it won’t work as it hasn’t been compiled into your output.css file, and, for example, the tailwind element `bg-green-500` won’t be understood by the browser.
