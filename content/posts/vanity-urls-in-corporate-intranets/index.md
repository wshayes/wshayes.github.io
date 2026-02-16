---
title: "Vanity URL's in Corporate Intranets"
date: 2012-02-20T15:31:00.003Z
draft: true
categories: ["Blogger Archive"]
series: ["Through the Haze"]
---

#### What is a Vanity URL or Custom Domain Name?

Examples:

- wmhayes.blog.biogenidec.com  (points to camlxlib02.biogenidec.com)
- blog.biogenidec.com  (points to camlxlib02.biogenidec.com)
- blogs.biogenidec.com  (points to camlxlib02.biogenidec.com)
- search.biogenidec.com
- howto.biogenidec.com
- webmail.biogenidec.com

These are subdomains that have been mapped to a specific application on a web server.  The application might be one of many on a server or many servers might be one web application, but we have a single domain name that servers as the URL for an application.  You can also have many domain names pointing to the same web application (there are over 20 different domain names pointing at various sites for the Sharepoint Application - e.g. teams.biogenidec.com, howto.biogenidec.com, search.biogenidec.com, inet.biogenidec.com, …).

#### Why are they important?

- Easier to remember - can usually just type the subdomain (e.g. search in the browser to go to it)
- More stable URL's and domain names

#### URL Stability

Stability of the URL for the application or function is of significant value.  In general, we should not use the server's functional name (such as camlxlib02.biogenidec.com or rtpcommv01.biogenidec.com) for a web application.  If the server is upgraded, it usually takes a new name at which point you need to update the application's access information everywhere it is distributed.  If you use a custom domain, all you have to do is have DNS (our Domain Name Server) point to the new server location.

#### Requesting a domain name for your application

The domain name requested should be of the format .biogenidec.com.   Second thing to note is that there are two options in requesting a custom domain name.  Option 1, an 'A Record' points the domain name you request at the IP address of the server.  Option 2, a 'CNAME Record' aliases the domain you've requested to another domain name.  Usually a CNAME record domain name request will serve your purposes.  I'm blanking on specific reasons why you would need to request an A Record, but hopefully readers of this post will add comments to this blog post to extend our knowledge in this regard.

The process to request a domain name is to enter a Help Desk request specifying:

> I am requesting a custom domain name - this request should be routed to the Networking Queue
>
> I am requesting a CNAME Record.
>
> My new domain name:  fantasticapp.biogenidec.com   #comment change fantasticapp to your subdomain name
>
> Aliased to:  camnxtmpv01.biogenidec.com    #comment change camnxtmpv01 to your application server name

Once you get confirmation that it has been created for you - TEST IT!  On Macs or Linux you can run 'dig XXXXX.biogenidec.com' on the command line to get the details.  On Windows - not sure if there is anything installed on the desktop image to check domain names.  If not, you can install '[dig](http://members.shaw.ca/nicholas.fong/dig/)' or 'nslookup' to check your domain names.

#### Advanced Domain Usage

The subdomain section can have one or more sections delimited by periods '.'   Typically you use one subdomain.biogenidec.com unless you have an application or set of applications that all work off of one server.  For example, you can set up a '***wildcard***' subdomain such that any sub-subdomain name XXXX (e.g. XXXX.cloud.biogenidec.com) gets directed to a single server that then manages directing the traffic to the correct sub-application.  This is how the cloud.biogenidec.com server is set up so you can create Virtual Servers from VM's and give them their own domain name - e.g. testserver1.cloud.biogeniec.com).
