## what you call to run summarization

#### from getting (gleaner) crawler's quad/repo  through making the summary triples, and loading them

```mermaid
flowchart TD;
R2S[repo_to_summary.sh]  -- calls --> G[1: fix_runX.sh];
G -- calls --> gr[1:get_repo.py]
G -- calls --> r2n[2:run2nq.py] -- loads --> rdf2[rdf2nq.py];
R2S -- calls --> SR[2: summarize_repo.sh];
SR -- calls --> F1[1: fnq.py];
SR -- calls --> F2[2: tsum.py] -- produces --> RT(repo.ttl) -- ttl2blaze.sh --> B[blazegraph];
r2n -- produces --> nq(repo.nq) -- into_fuseki --> F1;
```

#### there is a simplification of this, that would skip a server and just query a file, [here](https://github.com/MBcode/dc/blob/main/call-summary.md)

as soon as the [system](https://github.com/MBcode/ec/blob/master/system.md) is made more modular, the repo.nq can come from my [crawl](https://github.com/MBcode/ec/tree/master/crawl) as well
