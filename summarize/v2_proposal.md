# Proposal for v2 summary

## v1
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
  * does this work: `nabu prefix --cfg {path to nabu config} --prefix milled/{repo}` 
     * probably need to add a --namespace and/or --graphurl 
  * are these quads usable to create summaries
  * Can we just use nabu/glcon nabu
* can we just create a temporary namespace in blazegraph?
    * just use rdflib


### Dependencies
* stack
  * s3
  * blazegraph
* glcon/nabu
* python

### Workflow
1. parameters
  * repo name
  * nabu config
  * endpoint(s)
  * output file|graphsummary
3. python request to create a temp_repo namespaces in a blazegraph (temp_repo, repo_summary)
4. run nabu for repository
   * reads from s3, writes to temp_repo namespace
5. create an rdflib graph
```python
from rdflib import Graph

g = Graph()
```
6. read all graphs identifiers from temp_repo
7. for each graph, g
    1. create rdf triples using rdflib, 
```python
from rdflib import URIRef, BNode, Literal
from rdflib import Namespace

n = Namespace("https://schema.org/")
tripleuri = URIRef(g)
title = Literal({title})  # passing a string
g.add((tripleuri, n.title, title))
```
    2. add to graph
    3. every (100/1000) save graph to file.
8. serialize
```python
g.serialize(format="nquads", destination="{repo}.ttl")
```
9. write to std.out, 