---
title: "JSON Web Token payloads"
date: 2016-03-03T13:13:00Z
categories: ["Blogger Archive"]
series: ["Through the Haze"]
---

I really like the [JSON Web Token](https://jwt.io/) (JWT) technology for Single Page Application (SPA) user authentication.  I started off quite excited about storing things like permissions and other user profile data in the JWT.  My initial thoughts around JWT is that it was a good ‘state’ variable to hold user profile information on the client side.  
  
The problem with that idea is that it is hard to expire and update a JWT if the user changes their display name or gets new permissions/claims.  If your SPA client is using the JWT payload to hold this mutable (server side mutable) information, your client won’t be updated in a timely manner - it will have to wait for a new JWT to be issued.  It is a little mean to require the user to logout and back in again to be able to use their new permissions or see their new display name show up on the web application.   
  
Don't get me wrong, I'm not talking about concerns of the client side manipulation of the JWT payload.  I don’t trust anything from the client side.  Anything coming from the client has to be checked/validated on the server.  I know the new permissions really matter on the server side, but I would generally only allow users to see functionality that they are permitted (not that they can’t hack the front end code and do whatever they want on the front end - they just would not be able to complete the transaction on the server).
