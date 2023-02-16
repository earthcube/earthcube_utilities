# Summarize

## Overview
(what does this do?) eg. 
Summarize creates a 'normalized view' of a repositories JSONLD as quads to improve
performance a searches for geocodes. It basically flattens the JSONLD arrays into strings.

To do this, it reads the triples that nabu generates as part of it's workflow, then 
converts them  'summary' graph namespace.
A more detailed overview is in [Summarize](docs/summarize.md)

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
* Run steps below

## Steps: 
 
1. if you have not, change to the summarize directory: `cd  earthcube_utilities/summarize`
2. Insure that a gleaner crawl has already been done, and you have the location of it's bucket

once gleaner has been run it should have a gleaner/summoned path full of repos you can summarize

3. run> `src/summarize_repo.py repo nabufile`
> where repo is the name of a repo directory in that crawl's bucket and nabufile is the path to the nabu configuration file
> this assumes that glcon is at ~/indexing/glcon. If it is not, then pass --glcon with path to glcon

In the console you should see nabu run. 

!!! note 
    need to update logging so that some output is generated.

## Example

```shell
geocodes: src/summarize_repo.py iris ../resources/testing/nabu --glcon

version:  v3.0.8-ec
Using nabu config file: nabu_iris
nabu prefix called
 100% |██████████████████████████████████████████████| (49/49, 4 it/s)

Process finished with exit code 0

```

files will be generated. All files are ok to delete.
* `{repo}.ttl` - the turtle file of the repository used to load the data to summary
* `nanu_{repo}` the config that was used to load the summary namespace
* `logs/gleaner-date.log`  
* `gleaner.db`  artifact from glcon


got to  the sparql endpoint in the nabu file, and 
```sparql
SELECT * { ?s ?p ?o } LIMIT 1
```

