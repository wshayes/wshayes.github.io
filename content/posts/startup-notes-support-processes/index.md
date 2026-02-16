---
title: "Startup Notes: Support Processes"
draft: true
categories: ["Medium Archive"]
---

---

![“landscape photography of road during golden hour” by Rory Hennessey on Unsplash](https://cdn-images-1.medium.com/max/800/0*9glOGYi_3HemE_VF)
*“landscape photography of road during golden hour” by Rory Hennessey on Unsplash*

Starting a company is always full of new challenges. One challenge is figuring out how to support your new customers. Every situation is different — some services are really organization based so you deal with one customer at each organization. Other situations involve many individual paying customers. Basically, the history, support approach and learning opportunities we were introduced to may not relate in any way to your experiences in your company.

### What we do

We provide a SaaS application to help Life Scientists communicate biology more effectively and make that communication computable. We do this by using an open-standard called BEL (Biological Expression Language) and providing a supportive platform to write BEL content and use it in building networks and analyzing life science data. We are currently supporting Life Science organizations like bioPharma and biotechs and plan on providing a personal/teams version of this by the end of the year. We need to support life scientists, data scientists, developers, and organizations.

This may not seem that interesting until you think about the millions of life scientists that have no common language (unlike chemists with their Chemical Reaction Language) to share knowledge with each other much less data scientists. Life sciences are probably the most knowledge-intensive scientific discipline.

### Support History

Our first approach to handle support was temporary and typical. Use email — quick, cheap, natural and works while you are trying to figure out what you actually need. Hopefully, you can move off of this onto a dedicated support tool before you become overwhelmed.

![“black typewriter” by Da Kraplak on Unsplash](https://cdn-images-1.medium.com/max/800/0*iJi1tzRoOTr9CncH)
*“black typewriter” by Da Kraplak on Unsplash*

We have always been a big fan of [Intercom.io](https://www.intercom.com/) for their platform and their continuing education regarding customer support in their blog. They tend to be pricey for startups, but they have an [Early-Stage Startup](https://www.intercom.com/early-stage) option which alleviates some of the early startup budget concerns.

We added Intercom as our main customer support tool and everything was great! Until it wasn’t :) Don’t get me wrong — we LOVE Intercom. It is a fantastic tool. But our customers wanted an overview of all of the issues/bugs raised.

### Where we are now

[Shippable](https://github.com/Shippable/support)

Proposed flow:

1. User uses Intercom to get support.
2. Agent (Customer Service Agent) provides support to User
3. If Agent is not able to resolve issue immediately, Agent opens a Github issue in the BioDati Support repository which goes into the Inbox (the issue is scrubbed to make certain that the issue contains no proprietary information).
4. The issue is tagged with an anonymizing label (e.g. Acme Company -> Brisbane)
5. Users can subscribe to issues to get notifications on status changes or comments
6. Users can add comments directly to the issues or the comments can be managed through Intercom
7. Users can also add Reactions [‘thumbsup/down’, etc] (we’ll provide help documentation on how to do this as well as warnings about the public nature of Issue subscriptions and Reactions)
8. You can view all of the issues via the Waffleboard link or direct in Github and view a filtered set with just the label = <your anonymizing label here> which would be accessible via a link that you can post

Waffleboard: <https://waffle.io/biodati/support>

Github view: <https://github.com/biodati/support>
