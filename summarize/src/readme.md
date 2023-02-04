## - 1:make summary triples

### getting crawl quads/repo and sumarizing to endpoint, in [one callgraph *here*](call.md)
#### in the new [decoder staging](https://github.com/MBcode/dc), will reduce dependancy on fuseki, to get [this call graph](https://github.com/MBcode/dc/blob/main/call-summary.md)
#### prereq: [get](https://github.com/MBcode/ec/blob/master/crawl/get.md)/(& [soon](https://github.com/MBcode/ec/blob/master/summary.md) also [have](https://github.com/MBcode/ec/tree/master/crawl)) quads/repo to
### [summarize_repo.sh](https://github.com/MBcode/ec/blob/master/summary/summarize_repo.sh) runs:
#### [fnq.py](https://github.com/MBcode/ec/blob/master/summary/fnq.py) on a repo, to load the quads into repo namespace in fuseki
#### [tsum.py](https://github.com/MBcode/ec/blob/master/summary/tsum.py) for repo, to read that namespace and dump summary ttl triples
```mermaid
flowchart TD;
runX[runX w/loadable repo.nq files] -- fnq:load_to_repo_namespace --> F[fuseki_repo_namespace];
tsum[tsum: cache complex query as ttl] -- reads_repo_namesapce --> F;
tsum -- dump_ttl_triples --> T[repo_ttl];
```
  
  
  
## - 2:use for fast sparql on summary namespace
```mermaid
flowchart TD;
T[ttl per repo]  -- load --> B[blaze:summary namespace];
search[ui/nb] -- 1:query --> B -- 2:return_same_facets --> search;
```
  
## - also: get RDF from endpoint
### which gets rid of need for a duplicate cache
```mermaid
flowchart TD;
B[blaze] -- query_ret_facets_incl_g --> U[ui/nb]; 
U -- use_g_to_get_rdf --> B;
``` 



## - ps. metadata from crawl/s, [now easier to use](https://github.com/MBcode/ec/blob/master/system.md)
### [runX](https://github.com/gleanerio/gleaner/issues/126) 'quads' could come from gleaner or extruct crawls, as they are not coupled to outside systems now
