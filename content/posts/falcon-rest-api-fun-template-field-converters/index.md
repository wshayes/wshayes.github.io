---
title: "Falcon REST API Fun: template field converters"
date: 2018-03-15T20:24:12.583Z
categories: ["Medium Archive"]
---

---

![“A Lego stormtrooper on sand” by Daniel Cheung on Unsplash](0m5ue3jx54_HWC96D.jpg)
*“A Lego stormtrooper on sand” by Daniel Cheung on Unsplash*

Why would I bother with something as fascinating as *field template converters*? Funny you should ask that. I was running along, happily with scissors in hand, completely ignorant of what *field template converters* are and quite happy about that …

However, I noticed that I was getting a lot of 404’s from a BEL.bio REST API endpoint.

> The [BEL.bio REST API](https://apidocs.bel.bio) provides [BEL](http://bel.bio) language tooling for parsing, validating, BEL terminology support (as seen below), etc.

The REST endpoint in question is setup as:

```
https://api.bel.bio/v1/terms/{term_id}/canonicalized
```

Turns out that my API endpoint had some occasional nasty inputs for term identifiers (the *term\_id,* which is a url template field) that included a ‘/’ — the dreaded forward slash ([SCOMP:”p85/p110 PI3 Kinase Complex”](https://api.bel.bio/v1/terms/SCOMP%3A%22p85%2Fp110%20PI3Kinase%20Complex%22/canonicalized)) as seen below:

```
https://api.bel.bio/v1/terms/SCOMP:"p85/p110 PI3 Kinase Complex"/canonicalized  (using requests so this will be url-encoded properly - e.g. the spaces, : and quotes)
```

The 404’s were caused by the Falcon router trying to match two template fields instead of one (e.g. /terms/{term\_id}/{field\_two}/canonicalized with term\_id=SCOMP:”p85 and field\_two=p110 PI3 Kinase Complex).

No big deal, I’ll just URL encode the forward slash in the *term\_id* as ‘%2F’ which is the standard url encoding for forward slashes and Falcon will url decode it when it processes it.

Nope! Falcon still saw the forward slash and not the %2F. Fortunately, a quick look at the Falcon issue queue (after a not so quick amount of head scratching and Googling) resulted in the following great description of the problem, by Kurt Griffiths: [“%2F is treated as / in routing”](https://github.com/falconry/falcon/issues/897) (and thank you Qingping Hou for raising the issue). So, not Falcon’s fault, the WSGI server (I’m using gunicorn but most of the WSGI servers do this) is processing the **%2F** back into a forward slash before Falcon’s router could extract the *term\_id* path template field.

Okay, so I really want to replace ‘/’ in the term\_id before I submit the request to the REST API to something really custom that the WSGI server won’t touch. Let’s try \_FORWARDSLASH\_ and hope that no biologist gets cute and names a protein \_FORWARDSLASH\_ (given that someone named a gene ‘a’ — which is nearly impossible to extract via text mining — not a great hope, but we’ll go with this for now).

Now how to handle it on the Falcon side, I could:

- convert it back everytime I use a term\_id type template field in a path in the handler function for each endpoint that needs it
- replace \_FORWARDSLASH\_ in every URL that I process in Falcon middleware processing (which is awesome, but a little too brute force)
- or use the new (as of Falcon 1.3) template field converter feature

Using the template field converter is a lot more elegant than processing every request whether it is needed or not or remembering to handle this in every endpoint handler function.

According to the [instructions](http://falcon.readthedocs.io/en/stable/api/routing.html?highlight=converter#custom-converters) for template field custom converters, I needed to add a Custom Converter Class implementing the [BaseConverter interface](http://falcon.readthedocs.io/en/stable/_modules/falcon/routing/converters.html).

```
class BelConverter(falcon.routing.converters.BaseConverter):    """Convert BEL path parameter"""
```

```
def convert(self, value):        return value.replace('_FORWARDSLASH_', '/')
```

and register it with my api

```
# Router converter for BEL Expressions and NSArgs#   converts_FORWARDSLASH_ to / for selected URI template fields
```

```
api.router_options.converters['bel'] = BelConverter
```

and then add the field converter as depicted in the [help](http://falcon.readthedocs.io/en/stable/api/routing.html?highlight=converter#field-converters) — e.g. the ‘:bel” after the *term\_id*.

```
api.add_route(‘/terms/{term_id:bel}/canonicalized’, TermCanon())api.add_route(‘/terms/{term_id:bel}/decanonicalized’, TermDecanon())
```

Note: You have to add the converter tag to all template fields at the same level. When I was initially testing it, I only added the “:bel” converter tag to the canonicalized endpoint, but the server wouldn’t start since it expected all /terms/{term\_id}/… to be /terms/{term\_id:bel}/…

I’m still pretty blissfully ignorant, but less so now about Falcon field template converters — still very happy with and appreciative of Falcon (thanks Kurt Griffiths and John Vrbanac for all of your hard work on Falcon!)
