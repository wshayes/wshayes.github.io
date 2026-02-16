---
title: "Poetry and Docker with a private git repo package"
draft: true
categories: ["Medium Archive"]
---

---

### Poetry and Docker with a private git repo package

Initial conditions

Add the following

`ssh-add -K <ssh_key_file>`

Dockerfile setup:

Key lines to make private git repository poetry libraries work are #1, #35 and #54–55 below.

Makefile command to build docker image

```
DOCKER_BUILDKIT=1 docker build --ssh default -t biodati/userstore:dev -t biodati/userstore:$(VERSION) -f ./docker/Dockerfile.prod .
```

Command to build docker image for local development using a docker-compose.yml file:

```
# Template commanddocker buildx bake --set <service_name>.ssh=default <service_name>
```

```
# Example alias that we use, e.g. db service1alias db="docker buildx bake --set $1.ssh=default $1"
```

Note: docker buildx does pull configuration information by default from docker-compose.yml but does not read the local .env file by default like the docker-compose commands do.

Bash commands to make it easier to build images and run them.

```
# Load the .env environment variables into the shell environmentadd_dotenv() {    set -a    [ -f .env ] && . .env    set +a}
```

```
# Rebuild Docker-compose service#   remove image and start over - image has to be named#   same as docker-compose servicedcb() {    add_dotenv    docker-compose stop $1;    docker-compose rm -f $1;    docker rmi $1;    docker buildx bake --set $1.ssh=default $1;    docker-compose up --no-start --no-build $1;    docker-compose start $1;}
```
