---
title: "Python virtualenv shell prompts"
date: 2022-05-21T20:07:36.721Z
categories: ["Medium Archive"]
---

---

### Python virtualenv shell prompts

![Photo by Gabriel Heinzer on Unsplash](https://cdn-images-1.medium.com/max/800/0*60b_UMhj3I5LPd78)
*Photo by Gabriel Heinzer on Unsplash*

A quick note so next time I’m trying to figure out how to get a useful shell prompt with my current python virtualenv indicated, I’ll know how to do it.

If you don’t know what this means, this article is not for you (yet!).

### Problem

You’ve got several python codebases using different virtualenv’s.

You are activating a virtual environment and your beautiful prompt (using [Starship](https://starship.rs/) of course) shows the following:

```
:~/code/python_app1 (develop) [*] via 🐍 v3.10.2 (.venv)
```

The `.venv` on the end indicates that your virtualenv is active, but which one is activated? I like to keep my [virtualenv in poetry](https://python-poetry.org/docs/configuration/#virtualenvsin-project) inside my code and add the directory to `.gitignore` which leads to all of my virtualenvs showing up as `(.venv)` .

### Solution

Since we cannot yet pass a prompt for virtualenvs when creating initializing poetry, we can edit the `.venv/pyvenv.cfg` file and add the following line to it:

```
prompt = CHANGEME
```

This prompt value will get picked up by [Starship](https://starship.rs/) when you are using the standard python prompt fragment configuration.
