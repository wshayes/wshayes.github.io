---
title: "Django, Poetry, ER Diagrams, Apple MacOS Installation challenges"
date: 2024-09-10T12:07:34.256Z
categories: ["Medium Archive"]
---

---

The goal of this article is to document how to install graphviz so I can easily generate ER diagrams in Django.

[django-extensions](https://django-extensions.readthedocs.io/en/latest/) has a great [utility](https://django-extensions.readthedocs.io/en/latest/graph_models.html?highlight=graph#graph-models) function called *Graph models*. This will use `graphviz`to provide a graphical overview or ER diagram of your data models (e.g. an Entity-Relationship diagram of your database tables).

Everytime I try to do this in a new project I have problems installing the supporting library pygraphviz to support this on my Mac (M1+). I’m writing this mostly to make sure I document how to install pygraphviz for myself. Hopefully, it’s helpful to other people as well.

The wonderful people answering the support request for `pygraphviz`, in particular [michaeloliverx](https://github.com/michaeloliverx) and [jeanclaude-jardim-oxb](https://github.com/jeanclaude-jardim-oxb), provided easy solutions if you are getting the following error when trying to install `pygraphviz:`

```
fatal error: 'graphviz/cgraph.h' file not found
```

The solution if you are using `poetry` is the following:

```
brew install graphvizexport CFLAGS="-I $(brew --prefix graphviz)/include"export LDFLAGS="-L $(brew --prefix graphviz)/lib"poetry add pygraphviz
```

and the solution if you are using `pip` is the following:

```
python3 -m pip install \                --config-settings="--global-option=build_ext" \                --config-settings="--global-option=-I$(brew --prefix graphviz)/include/" \                --config-settings="--global-option=-L$(brew --prefix graphviz)/lib/" \                pygraphviz
```

After this, and of course installing django-extensions, you can run:

```
./manage.py graph_models -a -g -o db_visualized.png
```

to get something like this:

![](https://cdn-images-1.medium.com/max/800/0*oUDSwPeIfK_FmO5o)
