## what you call to run summarization

#### from getting (gleaner) crawler's quad/repo  through making the summary triples, and loading them

```mermaid
flowchart TD;
R2S[repo_to_summary.sh]  -- calls --> G[1: fix_runX.sh];
G -- calls --> gr[1:get_repo.py]
G -- calls --> r2n[2:run2nq.py] -- loads --> rdf2[rdf2nq.py];
r2n -- produces --> nq(repo.nq);
R2S -- calls --> SR[2: summarize_repo.sh];
SR -- calls --> F2[tsum.py] -- loads2tmp_blaze --> nq;
F2 -- produces --> RT(2: repo.ttl) -- ttl2blaze.sh --> B[blazegraph];
```

#### there is a simplification of this, that would skip a server and just query a file, [here](https://github.com/MBcode/dc/blob/main/call-summary.md)

as soon as the [system](https://github.com/MBcode/ec/blob/master/system.md) is made more modular, the repo.nq can come from my [crawl](https://github.com/MBcode/ec/tree/master/crawl) as well
