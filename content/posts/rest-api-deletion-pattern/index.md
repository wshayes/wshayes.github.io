---
title: "REST API deletion pattern"
date: 2019-07-15T13:15:45.145Z
categories: ["Medium Archive"]
---

---

### REST API deletion pattern

![Photo by Boris Smokrovic on Unsplash](image.jpg)
*Photo by Boris Smokrovic on Unsplash*

Patterns in development are really helpful. As we refine our patterns, they hopefully become easier to develop and most importantly easier to use.

Simple things are often much more complex than they seem. One example is the exercise of deleting things using a REST API approach. This is the story of our evolution to our current pattern at [BioDati](https://biodati.com) (which is building the best communication platform for biology in the world).

Canonical REST, keeping absolutely true to the philosophy of REST, will have two endpoints for deleting resources (we will use `users` as the example resource):

```
DELETE https://example.com/users  # delete all usersDELETE https://example.com/users/1  # delete user 1
```

This works very well — it’s easy to understand and remarkably easy to shoot yourself in the foot — well actually blow your foot off up to the knee at least.

The problem here is that if you are programmatically deleting user 1 with a variable in your code that happens to have a null value in that variable — you just deleted all of the users in your database. Unfortunately, I know this can happen because I did it and had to waste time recovering that data.

A ‘simple’ solution to get rid of that problem was applied. We required a query param to validate that you were actually desiring to remove all users.

```
DELETE https://example.com/users?areyousure=yesiam
```

Yes, this is an anti-pattern. No, we did not think hard about this before applying it.

Another approach is to use the following:

```
DELETE https://example.com/users/all
```

Now we clearly want to delete all users when we hit that endpoint. Unfortunately, two issues pop up in this situation.

- You have to make absolutely sure that no users are named ‘all’.
- Some REST API frameworks match routes based on first or last found

Order is very important as ‘all’ may match as an {id} instead of as the *delete all users* route depending on how your routes are parsed and matched.

```
https://example.com/{resource}/{id}  # resource=users, id=all
```

### Logical deletes and purging

You may want to add the ability to logically delete (e.g. mark for deletion) and have separate endpoints to actually delete a resource. This is a very good pattern providing the users a safety net for deletes.

We initially implemented this with an overloaded endpoint using query parameters to indicate intent (default was logical delete, e.g. purge=0).

```
DELETE https://example.com/all_users?purge=1
```

### Our current REST deletion pattern

```
DELETE https://example.com/delete_all/users  # Delete all usersDELETE https://example.com/delete_all/projects 
```

```
DELETE https://example.com/users/1    # Delete user=1
```

```
DELETE https://example.com/purge_all/users  # Purge all users DELETE https://example.com/purge_all/projects
```

```
DELETE https://example.com/users/purge/1    # Purge user=1
```

Delete is a logical delete. This just marks the resource(s) for deletion and removes them from being returned/searched by default.

This pattern takes two calls to fully remove a user or all users though you can allow purge calls to delete unmarked (e.g. un-logically deleted resources). I prefer to have it as two calls because it makes it easy to allow users to logically delete resources and then call purge\_all/users periodically to remove any users marked for deletion. You could even add an option in the purge code to only remove resources that have been marked for over X days/weeks/months.

The standard individual REST CRUD operations are handled in a standard fashion, but the really dangerous delete all and purge all operations are not easy to access without intention.

> None of this adheres to a strict REST API philosophy. I prefer to take a more pragmatic approach to REST.
