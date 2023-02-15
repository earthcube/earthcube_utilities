# Proposal for v2 summary

## v1
this is what summary version on has implemented. The first three steps duplicate what nabu does, 

* get_repo: read s3 stored triples from gleaner, write files
* fnq: start stop fuseki, and create a temporary namespace
* rdf2nq: convert triples to quads write to a local (fuseki) graph namespace
* tsum:
   * query namespace to get all records insert into a dataframe
   * for each record in dataframe, 
      * convert to a summary set of triples
      * write to a file

## v2

### Questions
* nabu converts to quads
  * does this work (**dv, yes**): `nabu prefix --cfg {path to nabu config} --prefix milled/{repo}` 
     * probably need to add a --namespace and/or --graphurl 
       * these are convince effort, and not a blocker on use. 
  * are these quads usable to create summaries (**dv, yes, tsum dev branch can generate summaries**)
     * Can we just use nabu/glcon nabu **DV, I say yes**
* can we just create a temporary namespace in blazegraph?
    * **yes there is an rest api to create and delete a nsamspace**. Coding up a class to do it. 
    * just use rdflib. 


### Dependencies
* stack
  * s3
  * blazegraph
* glcon/nabu
* python

### Workflow
**curl and wget are not standard packages in the base docker images. Use python requests.**

#### summarize a python script to call the methods needed.
* parameters  for 
   * nabu_cfg. glcon generates a gleaner and a nabu file. where is this nabu file.
   * repo name
   * (override) graphendpoint
   * (override) path to glcon
   * (override) output=filename
   * (future) graphsummary if true, upload summary triples to summary_namespace
      * (opt) summary_namespace (default: {repo}summary)
   * (later) upload to s3
* **workflow**
   * see if nabu_cfg exists, get sparql.endpoint from file
   * create temp_namespace
   * run nabu to make quads into temp namespace
   * run tsum_v2 to create summary triples
   * if uploadSummary, use python requests to upload summary


**details**
Suggested Classes/object whatever we think they should be called
* (sn)summarize_namspace.py -- class to read configs, call summary code
* (ec) ec_summarize.py
   * uses (mg) manageGraph.py and other libraries

1. (sn)cli to read parameters
2. (sn)read sparql.endpoint from nabu file (unless overriden by graphendpoint )
```minio:
    address: oss.geocodes.ncsa.illinois.edu
    port: 443
    ssl: true
    accesskey: worldsbestaccesskey
    secretkey: worldsbestsecretkey
    bucket: gleaner
objects:
    bucket: gleaner
    domain: us-east-1
    prefix:
        - summoned/iris
        - org
    prefixoff: []
sparql:
    endpoint: https://graph.geocodes.ncsa.illinois.edu/blazegraph/namespace/iris_nabu/sparql
    authenticate: false
    username: ""
    password: ""
```
4. (sn->mg)python request to create a temp_repo namespaces in a blazegraph ((tns)temp_repo, (sns)repo_summary)
5. (sn)Quads/Nabu step (future:  nabu can write out a file. It now can, but no binaries done yet )
    * modify nabu file with a correct sparql.endpoint
    * run nabu for repository: `glcon nabu prefix --cfg {nabu_cfg} --prefix summonned/{repo}` 
* (sn -> ec) run tsum
* (ec) write out to file, or whatever
* (sn ->mg(sns) ) upload to (sns)repo_summary with a python script. read file a binary, insert
* (sn->mg(tns))  python request to delete temp namespace

##### tsum, or tsumv2 steps to make graph using rdflib.
ideas on how to improve the summary generate to make less use of print, and more use of a 
library to generate triples/quad, etc

    1. create an rdflib graph
```python
from rdflib import Graph

g = Graph()
```

    2. read all graphs identifiers from temp_repo
       1. for each graph, g
           1. create rdf triples using rdflib, 

```python
from rdflib import URIRef, BNode, Literal
from rdflib import Namespace

n = Namespace("https://schema.org/")
tripleuri = URIRef(g)
title = Literal({title})  # passing a string
g.add((tripleuri, n.title, title))
## repeat for other summary triples
```
    3. add tripe to graph
    4. every (100/1000) save graph to file.
    5. serialize
```python
g.serialize(format="nquads", destination="{repo}.ttl")
```
    6. write to std.out, 