---
title: "FastAPI/Starlette debug vs prod"
date: 2019-03-01T21:09:16.608Z
categories: ["Medium Archive"]
---

---

### FastAPI/Starlette debug vs prod

![Photo by Austin Ban on Unsplash](image.jpg)
*Photo by Austin Ban on Unsplash*

> **Updated**: *uvicorn* now uses `--reload instead of --debug` , and the FastAPI docker image provides a `/start-reload.sh` that will start with reload enabled.

> Update2: [@euri10](https://github.com/encode/uvicorn/issues/452#issuecomment-551849747) recommended using `--reload-dir <path>` for uvicorn as `--reload` tracks everything in sys.path. I updated the article below accordingly.

Really enjoying working with the Python Async (ASGI-based) framework [FastAPI](https://fastapi.tiangolo.com/) which is built on top of [Starlette](https://www.starlette.io/). Great framework with [OpenAPI](https://www.openapis.org/)/[Swagger UI](https://swagger.io/tools/swagger-ui/) and [ReDoc](https://rebilly.github.io/ReDoc/) built-in, easy to use, middleware functionality with a lot of the things everyone needs (e.g. [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS)) already available.

I generally do most of my development now inside Docker by mounting volumes into the docker container of my code. I’ve been having trouble with getting gunicorn as the supervisor for uvicorn to automatically reload after application file changes. This is a standard capability for gunicorn with WSGI-based applications, but it doesn’t appear to work for uvicorn managed by gunicorn.

> Uvicorn documentation indicates you have to run uvicorn from the command line for the debugging/auto-reloading feature to work. It can’t be run programmatically either.

### Debug Version

Example docker-compose.yml entry:

```
fastapiapp:    image: example/app:localdev    build:      context: ./fastapiapp      dockerfile: ./docker/Dockerfile    ports:      - "80:80"    environment:      - GUNICORN_CMD_ARGS="--reload"  # Don't include - doesn't work
```

```
    # Use ONE of the two commands below to    #   auto-reload when developing
```

```
    # will track everything in sys.path and can use a lot of CPU    command: ["/start-reload.sh"]
```

```
    # will only track files in /app directory    #  (can add additional paths with additional reload-dir options)    command: ["uvicorn", "main:app", "--host", "0.0.0.0", "--debug", "--port", "80", "--reload-dir", "/app"]
```

```
    volumes:      - ./fastapiapp/app:/app
```

The command: `uvicorn main.app --host 0.0.0.0 --reload --port 80` is the part that runs the following dockerfile using uvicorn directly in debug mode so that it restarts after code changes (injected in via the volume, ./fastapiapp, mounted from the docker host machine (e.g. my Mac laptop) to the docker container /app directory.). The `--host 0.0.0.0` is critical as I was getting a bad gateway without it as it defaults to just allowing localhost →127.0.0.1 access.

> I also tried using the environment variable option for gunicorn: `GUNICORN_CMD_ARGS=--reload` (without the uvicorn command line option). This was before I understood that uvicorn ONLY allows debugging (at this point) from the command line.

Another approach is to call uvicorn directly instead of using the FastAPI docker container */start-reload.sh* script by swapping out the command line: *command: [“/start-reload.sh”]* with:

> Updated — replaced `reload` with`reload-dir /app` option. The `reload` option tracks everything in sys.path and uses up a fair amount of cpu (5–10% on my machine vs 2% when only tracking file in the /app directory).

```
command: ["uvicorn", "main:app", "--host", "0.0.0.0", "--debug", "--port", "80", "--reload-dir", "/app"]
```

### Dockerfile

(ignoring the external python library installation using pipenv — just 2 lines):

```
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
```

```
RUN pip3 install pipenv
```

```
# -- Adding PipfilesCOPY Pipfile PipfileCOPY Pipfile.lock Pipfile.lock
```

```
# -- Install dependencies:RUN set -ex && pipenv install --deploy --system
```

```
COPY ./app /app
```

### Production version

To use the production-oriented setup of gunicorn managing uvicorn, just comment out the command line in the docker-compose.yml file. Restart the docker container. Done!

The image I’m basing this Dockerfile on runs gunicorn with uvicorn on the main.py app attribute automatically — e.g. something like `gunicorn main:app`

### Finally

Many thanks to Tom Christie (Starlette), Sebastián Ramírez (FastAPI) and everyone else that has contributed to those projects. They are delightful to use and the user community/project owners have been really supportive.
