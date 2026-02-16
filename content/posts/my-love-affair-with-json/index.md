---
title: "My love affair with JSON"
date: 2018-01-30T18:58:18.297Z
categories: ["Medium Archive"]
---

---

![Photo by Glenn Carstens-Peters on Unsplash](1W5vbBi1Nah40KGMRIE1GJw_1.jpeg)
*Photo by Glenn Carstens-Peters on Unsplash*

### My love affair with JSON

For me, [JSON](https://www.json.org/) (JavaScript Object Notation) is a delightful data sharing/transfer format to use. It is simple to use and read. It is very fast to process. It is also subset of [YAML](http://yaml.org/) which is even easier to read.

I’ve evolved personal best practices to use for working with data for which JSON is central which I’ll share below. These best practices I’ve learned from others and personal experience in dealing with bioPharma data which while not generally very large is often quite heterogeneous and data formats are not very stable. I do not want to suggest that you use JSON for everything. For example, sometimes a binary format is required for performance reasons.

It serializes and deserializes incredibly fast for most languages which means it is easy and fast to send to another process, save to disk/file and retrieve. You can save a data object to disk as JSON and send that file to someone else using a different language and usually they have a library/package in their programming language of choice to easily deserialize it from the JSON data object into a data structure variable.

> Serialize means convert to a file on disk — e.g. dump a variable (data object, list or dictionary/hash) to disk from an application. Deserialize is the reverse, read a file into an application variable.

> A javascript object, python dictionary, perl hash or associative arrays are mostly the same concept though I’m stretching it a bit with the javascript object. Any array using a key, value format such as fruit\_colors[‘apple’] = ‘red’. Hereafter, I’m going to refer to this data structure as a hash.

### Best practice number 1 — JSON for all the things

Use JSON for sharing structured data between applications and data scientists whenever possible. In order to do this easily with the most versatility, always convert dates to strings before saving to JSON using ISO date formats. Instead of adding custom JSON formatters to my JSON packages to handle dates and other non-JSON simple formats (e.g. string, number, array, hash), I generally just convert to a string representation and convert it back from a string into a date when I deserialize it.

```
JSON hash and array example:
```

```
{  "key": "value",  "example_array": [    "one",    "two"  ]}
```

I generally serialize JSON into a datafile with indentation and linefeeds to make it easier to read but you don’t have to. You can make it all one line with no extra spaces or line feeds to make it smaller though I’ve found this generally has negligible effect as you always want to compress your JSON data when storing or transferring it to another server if it’s of any significant size. *For REST API servers transferring JSON, you always want to turn on* [*compression*](https://www.nginx.com/resources/admin-guide/compression-and-decompression/) *on the webserver.*

### Best practice number 2 — JSONSchema

Use [JSONSchema](http://json-schema.org/) to describe your dataset. Even if you are just using it for yourself, it helps you think about what you are storing and provides description attributes to make it easy to document your format. It is the best standard way to describe JSON data that you can easily share, and it’s usable by most programming language to validate your datasets.

Not every aspect of dataset validation can be captured in JSONSchema, some things you’ll need to put into code, but it can capture most aspects of a data structure definition.

> I will often structure my JSONSchema definitions to work with JSON array **and** JSONLines (explained below) formats — example [here](https://github.com/belbio/schemas/blob/master/schemas/nanopub_bel-1.0.0.yaml).

The [JSON Schema Store](http://schemastore.org/json/) is a great place to publish your JSONSchema files if you think it is of wider, public interest.

> I have started adding the url to the JSONSchema definition in my JSON data so I have a reference to the schema definition used for that data — especially if it is a longer-lived dataset that evolves.

### Best practice number 3 — YAML Yes

Use [YAML](http://yaml.org/) for JSONSchema definitions. Yes, YAML for JSONSchema definitions. Generally to validate JSON using JSONSchema you have to load/deserialize the JSONSchema definition file first into your application to validate so it doesn’t really matter what format you use. YAML allows comments (JSON doesn’t) and is easier to read for humans.

```
# You can have comments in the YAML file like thiskey: valueexample_array:  - one  - two
```

There is a nice python package called [json2yaml](https://github.com/drbild/json2yaml) that does a nice job of converting back and forth between JSON and YAML files *while maintaining the order of the hashes*. Keeping the natural order of the YAML/JSON is handy if you are using it for configuration or have a standard order for the data. Most JSON/YAML converters will sort the data in alphanumeric order. You do lose the YAML comments when converting back and forth though so I tend to use the YAML as the original source of truth and convert to JSON as needed.

I prefer to use YAML for human-readable, maintainable configuration files. One example of this pattern is using YAML to write the [BEL](http://bel.bio) Language Specification file and then converting it into an enhanced JSON file with additional sections programmatically-generated for convenience.

### Best practice number 4 — YAML No

Do not use YAML for performance-related tasks unless you’ve checked your YAML parser for performance. I didn’t realize the YAML parser was so slow in Python compared to JSON. In Python 3.4+, [JSON performs almost as fast as any of the built-in serialization formats (e.g. pickle)](https://stackoverflow.com/a/26860404/886938).

It takes about 150ms to read in the BEL Specification YAML file which is about 1000 lines long. It takes about 6ms to read in the enhanced JSON version of that file which is about 50% longer. YAML is a more complicated structure to parse than JSON, and it is also is not as popular so has less performance tuning.

So, YAML is really good to use where you are going to need lots of human interaction and editing and won’t cause a bottleneck because it has to be parsed over and over in a high throughput data pipeline.

### Best practice number 5 — JSONLines

[JSONLines](http://jsonlines.org/) is a great way to store smaller JSON data together into a single dataset when you want to reduce memory overhead for processing or be able to handle streaming data. The JSONLines concept is each line of your datafile is a separate JSON object as seen below.

```
JSONLines - each line below is a separate JSON object
```

```
{"key": "value1", "key2": "key2value"}{"key": "value2", "example_list": [1, 3]}[1, 5, 10]
```

I work with terms in terminology datasets (BEL Namespaces) that can have millions of entries. If I use a top-level array like the example below, I have to read all of those terms into memory in order to process them. Since I only need to work with one term at a time, I can use the JSONLines format to read a line at a time (which is a term at a time) and keep my memory overhead several million times lower.

```
JSON array of objects:
```

```
[  {    "key": "value1"  },  {    "key": "value2"  }]
```

If I have multiple types of data objects in a JSONLines file, I will add a top-level key to identify each type. An example is:

```
{"metadata": {"author": "William Hayes", "date": "20180101", ...}{"nanopub": {"id": 1, "citation": {...}, "assertions": {...} }{"nanopub": {"id": 2, "citation": {...}, "assertions": {...} }
```

Some tricks in dealing with JSONLines (\*.jsonl) files. I keep my larger JSONLines files gzipped and use a custom bash function based on:

```
gunzip -c $1 | jq . | more;
```

to gunzip to STDOUT, use [jq](https://stedolan.github.io/jq/) to format each line/JSON object using indentation/linefeeds and view it a page at a time. I’ve personally found gzip/gunzip to be a good balance in speed/compression. Bzip2 compresses better but is much slower. Your needs may vary from mine.

### Final thoughts

Thank you, thank you, thank you Douglas Crockford for specifying JSON and helping to make it the success it is today. I’ve suffered through CSV, ASN.1, SGML, XML, and custom data formats of various flavors and cannot fully express my love for JSON here. The many creators of JSON parsers for various languages, JSONSchema, YAML, etc have had a great impact on APIs, Data Science and Informatics that is not fully appreciated.
