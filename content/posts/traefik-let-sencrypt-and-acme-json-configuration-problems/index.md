---
title: "Traefik, Let’sEncrypt and acme.json Configuration Problems"
date: 2021-03-25T17:08:02.378Z
categories: ["Medium Archive"]
---

---

![Photo by NOAA on Unsplash](https://cdn-images-1.medium.com/max/800/0*d8VtALf9jMmkMbC1)
*Photo by NOAA on Unsplash*

**TL/DR**: To save acme.json file with LetsEncrypt details for Traefik — volume mount parent directory with Traefik container and configure `…acme.storage` inside that parent directory `/shared/acme.json`

```
# Skipping parts that aren't relevant in docker-compose file
```

```
volumes:  - ./shared:/shared
```

```
command:  - --certresolv.myresolver.acme.storage=/shared/acme.json
```

### Deets!

Nope, the picture has nothing to do with this story. It’s just to help me recover my mind after an incredibly stupid and frustrating session with [Traefik](https://traefik.io/) configuration. Don’t get me wrong, Traefik is a great reverse proxy for managing docker containers, but you definitely want to configure it, step away and never touch the configuration again!

So, let’s set up [Let’s encrypt](https://letsencrypt.org/) with Traefik so we get all of the SSL goodness for our websites and web API’s in an automated, updated, and free fashion [actually, I do periodically donate to Let’s Encrypt — so not completely free, but well worth it :) ].

Unfortunately, if you do this one thing in docker-compose.yml:

```
# Skipping parts that aren't relevant
```

```
volumes:  - ./acme.json:/acme.json
```

```
command:  - --certresolv.myresolver.acme.storage=/acme.json
```

You will wind up with a directory called acme.json instead of a simple file. This is not handled well at all by Traefik. If you expose the Traefik dashboard via SSL, you’ll see a message like this in the logs.

> `msg="the router traefik@docker uses a non-existent resolver: myresolver"`

What that means is Traefik couldn’t read the `acme.json` file. Since this was not AT ALL clear to me when I saw that message, I was fortunate to quickly find this Traefik forum article on it: <https://community.traefik.io/t/a-solution-to-the-incredibly-unhelpful-the-router-uses-a-non-existent-resolver-letsencrypt-message/3859>. Thank you so much to Somebody for that post — yes it was literally Somebody who posted that!

So the other fun thing I learned is that you can’t create the acme.json file and volume mount that into the Traefik docker container because Traefik 2+ will fail on an empty acme.json file (though this worked like a charm in the Traefik 1 version).

The only way I and others figured out how to handle this is to make sure we volume mounted a local directory and mapped the acme.json file into that shared parent directory. You can call the `shared` directory name whatever you want — just make sure it matches between the volumes and command sections.

```
# Skipping parts that aren't relevant in docker-compose file
```

```
volumes:  - ./shared:/shared
```

```
command:  - --certresolv.myresolver.acme.storage=/shared/acme.json
```

Again, it’s incredible how amazing Traefik is— you can add in middleware to do access throttling, basic auth, remapping requests on the fly, and dynamic mapping of containers to URLs is just amazing. Once you get your configuration setup locked in, you should be golden — just plan on a lot of time figuring out how to get it configured because the error messages (and missing error messages — that really should show up when some things are mis-configured) always make it a nightmare to get Traefik configured for me.
