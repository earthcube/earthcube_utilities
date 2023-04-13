# notes on developing new sparql queries

graph:<urn:gleaner:summoned:opentopography:237ccc9501fc0e0349c8643e61e9db1e82dbd9ac>
top level subj: <https://portal.opentopography.org/raster?opentopoID=OTSDEM.052015.26910.1>
urn all triples in graph: 88

```sparql
SELECT distinct ?s ?p ?o ?g
WHERE     {
    GRAPH <urn:gleaner:summoned:opentopography:237ccc9501fc0e0349c8643e61e9db1e82dbd9ac> {?s ?p ?o .
    bind(<urn:gleaner:summoned:opentopography:237ccc9501fc0e0349c8643e61e9db1e82dbd9ac>   as ?g)
} }
```

subj_construct with blank nodes: 69

```sparql
CONSTRUCT {?x ?y ?z . ?z ?w ?v } WHERE
  {
    <https://portal.opentopography.org/raster?opentopoID=OTSDEM.052015.26910.1>  ?y ?z .
    BIND(<https://portal.opentopography.org/raster?opentopoID=OTSDEM.052015.26910.1>  as ?x)
    OPTIONAL {
      ?z ?w ?v
      FILTER (isBlank(?z) && !isBlank(?v))
     }
        OPTIONAL {
      ?z ?w ?v
      FILTER (!isBlank(?z) )
    }

}
```

V3 subj_construct with blank nodes: 82
mising the six  identifier triples <https://doi.org/10.5069/G9J10130>
```
CONSTRUCT {?x ?y ?z . ?z ?w ?v . ?z ?w1 ?v1 . ?v2 ?w3 ?v3} WHERE
  {
    <https://portal.opentopography.org/raster?opentopoID=OTSDEM.052015.26910.1>  ?y ?z .
    BIND(<https://portal.opentopography.org/raster?opentopoID=OTSDEM.052015.26910.1>  as ?x)
    OPTIONAL {
      ?z ?w ?v
      FILTER (isBlank(?z) && !isBlank(?v))
      
     }
     OPTIONAL {
      ?z ?w1 ?v1     
    }
    OPTIONAL {
      ?z ?w2 ?v2
      FILTER (isBlank(?z) && isBlank(?v2))
      ?v2 ?w3 ?v3
     }

}
```
