---
title: "Local Dev on Docker - Fun with DNS"
date: 2018-12-06T18:28:29.287Z
categories: ["Medium Archive"]
---

---

### Local Dev on Docker - Fun with DNS

![Photo by Dave Webb on Unsplash](image.jpg)
*Photo by Dave Webb on Unsplash*

> Updated Dec 9, 2018: Added link to instructions on making the loopback alias persistent across reboots

I’m working on a project ([BioDati](https://biodati.com) and [BEL.bio](https://bel.bio)) that has a web front-end, several custom datastore services, and various infrastructure services (e.g. traefik, arangodb, elasticsearch, etc). The application is a single-page-application (SPA) with several microservice API’s supporting it. I wanted to set up a local development environment that matched production as closely as possible. Of course, desires and actual reality diverged immediately which led to the following adventure in Docker and DNS setup.

The brick wall above tells the story of how painful my many attempts at even understanding what my problem was and how to solve it. It’s always surprising to see how simple the solution can be to what was an incredibly frustrating problem.

### Goal:

- Support local development of multiple docker services with API interdependencies
- Ability to use fully qualified domain names from Mac host
- Ability to use same fully qualified domain names inside Docker containers

### Environment/Setup

- Mac Docker Desktop (2.0.0.0-mac81)
- Traefik (1.7.4)
- MacOS (10.14 — Mojave)

### Solution

- Run *sudo ifconfig lo0 alias 10.254.254.254 (*to make persistent *—*[Persistent loopback interfaces in Mac OS X](https://blog.felipe-alfaro.com/2017/03/22/persistent-loopback-interfaces-in-mac-os-x/))
- Install DNSMasq ([good tutorial](https://www.stevenrombauts.be/2018/01/use-dnsmasq-instead-of-etc-hosts/) on doing this) (but use 10.254.254.254 instead of 127.0.0.1 for the nameserver and address target)

### Details

[Traefik](https://traefik.io/) is used for reverse proxying to your containers (for ports 80 and 443). I won’t go into detail on setting it up here, but it allows me to label my containers with a domain name and have traffic routed to that container based on that domain name on my Mac. As long as I can get traffic for those domains to my host machine (Mac), all is well.

Docker Desktop on Mac maps your local DNS setup into the docker containers. Your DNS servers include your local machine if you have that setup (and [dnsmasq](http://www.thekelleys.org.uk/dnsmasq/doc.html) can be set up to add to your DNS resolvers for specific domains or completely take over DNS resolution).

Typically when you setup dnsmasq, you define 127.0.0.1 as your target for your local domains (e.g. ‘.local’, ‘.test’, ‘.box’, etc — just don’t use ‘.dev’ as that is problematic). This then allows any domains ending in \*.test (e.g. service1.test for example) to be directed to 127.0.0.1. This works great when you are using your browser or terminal on your Mac to access your API service endpoint, but it does not work when you are inside your container trying to access another service as your DNS request for service2.test returns 127.0.0.1 which is your current container not your container host Mac machine.

```
dig service2.test   # results in 127.0.0.1
```

> Note: *dig* may not be installed in your docker container image. You can override the Dockerfile to add it — in Ubuntu it is part of the dns-utils package.

> Jake Goulding shared the insight on using 10.254.254.254 in the following blog article which was the key piece I needed to make this work — thank you Jake!

[**Running dnsmasq on OS X and routing to virtual machines**  
*At work, I needed to run a Docker container with a Rails application that talked to another application running inside…*jakegoulding.com](http://jakegoulding.com/blog/2014/04/26/running-dnsmasq-on-os-x-and-routing-to-virtual-machines/ "http://jakegoulding.com/blog/2014/04/26/running-dnsmasq-on-os-x-and-routing-to-virtual-machines/")

On your Mac, run the following in a terminal to set up the IP address alias for 127.0.0.1 (e.g. localhost):

```
sudo ifconfig lo0 alias 10.254.254.254
```

If you use 10.254.254.254 (semi-randomly picked from the list of private IP addresses) as your DNS target IP for your local domains, then querying DNS inside the container using *docker exec* or *docker run* results in:

```
dig service2.test  # results in 10.254.254.254
```

You can also check your domain resolution on your Mac host

```
dig service2.test @127.0.0.1  # results in 127.0.0.1
```

> Note: You have to put @127.0.0.1 in your dig request to get it to query your local DNS service (e.g. dnsmasq).

Now I can use domain names for my services and access them from both my Mac host and between docker containers. All of the traffic is proxied by Traefik both from direct host requests to services and Docker container to container requests.

Finally — make the loopback alias persistent by following the instructions here: [Persistent loopback interfaces in Mac OS X](https://blog.felipe-alfaro.com/2017/03/22/persistent-loopback-interfaces-in-mac-os-x/). Otherwise, you’ll need to re-run the alias command every time you reboot.

> [@tsc on StackOverflow](https://stackoverflow.com/questions/53181154/docker-container-internal-vs-external-dns-resolution-issue-using-traefik/53503399?noredirect=1#comment101968337_53503399) still had problems with this approach until they put `dns: 10.254.254.254` in the docker-compose file.

### Bad Solution #1

I first tried to use service names for inter-container requests which worked perfectly fine between containers (and is what I still use for the non-public endpoints, e.g. Arangodb and Elasticsearch services).

This resulted in the unfortunate situation where I needed to know if I was accessing a service from a host context or a container context which leads to significant extra code and makes this solution more fragile.

### Bad Solution #2

I next tried to use network aliases in Docker Compose to specify the domain names I wanted to use for each service. This worked great in allowing me to use the same URL/domain both from the Mac host level and from inside the container.

This basically routed traffic through Traefik from the Mac host and directly between containers for internal container traffic — pretty much the same as if I’d used the service names.

When I started using https URLs with Traefik for SSL termination (using Let’s Encrypt) for my release applications — this resulted in having two different contexts again as I either had to handle HTTPS traffic in each container or deal with an https context external to the containers using Traefik for SSL termination AND use HTTP for contexts internal to the containers. The Docker container network alias routed the traffic directly to the container from other containers — it never went through Traefik.

### Thanks!

Thanks to all of the bloggers that I didn’t directly link — you guys are great sharing your knowledge — I’ve read through almost everything mentioning Docker/DNSMasq out there.

Also — thanks to Daniel Tomcej from Traefik for your help. Your advice was spot on — I just didn’t understand it at the time.
