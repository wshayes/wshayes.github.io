---
title: "Github Actions — my initial realizations"
date: 2019-11-11T16:59:47.934Z
categories: ["Medium Archive"]
---

---

![Photo by Gia Oris on Unsplash](image.jpg)
*Photo by Gia Oris on Unsplash*

[GitHub Actions](https://github.com/features/actions) is a build tool integrated into GitHub that allows you to run build pipelines defined in files added to your GitHub code repository. You can start these workflows based on any branch changes, pull requests, code pushes, pushed git tags, API requests, or scheduled jobs.

At Biodati, we firmly believe both code and application quality is highly dependent on automation and automated testing. A key objective for our platform is to attain a consistent level of frictionless deployment. To facilitate this, we are working on automating as much of the code testing, platform deployment, and server management as we can. GitHub Actions is helping us automate build, testing, and deployment VERY cost-effectively.

It took me a little while to start understanding GitHub Actions — probably because I’m not a DevOps engineer. Couple that with the fact I’ve just started working with it helps explain why I experienced some bumps in the road. I am hoping to help others who are getting started with GitHub Actions to make things a bit less bumpy. I like GitHub Actions, but I find the documentation for it currently to be quite opaque, hard to search, and confusing.

Let’s start with the positives! Things I like about GitHub Actions:

1. Built into GitHub — fully integrated
2. Version controlled with the codebase (I don’t look at anything for CI (Continuous Integration) that isn’t managed by a text-based pipeline document embedded with the code)
3. Docker friendly (very docker friendly)
4. Allows services to be spun up with test code for integrated testing

Things that are not great (yet!) — GitHub Actions will not officially launch for another couple of days.

1. No UI option to manually start a pipeline (e.g., manual release or deployment) — likely coming very soon (can use [DeliveryBot](https://deliverybot.dev/) until then)
2. Documentation and documentation search
3. No ability to filter between docker and node-based actions in the [GitHub Actions Marketplace](https://github.com/marketplace?type=actions)
4. No way to run GitHub Actions locally for testing/debugging before pushing into GitHub

> [Workflow syntax](https://help.github.com/en/actions/automating-your-workflow-with-github-actions/workflow-syntax-for-github-actions) help: I keep having trouble finding this page in the documentation for workflow syntax.

### Realization #1 — Virtual Machine

GitHub Actions starts up a new virtual machine using the OS you identify using runs-on (e.g. `runs-on ubuntu-latest` ) for every job. You then run things on this machine with every `uses` or `run` step in the job.

I’m still not clear what is [installed by default](https://github.com/actions/virtual-environments) on this virtual machine and what is not.

### Realization #2 — Uses Action step

The `uses` step either runs an action that does some setup or runs something (build process, deployment, etc.) on the virtual machine.

The [node setup](https://github.com/actions/setup-node) or [python setup](https://github.com/actions/setup-python) actions do just that, and they add a specific version of node or python (or if you are using the matrix option — it will setup multiple versions one after another). An action like slack-notify (from the [GitHub Actions Marketplace](https://github.com/marketplace?type=actions)) can install functionality (e.g., a slack script) and run that script with provided inputs.

### Realization #3 — Dockerfile, Docker, Node Action

The `uses` step in the job can be created by referencing an action based on a Dockerfile, or use a Docker image directly or create the Action as a Node.js script.

The Dockerfile will build the first time you run the task and will generally/mostly/sort of cache the Dockerfile build layers. I’ve not figured out when it caches and when it doesn’t. So the Dockerfile appears to be the slowest option as it has to be built into the new virtual image used for the job each time.

The next slowest option is using a Docker image — due to how long it takes to pull the image (into the new virtual machine created for every job). The fastest option is using the Node-based action (which is why I’d like a way to filter Actions on the Marketplace to Node-based or not).

### Realization #4 — Run step

This one is embarrassing, but I think I got a bit confused with `uses` and `run`. Each `run` step is just running a CLI command(s) in the shell of the virtual machine using whatever has been installed by prior `run` or `uses` actions before it.

I also like the ability to use the literal block style for multi-line strings for adding multiple commands in one `run` step.

```
# Single line command- run: npm install
```

```
# uses default shell (bash in ubuntu)- name: Clean install dependencies and build   run: |    npm ci    npm run build
```

```
# using a python shell- name: Display the path   run: |    import os    print(os.environ[‘PATH’])    shell: python
```

GitHub Actions is a very cost-effective option for small startups growing their CI capabilities. I’ve only really evaluated it for this purpose — it may be great for large enterprises as well.

I like GitHub a lot, and we have all of our code already on it. However, if I were starting from scratch, I would have taken a hard look at Gitlab. The functionality of GitHub/GitHub Actions/Zenhub/DeliveryBot is already built into Gitlab. Gitlab’s version of GitHub Actions is more mature than GitHub’s though I suspect GitHub Actions will mature very rapidly — it’s already quite good. I’ve not looked/tested Gitlab, so I can’t say which CI implementation is better.
