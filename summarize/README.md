# Summarize

## Overview
Because of the lack of standardardization on how Science on Schema is implemented, there are performance issues
quering and retrieving information from the blazegraph graphstore. Because JSONLD fields can be strings/objects/arrays
asking the graphstore to guess the best optimization for retrieval is haphazard.
In order to work around this, we create a materilized view view. Materialization is common performance trick
which basically brings all values into a single object so that retreival of what would be normalized
information is flattened.  The JSONLD strings/objects/arrays single object to improve search and retrieval performance. 

**Summarize tool** creates this 'materilized view' of a repositories JSONLD as triple to improve
performance a searches for geocodes. 

To do this, it reads the quads that nabu generates as part of it's workflow, then 
converts them into flattend triples in  'summary' graph namespace.
A more detailed overview workflow is in [Summarize v2](./v2_proposal.md)

More details are in the [documentation diretory](docs/), 
or at the [geocodes documentation site](https://earthcube.github.io/geocodes_documentation/)

## Dependencies
* Geocodes Stack
* glcon
* python > 3.3
* the nabu configuration file that was used to load the data to the graphstore

## INSTALL

* pull repository,
    * `git clone https://github.com/earthcube/earthcube_utilities.git`
* `cd earthcube_utilities/summarize`
* install python dependencies
    * `pip3 install requirements.txt`
* Run steps below

## Two Approaches
* Summarize existing graph stores. AKA: data is loaded into a graph
* summarize as part of workflow, aka build summary when repo is loaded

### summarize a loaded repository
1. if you have not, changed to the summarize directory: `cd  earthcube_utilities/summarize`
2. Insure that a `glcon gleaner batch --cfgName` crawl and loading to the graphstore using has already been done,
nabu has already been done.  

repo is optional. San repo will summarize all information
```shell
geocodes: src/summarize_from_graph_namespace.py --repo iris --graphendpoint {endppiont} --summary_namespace {earthcube_summary}

```


