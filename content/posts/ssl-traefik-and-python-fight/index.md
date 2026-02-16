---
title: "SSL, Traefik, and Python — Fight!"
date: 2020-04-10T17:57:18.875Z
categories: ["Medium Archive"]
---

---

![Photo by Attentie Attentie on Unsplash](image.jpg)
*Photo by Attentie Attentie on Unsplash*

I had some fun trying to get SSL working correctly on my Website and API endpoints so that python [*requests*](https://requests.readthedocs.io/en/master/) and [*httpx*](https://github.com/encode/httpx) libraries wouldn’t error out due to SSL (https) access failures.

First off, I love [Traefik](https://containo.us/traefik/). It works incredibly well as your reverse proxy for docker containers. Simply, if you want your docker services to be exposed as `https://fantasticthing.example.com` instead of `http://145.38.28.2:8000,` Traefik is your BestFriendForever. Less simply — not even going to start :)

### Round 1

For a particular application, I had to use a provided wildcard SSL certificate.

#### Traefik docker-compose partial example

Apologies for using Traefik 1.7 in my example when they are up to Traefik 2.2 (with a lot of nice new features)

Browsers accessed and validated the SSL endpoint fine. Python scripts using *requests* or *httpx* were a different story. I got the following error trying to do a requests GET against one of the API endpoints:

```
requests.exceptions.SSLError: HTTPSConnectionPool(host='nanopubstore.tib.aws.precisionformedicine.com', port=443): Max retries exceeded with url: /nanopubs/update_validation?email=whayes%40biodati.com (Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1056)')))
```

Further research indicated that since the Root Certificate Authority (CA) wasn’t in the [*certifi*](https://pypi.org/project/certifi/) package, *requests* couldn’t validate the SSL certificate. You can check what Root CA’s are included in *certifi* as it automatically updates from the [Mozilla CA Certificate Store](https://www.mozilla.org/en-US/about/governance/policies/security-group/certs/). The *certifi* package was created to make it easier to work with SSL endpoints using python. You can, of course, turn off SSL verification but that is not recommended, e.g. `requests.get(url, verify=False)` . If you do, you’ll get a lot of warnings about how you are using an untrusted SSL endpoint.

### Round 2

We got an updated wildcard cert from a Root CA in the Mozilla CA Certificate Store. The web browsers, Chrome, Edge, Firefox, etc are all accessing the website with no issues. Everything is great now — except it’s not. My python script is still reporting an error with the SSL validation.

> I forgot to add the intermediates certificates to build the full trust chain between the wildcard certificate for my website and the Root CA. You can go [here](https://support.dnsimple.com/articles/what-is-ssl-certificate-chain/) to learn more about the full trust chain.

### Round 3

I changed the files I used in line 17 of the Traefik docker-compose example above so that instead of using the `wildcard_example_com.crt` and `wildcard_example_com.key` files which hold the SSL certificate and the Private Key file used in the SSL request process — I combined them all into a [PEM](https://support.quovadisglobal.com/kb/a37/what-is-pem-format.aspx) file. You combine them together using the instructions [here](https://www.digicert.com/kb/ssl-support/pem-ssl-creation.htm).

The PEM file creation basically says to copy/paste the SSL components together like so:

> **— — BEGIN RSA PRIVATE KEY — —   
> (Your Private Key: your\_domain\_name.key)  
>  — — END RSA PRIVATE KEY — —**   
> **— — BEGIN CERTIFICATE — —   
> (Your Primary SSL certificate: your\_domain\_name.crt)  
>  — — END CERTIFICATE — —**   
> **— — BEGIN CERTIFICATE — —   
> (Your Intermediate certificate: DigiCertCA.crt)  
>  — — END CERTIFICATE — —**   
> **— — BEGIN CERTIFICATE — —   
> (Your Root certificate: TrustedRoot.crt)  
>  — — END CERTIFICATE — —**

The main thing to know about the PEM format is that you can combine the key file, your website certificate and the intermediate chain certificates all in one file and Traefik will read it. You still need to add the cert file and key file in the Traefik configuration from what I can tell, but you use the same file for each. You can replace line 17 in the docker-compose file example above with:

```
- --entryPoints=Name:https Address::443 TLS:/certs/wildcard_example_com.pem,/certs/wildcard_example_com.pem
```

Now the python scripts validate SSL correctly using *requests* and other HTTP clients that validate SSL using the *certifi* package.

No doubt I’ll be referring back to this in a year or so when I have to do this again. Hopefully, if you find this article when you are trying to figure out why you can’t get python to work with your SSL endpoint, it will help you as well.
