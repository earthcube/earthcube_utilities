# Summarize

## Overview

Steps:
1. Insure that a gleaner crawl has already been done, and you have the location of it's buck
2. run> repo2summary.sh repo

where repo is the name of a repo directory in that crawl's bucket

[What it calls](https://github.com/earthcube/ec/blob/master/summary/call.md):

It will call 'fix_runX.sh repo' to get all the rdf and convert it to quads

then it will call 'summarize_repo.sh repo' to put it in fuseki so it can be queried and summarized

producing a: repo.ttl file that can be loaded into the blazegraph summary namespace of your choice

## Example

LD> repo2summary.sh earthchem

will run over:earthchem
not IN_COLAB
rdf_inited,rdflib_inited,sparql_inited=True,True,True
will get files for earthchem in a dir named after it
will create the earthchem dir
cd to: cwd=/var/www/html/LD/earthchem to get the repo=earthchem to downloads files into
will wget:https://oss.geocodes.ncsa.illinois.edu/gleaner/milled/earthchem/00b0ad684052b7674832f1dff8e537dbcffcbb84.rdf
will wget:https://oss.geocodes.ncsa.illinois.edu/gleaner/milled/earthchem/00e34d1f624300099a0f72b3a33444ee4e970019.rdf
will wget:https://oss.geocodes.ncsa.illinois.edu/gleaner/milled/earthchem/01272511a24c726c45cf9f6d2804543b081a685a.rdf
will wget:https://oss.geocodes.ncsa.illinois.edu/gleaner/milled/earthchem/017e6dd8b16d4e102f0f3d85c3d7deedc0b23fea.rdf
will wget:https://oss.geocodes.ncsa.illinois.edu/gleaner/milled/earthchem/02b76c2c64934dfd54c16925510a1d4823185496.rdf
will wget:https://oss.geocodes.ncsa.illinois.edu/gleaner/milled/earthchem/037ee404dae1fbf42b491a7856b2d20fbd6b983b.rdf
...

will wget:https://oss.geocodes.ncsa.illinois.edu/gleaner/milled/earthchem/fec94d837fe1c0c2f255e0ffd49a1e704c72bd16.rdf
will wget:https://oss.geocodes.ncsa.illinois.edu/gleaner/milled/earthchem/fee66304ce6dc4b36bb02294262f04033b3e6e17.rdf
will wget:https://oss.geocodes.ncsa.illinois.edu/gleaner/milled/earthchem/ff277f4a4042a542fd443c8bde936cfe8a6a4de3.rdf
will run over:earthchem
found:640 files
['a37ce54862443b2fb1e62c91c9fb59ab2f8b3e24.rdf', 'e81b92cc8f1787f7d770ad4230658bb00b4ced50.rdf', '35c3d84f9cb38cb560fd7282860bcedc57ba78a2.rdf', '26baf57de16e4ecbe9daae4f16609ea0fe1da3f8.rdf', 
...
 '4bc9b6764dfbc9cbfe4386b0ee24a548f4b7b240.rdf', '69368abc14ed22a2b1eee380df7ce560031b5021.rdf', '3cdd4212b1d865c63ca6f4d1ab61f79e0d31732c.rdf', '3e6dadf0c1023922c0e791ec296c3c1e8628da7a.rdf', 'cbb4289de24fad2906a8e9164c7b0382619652d0.rdf']
found:639 rdf files
2nq,gives:earthchem/a37ce54862443b2fb1e62c91c9fb59ab2f8b3e24.nq
2nq,gives:earthchem/e81b92cc8f1787f7d770ad4230658bb00b4ced50.nq
2nq,gives:earthchem/35c3d84f9cb38cb560fd7282860bcedc57ba78a2.nq

...

2nq,gives:earthchem/3e6dadf0c1023922c0e791ec296c3c1e8628da7a.nq
2nq,gives:earthchem/cbb4289de24fad2906a8e9164c7b0382619652d0.nq
out-filename=earthchem.nq
created
try:http://localhost:3030/earthchem/sparql
ps:['mbobak', '736052', '1', '1', '13:08', 'pts/4', '00:00:06', '/usr/lib/jvm/default-java/bin/java', '-Xmx4G', '-Dlog4j.configurationFile=/home/mbobak/dwn/ai/sw/db/jena/apache-jena-fuseki-4.6.1/log4j2.properties', '-cp', '/home/mbobak/dwn/ai/sw/db/jena/apache-jena-fuseki-4.6.1/fuseki-server.jar', 'org.apache.jena.fuseki.cmd.FusekiCmd', '--file', 'iris.nq', '/iris\n']
pid:736052
will kill server, from:736052
kill -9 736052
will start fuseki-server, for:earthchem
13:16:31 INFO  Server          :: Dataset: in-memory: load file: earthchem.nq
13:16:36 INFO  Server          :: Running in read-only mode for /earthchem
13:16:36 INFO  Server          :: Apache Jena Fuseki 4.6.1
13:16:36 INFO  Config          :: FUSEKI_HOME=/home/mbobak/dwn/ai/sw/db/jena/apache-jena-fuseki-4.6.1
13:16:36 INFO  Config          :: FUSEKI_BASE=/home/mbobak/mb/w2/n/ec/ext/org/LD/run
13:16:36 INFO  Config          :: Shiro file: file:///home/mbobak/mb/w2/n/ec/ext/org/LD/run/shiro.ini
13:16:37 INFO  Server          :: Database: in-memory, with files loaded
13:16:37 INFO  Server          :: Path = /earthchem
13:16:37 INFO  Server          :: System
13:16:37 INFO  Server          ::   Memory: 4.0 GiB
13:16:37 INFO  Server          ::   Java:   17.0.5
13:16:37 INFO  Server          ::   OS:     Linux 5.4.0-131-generic amd64
13:16:37 INFO  Server          ::   PID:    740468
13:16:37 INFO  Server          :: Started 2023/02/03 13:16:37 CST on port 3030
13:16:41 INFO  Fuseki          :: [1] GET http://localhost:3030/earthchem/sparql?format=json&query=prefix+schema%3A+%3Chttps%3A%2F%2Fschema.org%2F%3E%0ASELECT+distinct+%3Fsubj+%3Fg+%3FresourceType+%3Fname+%3Fdescription++%3Fpubname%0A++++++++%28GROUP_CONCAT%28DISTINCT+%3Fplacename%3B+SEPARATOR%3D%22%2C+%22%29+AS+%3Fplacenames%29%0A++++++++%28GROUP_CONCAT%28DISTINCT+%3Fkwu%3B+SEPARATOR%3D%22%2C+%22%29+AS+%3Fkw%29+%3Fdatep+%0A++++++++%23%28GROUP_CONCAT%28DISTINCT+%3Furl%3B+SEPARATOR%3D%22%2C+%22%29+AS+%3Fdisurl%29%0A++++++++WHERE+%7B%0A++++++++++graph+%3Fg+%7B%0A+++++++++++++%3Fsubj+schema%3Aname+%3Fname+.%0A+++++++++++++%3Fsubj+schema%3Adescription+%3Fdescription+.%0A++++++++++++Minus+%7B%3Fsubj+a+schema%3AResearchProject+%7D+.%0A++++++++++++Minus+%7B%3Fsubj+a+schema%3APerson+%7D+.%0A%23BIND+%28IF+%28exists+%7B%3Fsubj+a+schema%3ADataset+.%7D+%7C%7Cexists%7B%3Fsubj+a+schema%3ADataCatalog+.%7D+%2C+%22data%22%2C+%22tool%22%29+AS+%3FresourceType%29.%0A+++++++++++++++++++%3Fsubj+a+%3FresourceType+.%0A++++++++++++optional+%7B%3Fsubj+schema%3Adistribution%2Fschema%3Aurl%7Cschema%3AsubjectOf%2Fschema%3Aurl+%3Furl+.%7D%0A++++++++++++OPTIONAL+%7B%3Fsubj+schema%3AdatePublished+%3Fdate_p+.%7D%0A++++++++++++OPTIONAL+%7B%3Fsubj+schema%3Apublisher%2Fschema%3Aname%7Cschema%3AsdPublisher%7Cschema%3Aprovider%2Fschema%3Aname+%3Fpub_name+.%7D%0A++++++++%23+++OPTIONAL+%7B%3Fsubj+schema%3AspatialCoverage%2Fschema%3Aname+%3Fplace_name+.%7D%0A++++++++++++OPTIONAL+%7B%3Fsubj+%0A++++++++schema%3AspatialCoverage%2Fschema%3Aname%7Cschema%3AspatialCoverage%2Fschema%3AadditionalProperty%2Fschema%3Aname+%3Fplace_name+.%7D%0A++++++++++++OPTIONAL+%7B%3Fsubj+schema%3Akeywords+%3Fkwu+.%7D%0A++++++++++++BIND+%28+IF+%28+BOUND%28%3Fdate_p%29%2C+%3Fdate_p%2C+%22No+datePublished%22%29+as+%3Fdatep+%29+.%0A++++++++++++BIND+%28+IF+%28+BOUND%28%3Fpub_name%29%2C+%3Fpub_name%2C+%22No+Publisher%22%29+as+%3Fpubname+%29+.%0A++++++++++++BIND+%28+IF+%28+BOUND%28%3Fplace_name%29%2C+%3Fplace_name%2C+%22No+spatialCoverage%22%29+as+%3Fplacename+%29+.%0A+++++++++++++%7D%0A++++++++%7D%0A++++++++%23GROUP+BY+%3Fsubj+%3Fpubname+%3Fplacenames+%3Fkw+%3Fdatep+++%3Fname+%3Fdescription++%3FresourceType+%3Fg++%0A++++++++GROUP+BY+%3Fsubj+%3Fg+%3FresourceType+%3Fname+%3Fdescription++%3Fpubname+%3Fplacenames+%3Fkw+%3Fdatep%0A
13:16:41 INFO  Fuseki          :: [1] Query = prefix schema: <https://schema.org/> SELECT distinct ?subj ?g ?resourceType ?name ?description  ?pubname         (GROUP_CONCAT(DISTINCT ?placename; SEPARATOR=", ") AS ?placenames)         (GROUP_CONCAT(DISTINCT ?kwu; SEPARATOR=", ") AS ?kw) ?datep          #(GROUP_CONCAT(DISTINCT ?url; SEPARATOR=", ") AS ?disurl)         WHERE {           graph ?g {              ?subj schema:name ?name .              ?subj schema:description ?description .             Minus {?subj a schema:ResearchProject } .             Minus {?subj a schema:Person } . #BIND (IF (exists {?subj a schema:Dataset .} ||exists{?subj a schema:DataCatalog .} , "data", "tool") AS ?resourceType).                    ?subj a ?resourceType .             optional {?subj schema:distribution/schema:url|schema:subjectOf/schema:url ?url .}             OPTIONAL {?subj schema:datePublished ?date_p .}             OPTIONAL {?subj schema:publisher/schema:name|schema:sdPublisher|schema:provider/schema:name ?pub_name .}         #   OPTIONAL {?subj schema:spatialCoverage/schema:name ?place_name .}             OPTIONAL {?subj          schema:spatialCoverage/schema:name|schema:spatialCoverage/schema:additionalProperty/schema:name ?place_name .}             OPTIONAL {?subj schema:keywords ?kwu .}             BIND ( IF ( BOUND(?date_p), ?date_p, "No datePublished") as ?datep ) .             BIND ( IF ( BOUND(?pub_name), ?pub_name, "No Publisher") as ?pubname ) .             BIND ( IF ( BOUND(?place_name), ?place_name, "No spatialCoverage") as ?placename ) .              }         }         #GROUP BY ?subj ?pubname ?placenames ?kw ?datep   ?name ?description  ?resourceType ?g           GROUP BY ?subj ?g ?resourceType ?name ?description  ?pubname ?placenames ?kw ?datep 
13:16:42 INFO  Fuseki          :: [1] 200 OK (1.034 s)
Îœ<495 f3geocodes: /org/LD> 

Îœ<60 f3geocodes: /org/LD> wc earthchem.*
  331126  1722821 46595935 earthchem.nq   ;use nabu to load this if you want, from minio ; or check/fix and load from here
    5756    78778   649470 earthchem.ttl  ;=now to load this to the summary namespace of your choice

load via dashboard, or I'll have a ttl2blaze.sh

## Details
