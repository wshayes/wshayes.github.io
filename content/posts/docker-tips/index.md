---
title: "Docker Tips"
draft: true
categories: ["Medium Archive"]
---

---

#### Docker Compose Environment Variables

`docker-compose` is a wonderful tool and generally it works great with very little frustration. I’ve learned the value of [**The twelve-factor app stores config in *environment variables***](https://12factor.net/config)***.*** Whenever I forget it, growth of my project reminds me sharply as I wind up refactoring in order to use environment variables to pass configuration to my applications.

I was using:

```
services:   api:       environment:          - HOST_NAME=${HOST_NAME:?err}
```

```
# instead of this:services:   api:       environment:          - HOST_NAME=${HOST_NAME:?"Missing HOST_NAME"}
```

1. ERROR: Missing mandatory value for “environment” option in service “dev\_api”: err

2. ERROR: Missing mandatory value for “environment” option in service “dev\_api”: “Missing ENTITIES\_COLL\_DEV”

Notes: <https://www.tldp.org/LDP/abs/html/parameter-substitution.html>

[**Shell Parameter Expansion (Bash Reference Manual)**  
*The '$ ' character introduces parameter expansion, command substitution, or arithmetic expansion. The parameter name or…*www.gnu.org](https://www.gnu.org/software/bash/manual/html_node/Shell-Parameter-Expansion.html "https://www.gnu.org/software/bash/manual/html_node/Shell-Parameter-Expansion.html")

#### Dockerignore File

The `.dockerignore` file really helps in speeding up builds and reducing secrets being inadvertently added to your docker image. As mentioned in the article below in more detail — instead of excluding files that you don’t need do this instead:

1. Exclude everything
2. Whitelist add in the things that your image needs

> Multi-stage builds also help with faster builds and have the bonus of smaller images.

Example .dockerignore file:

```
# Ignore everything*# Allow files and folders with a pattern starting with !!lib/**/*.js!lib/app
```

[**How to use your .dockerignore as a whitelist**  
*Many tools use ignore files to exclude files from build, process or publish steps (e.g. .npmignore for npm, .gitignore…*kevinpollet.dev](https://kevinpollet.dev/posts/how-to-use-your-dockerignore-as-a-whitelist/ "https://kevinpollet.dev/posts/how-to-use-your-dockerignore-as-a-whitelist/")

#### Checking your Dockerignore File

[**pwaller/docker-show-context**  
*Ever wonder why docker pauses when you do docker build, and what you can do about it? You know, when it says Sending…*github.com](https://github.com/pwaller/docker-show-context "https://github.com/pwaller/docker-show-context")

You can build the docker image from Peter Waller’s github repo and then run it in the directory with the .dockerignore file (e.g. your docker build context directory that is sent to build your docker image). It will then show you information on the largest files, directories and filetypes being sent to the docker build process for your image.
