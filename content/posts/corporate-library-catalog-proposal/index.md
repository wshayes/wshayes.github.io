---
title: "Corporate Library Catalog Proposal"
date: 2008-06-02T11:09:00Z
draft: true
tags: ["Library Mgmt", "IT"]
categories: ["Blogger Archive"]
series: ["Through the Haze"]
---

I've been thinking about what a library catalog for a corporation really needs to do and thought I'd use the wisdom of the crowds to review the ideas below. The library catalog we are currently using at my company is overkill for what we need, and it doesn't pass my test for what an application should do. In my opinion, software applications are supposed to leave high-level decisions for people and perform all of the rote, decision-less work as automatically as possible.  
  
  
  
Here is the list of what I see as needed in a corporate library catalog:  

- Allow easy ordering of books by anyone
- Automatically add books to catalog after being ordered
- Integrate with book vendors such that fulfillment and labelling are completely outsourced
- Allow easy sharing of books between *library aggregation points*\* and clients
- Make it easy to find and share thoughts regarding books and other media
- Strong search capability, probably supporting faceted search
- Optional: aggregate reviews/comments (or links to such) from the Internet

  
Some things that are not of great interest to me for a library catalog in a corporation:  

- Don't need full MARC capabilities
- Rigorous inventory control

  

### Ordering books

  
I want a library catalog that is integrated with a book ordering system/vendor. I want to search for books that are already owned by the company (both on employee desktops and in library aggregation points) yet also allow searching the entire universe of books that are available to order. If I as either a customer or library book manager order a book, a book request should be sent to the book fulfillment vendor with the book labelling information and associated order information:  

- item number
- call number if desired/available
- requestee  
  - name
  - cost center
  - email address
  - where to ship the book

  
After fulfillment of the book order, an email should be sent to the requestee to confirm receipt of the book. Another email or webservice request should be sent to the library catalog 'turning on' the new item as it should already have all of the information for the book record set up and just need a new status changing it from non-public to public.  

### Lending Books

  
Lending books should be as simple as logging in to the library catalog (which should use LDAP for user authentication) and assigning it from myself (as a library aggregation point mgr or library user) to another registered user (with an email confirmation sent to the new assignee). An option would be to allow someone to request a book which would generate an email request to the current item owner. Of course, all item owners need to be visible and accessible which is a benefit for a corporate library. This is another interaction point to make sure people who are working on similar projects get to know each other and can share books as well as best practice. So far, I have not seen any business book users that are concerned about privacy which is different from the public lending library privacy issue.  
  
Every few months due to the highly distributed nature of the book collection, there will need to be an automated email going out to all of the book owners with a listing of the books they have on permanent loan. They have to confirm they have the books or assign it over to the new owner. If confirmation doesn't occur after a configurable number of attempts to contact the item owner, the item will be marked lost and removed as a publicly available item record (though somehow we'll need to keep the comments recorded against the item). We may segregate the book record from the item record where the item record incorporates the book node but adds the item record number and item owner information. Keeping a history of previous item owners would also be helpful.  

### Classification system and Search

  
We don't have enough books to make it useful for people to come in to the library space to browse our bookshelves to discover books based on physical proximity. Therefore, I need to have an item number and a way of finding a book in a collection, but it doesn't need to be highly classified in an LC or Dewey Decimal system. Online similarity search is more important than serendipity-enhancing physical proximity. Apache Solr is a nice open source faceted search tool that has been incorporated into numerous library catalog systems (including Drupal-based library catalogs and the [Blacklight](http://blacklight.betech.virginia.edu/) project). Of course, using a social web based library catalog would also open up the use of tagging for books and the tags for searching book collections. I've found that tagging works best when it is most selfish and not just an exercise for other people to use (e.g. del.icio.us), but this concept fits well with the bookmarking option suggested below.  

### Social Aspects

  
I really like the idea of library users being able to comment on whether a book is useful or not and share listings of their books. Having RSS feeds of new books or books a department's employees have in their collection would be an easy result of such a library catalog. It should also be easy to create wishlists or bookmark listings of books.  

### Potential Implementation

  
I have seen a lot of interesting developments and useful modules for [Drupal](http://www.drupal.org/) that with the right implementation would get us 80-90% of the way to the online catalog I want. The Drupal Biblio, Millenium, Apace Solr, MARC and a few other modules should provide most if not all of what I need for this.  

### Comments and Suggestions Welcome!

  
Please comment below with suggestions on what is missing or if you think I'm simply crazy for even suggesting this :) I plan for this to be a somewhat living document incorporating suggestions from the comments into this posting.  
  
\* Library aggregation point - library space shelves or just a local collection of books - e.g. self-help books in HR department
