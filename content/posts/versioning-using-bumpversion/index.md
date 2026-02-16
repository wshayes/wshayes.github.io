---
title: "Versioning using bumpversion"
date: 2018-08-24T00:12:53.321Z
categories: ["Medium Archive"]
---

---

Having some fun with devops — scripting all the things.

![“A focused man working on a sticker-covered laptop in a coffee shop” by Tim Gouw on Unsplash (not me :)](image.jpg)
*“A focused man working on a sticker-covered laptop in a coffee shop” by Tim Gouw on Unsplash (not me :)*

### ADDED 2/11/2019 — Recommend bump2version — it’s an actively maintained fork of bumpversion.

[Bumpversion](https://pypi.org/project/bumpversion/) (use [bump2version](https://github.com/c4urself/bump2version) instead — it installs a command called bumpversion) is a python-based tool that you can use to manage [semantic versioning](https://semver.org/) for your application, library, module in any language you want. The nice thing about it is it makes it easy to update all of the files that might contain your version numbers such as VERSION, documentation version numbers hardcoded in the text, etc. It also provides an easy way to semantically note what parts to increment, e.g.

```
bumpversion [major|minor|patch]
```

In the shell ($ indicates a prompt in the terminal):

```
$ cat version$ 0.1.0
```

```
$ bumpversion minor
```

```
$ cat version$ 0.2.0
```

### Bump2version configuration file

Line 2 above starts at 0.0.0 so that the first time we run `bumpversion minor` , it results in 0.1.0-dev0.

> NOTE: 0.0.0 or whatever you have for current\_version has to match what’s in your different files (e.g. lines 19, 21, 23 — else you’ll get an error message trying to run the bumpversion commands)

We set (line 4)`tag = False`so that we do not automatically commit tags every build number created.

The parse (line 5) defines the components of the version number that we want to manage which is also tied to how we will serialize the number (line 6). Bump2version basically finds the string (current\_version — line2), splits it into components according to the parse regex and then rebuilds it using the first matching serialization which has all of the relevant parts.

Lines 10–15 control how the release part of the version number is managed. We basically rotate through dev and prod. Since prod is optional — it is not shown in the version number (just one of those tricks you have to know though it is documented in the bump2version documentation). This could have had values of [‘alpha’, ‘beta’, ‘gamma’, ‘delta’] with delta optional and it would progress from alpha → beta → gamma → <blank>.

Line 17 is the part that allows use to increment the build number.

Line 19 and 21 refer to two different files that have the version number in them. This is all that is needed to identify that they have a version number that needs to be replaced.

Lines 23–25 indicate a Swagger document. This could possibly have text in it that is the same as the version number. In order to make the match more specific, we can add the search and replace options so that we have to match `version: 0.0.0`

---

### Usage

```
$ cat VERSION0.0.0
```

```
$ bumpversion major; cat VERSION1.0.0-dev0
```

```
$ bumpversion minor; cat VERSION1.1.0-dev0
```

```
$ bumpversion patch; cat VERSION1.1.1-dev0
```

```
$ bumpversion build; cat VERSION1.1.1-dev1
```

```
$ bumpversion build; cat VERSION1.1.1-dev2
```

```
$ bumpversion --tag release; cat VERSION1.1.1
```

```
$ bumpversion minor; cat VERSION1.2.0-dev0
```

From the examples above, one can see that every time you increment based on major, minor or patch, it resets with a dev0 appended. You can then run `bumpversion build` to increment build numbers as you make changes before you release the changes to your production branch.

You add the `--tag` to the `bumpversion --tag release` in order to tag the commit in git when you cut a release. This is why we have tag = False in line 4 of the configuration file so we don’t commit tags for every change in the version number.

---

Thank you [Alan Briolat](https://github.com/alanbriolat) for your [insights](https://github.com/peritus/bumpversion/issues/77#issuecomment-130696156) that led to this article! Your contribution to an issue in the bumpversion issue queue in 2015 is still helping people.
