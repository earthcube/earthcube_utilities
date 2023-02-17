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

(need to add more on flattening.)

## Dependencies
* Geocodes Stack
* glcon
* python > 3.3
* the nabu configuration file that was used to load the data

## INSTALL

* pull repository,
    * `git clone https://github.com/earthcube/earthcube_utilities.git`
* `cd earthcube_utilities/summarize`
* install python dependencies
    * `pip3 install requirements.txt`
* Run steps below

## Steps: 
 
1. if you have not, change to the summarize directory: `cd  earthcube_utilities/summarize`
2. Insure that a `glcon gleaner batch --cfgName` crawl has already been done, 
and you have the location of it's bucket once gleaner has been run it should have a
 gleaner/summoned path full of repos you can summarize
5. run> `src/summarize_repo.py repo nabufile`
> where repo is the name of a repo directory in that crawl's bucket and nabufile is the path to the nabu configuration file
> this assumes that glcon is at ~/indexing/glcon. If it is not, then pass --glcon with path to glcon

??? note "Help"
    Warning, may not be all implemented.
    ```shell
    
    src/summarize_repo.py --help
    usage: summarize_repo.py [-h] [--graphendpoint GRAPHENDPOINT] [--glcon GLCON] [--graphsummary GRAPHSUMMARY] [--summary_namespace SUMMARY_NAMESPACE] repo nabufile
    
    positional arguments:
      repo                  repository name
      nabufile              nabu configuration file
    
    optional arguments:
      -h, --help            show this help message and exit
      --graphendpoint GRAPHENDPOINT
                            override nabu endpoint
      --glcon GLCON         override path to glcon
      --graphsummary GRAPHSUMMARY
                            upload triples to graphsummary
      --summary_namespace SUMMARY_NAMESPACE
                            summary_namespace

    ```

In the console you should see nabu run. 


## Example

```shell
geocodes: src/summarize_repo.py iris ../resources/testing/nabu --glcon

version:  v3.0.8-ec
Using nabu config file: nabu_iris
nabu prefix called
 100% |██████████████████████████████████████████████| (49/49, 4 it/s)

Process finished with exit code 0

```
!!! note 
    need to update logging so that some output is generated.

files will be generated. All files are ok to delete.

* `{repo}.ttl` - the turtle file of the repository used to load the data to summary
* `nanu_{repo}` the config that was used to load the summary namespace
* `logs/gleaner-date.log`  
* `gleaner.db`  artifact from glcon


## Check the data load
Go to  the sparql endpoint in the nabu file, use the "{repo}_summary" 
eg `https://graph.earthcube.org/blazegraph/`

If anything was loaded
```sparql
SELECT * { ?s ?p ?o } LIMIT 1
```

and how many actual 'Datasets' were loaded:
```sparql
SELECT (count(?g ) as ?count) 
WHERE     {     GRAPH ?g {?s a <https://schema.org/Dataset>}}
```

