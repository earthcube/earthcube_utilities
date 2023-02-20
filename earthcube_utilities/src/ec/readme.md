### earthcube_utliites

#### originally used for notebooks only, but getting more reuse in the rest of the workflow

##### this has caused a natural breakdown of submodules, that can be used as needed

```mermaid
flowchart TD;
U[earthcube_utilities]  -- has --> R[a bit for opening data in notebooks];
U -- loads --> TR[the rest]
TR -- import --> MB[min-base];
TR -- import --> query[SPARQL queries from git];
TR -- import --> R2[rdf2nq];
``` 
