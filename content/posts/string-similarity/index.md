---
title: "String Similarity"
date: 2012-07-17T11:53:00.001Z
tags: ["Literature Informatics"]
categories: ["Blogger Archive"]
series: ["Through the Haze"]
---

This post is my attempt at recording a very nice thread of [posts](https://lists.ccs.neu.edu/pipermail/bionlp/2012-July/002851.html) on [BioNLP.org](http://bionlp.org)'s mailing list on string similarity measures. Harsha G at Molecular Connections asked about string similarity measures which prompted

## Tools recommended:

- [Simmetrics](http://sourceforge.net/projects/simmetrics/)
- [Simstring](http://www.chokkan.org/software/simstring/)
- [secondstring](http://secondstring.sourceforge.net/)
- [automaton](http://www.brics.dk/automaton/)
- [Python NGRAM](http://packages.python.org/ngram/index.html)
- [AGREP](http://www.tgries.de/agrep/)
- [RE2](http://code.google.com/p/re2/)
- [TRE](http://laurikari.net/tre/)
- [FREJ](http://frej.sourceforge.net/)

## Papers:

- <http://dx.doi.org/10.1093/bioinformatics/btm393> - papers by Okazaki and others on string similarity metrics (shared by Sampo)
- <http://dc-pubs.dbs.uni-leipzig.de/files/Cohen2003Acomparisonofstringdistance.pdf>
- [Pubmed Distance paper - Lu 2009](http://www.ncbi.nlm.nih.gov/pubmed/19162232)
- [Névéol - 2010](http://www.ncbi.nlm.nih.gov/pubmed/21347036) - Author Keywords in Biomedical Journal Articles
- **<http://aclweb.org/anthology-new/D/D08/D08-1113.pdf>**
- **<http://lingpipe-blog.com/2010/04/27/mccallum-bellare-and-pereira-2005-a-conditional-random-field-for-discriminatively-traied-finite-state-string-edit-distance/>**

## Responses:

### From Tudor Groza:

> ```
> Dear Harsha,
>
> I would suggest you have a look at Simmetrics [1] - it is a comprehensive
> package for string similarities ranging from basic ones, like Levenshtein
> distance to more advanced one, like Smith-Waterman or Needleman-Wunch. You
> can find the Java API at [2] - for some reasons the original page is
> missing, hence the only way to get to it is via the Web archive.
>
> Hope that this helps.
>
> [1] http://sourceforge.net/projects/simmetrics/
> [2]
> http://web.archive.org/web/20081225104938/http://www.dcs.shef.ac.uk/~sam/simmetrics/index.html
>
> Kind regards,
> Tudor
> ```

### From Sampo Pyysalo:

> ```
> Dear Harsha, all,
>
> Not sure what your exact needs are, but I've found that in
> approximate-matching lookup against many larger biomedical resources it's
> good to do a fast, comparatively simple first-pass lookup before running
> more advanced string comparison algorithms to avoid the computational costs
> of full comparison for a large number of string pairs. I've found Naoaki
> Okazaki's simstring (http://www.chokkan.org/software/simstring/) to be
> excellent for this first task. The way I'd recommend to use this is to
> first filter a large string collection to a reasonably-sized set of best
> matches (in terms of a comparatively coarse similarity function like char
> n-gram cosine) with simstring and then run more advanced stuff like
> custom-cost edit distance for this smaller set.
>
> There are a number of studies by Okazaki as well as Yoshimasa Tsuruoka and
> others on the topic of string similarity metrics for domain tasks that may
> also be of interest to you, e.g.
> http://dx.doi.org/10.1093/bioinformatics/btm393
>
> Cheers,
>
> Sampo
> ```

### From Florian Leitner:

> ```
> Dear Harsha,
>
> A good overview is the 2003 W. Cohen paper "promoting" the SoftTFIDF measure and with a very good overview of available similarity measures:
>
> http://dc-pubs.dbs.uni-leipzig.de/files/Cohen2003Acomparisonofstringdistance.pdf
>
> As for libraries to do string similarity matching, there are many, many options available. As they have not been mentioned so far, most prominently, there are the Regular Expression libraries.
>
> -- REGEX
> In terms of pure speed, some of Google's own searches are powered by re2 (developed by a Google search engineer), a deterministic RegEx ("DFA")  engine that is significantly faster than the "default" engines available in most other programming languages (because they are all are at least in parts non-deterministic, i.e., "NFAs"). However, due to the pure deterministic nature there is quite some default functionality missing (e.g., lookaheads and -behinds, etc.), so you have to define all variants you wish to match in your patterns (no approximate matches!), while it is blazingly fast:
>
> http://code.google.com/p/re2/
>
> In terms of pure approximate matching speed, don't forget that *nix offers a pretty powerful approximate string matching implementation right at your "fingertips":
>
> http://www.tgries.de/agrep/
>
> Last, another C implementation of a POSIX compliant approximate (DFA-based) regex matcher is TRE, although this is library is therefore somewhat slower than the RE2 engine, too:
>
> http://laurikari.net/tre/
>
> These three regex libraries are probably the most noteworthy if you need raw speed. Then there are a few Java regex libraries that seem noteworthy, too:
>
> First, there is a non-determinisitc RegEx engine (FREJ) to do approximate matching, also in Java:
>
> http://frej.sourceforge.net/
>
> And yet another Java regex implementation, partially DFA and partially NFA, is the Brics Automaton:
>
> http://www.brics.dk/automaton/
>
> (there are much more Java regex libraries, but let Google be your best friend if you need even more pointers...)
>
> -- DISTANCE
> Apart from the regex/D- or NFA based implementations, there are distance-based measures to do approx. string matching. A very fast similarity search tool is SimString, an approximate matcher based on distance measures, and already mentioned by Sampo in his post, in C++:
>
> http://www.chokkan.org/software/simstring/
>
> Probably the most well-known package in this domain is the SecondString package from the CMU (from W. Cohen, the author cited above) for approx. string matching in Java, also based on edit distance measures:
>
> http://secondstring.sourceforge.net/
>
> Last I'd mention there is a simple Python module to calculate n-gram-based similarities; while I do love Python very much, alone due to that fact that this is Python-based, it will most likely be the slowest option listed here:
>
> http://packages.python.org/ngram/index.html
>
> Hope this helps to get you up to [matching] speed!
>
> Cheers,
> Florian
> ```

### From **Aurélie Névéol:**

> ```
> Harsha,
>
> Another measure to look into is the "PubMed distance" described in this paper:
>
> Lu Z, Wilbur WJ. Improving accuracy for identifying related PubMed queries by an integrated approach. J Biomed Inform. 2009 Oct;42(5):831-8.
>
> An example of use and evaluation can be found in this other paper:
>
> Névéol A, Islamaj-Doğan R, Lu Z. Author Keywords in Biomedical Journal Articles. Proc AMIA Annu Symp. 2010:537-41.
>
> Best regards,
>
> Aurelie
> ```

### **From Bob Carpenter:**

> **I'd suggest looking further than Jaccard distance in  
> the LingPipe matchers.  We have TF/IDF matchers based  
> on character n-grams that are widely used in practice (not  
> just by us or with our implementation;  note  
> that this is NOT the same as Cohen et al.'s soft TF/IDF,  
> which I've never fully understood).  
>   
> There's also the Jaro-Winkler matchers, which are  
> tuned for matching single-word names.  
>   
> LingPipe also has a dictionary-based matcher that will  
> spot approximate matches (by weighted edit distance) in  
> text using the Aho-Corasick algorithm for deterministic  
> matching and suffix arrays for speeding approximate matching.  
>   
> And you can also use something like an HMM- or CRF-based  
> chunker to find matches in texts.  It basically then looks  
> like a named-entity problem.  
>   
> If you want something fancier that should outperform any of  
> these methods, check out this paper by McCallum, Bellare and Pereira:  
>   
>   
> <http://lingpipe-blog.com/2010/04/27/mccallum-bellare-and-pereira-2005-a-conditional-random-field-for-discriminatively-traied-finite-state-string-edit-distance/>  
>   
> I'm also quite keen on this method for string comparison  
> by Dreyer, Eisner and Smith, though I haven't tried it, either:  
>   
>   <http://aclweb.org/anthology-new/D/D08/D08-1113.pdf>  
>   
> And in the end, you may be wanting to do something like cluster  
> similar terms rather than just provide pairwise similarities.  
> Andrew McCallum and crew have done some great work on this problem,  
> and there's a huge swath of "deduplication" and "record linkage"  
> literature that's related.**
