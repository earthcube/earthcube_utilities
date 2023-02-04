## what you call to run initial summarization

#### For the initial summarziation, we can pull from blaze and summarize all the repos in the namespace filled by the crawl

```mermaid
flowchart TD;
SR[summarize_namespace.sh];
SR -- calls --> F2[2: tsum.py] -- 1:queries --> BMN[blaze's big namespace];
F2 -- 2:produces --> RT(namespace.ttl) -- ttl2blaze.sh --> B[blaze's summary];
```

### after that we would go back to adding on a per repo basis, as see [here](call.md)

as soon as the [system](https://github.com/MBcode/ec/blob/master/system.md) is made more modular, the repo.nq can come from my [crawl](https://github.com/MBcode/ec/tree/master/crawl) as well
