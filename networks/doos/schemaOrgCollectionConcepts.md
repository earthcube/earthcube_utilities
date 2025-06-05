## List thoughts


ItemList

itemListElement

@id with 

https://www.w3.org/TR/json-ld/#reverse-properties

```json
{
  "@context": "https://schema.org/",
  "@graph":[
     {   
       "@id": "urn:example:dataset-list",
      "@type": "ItemList"
     },
     {
        "@type": "Dataset",
        "@id": "urn:example:dataset-01",
        "@reverse": {
            "itemListElement": [
                {"@id": "urn:example:dataset-list"}
            ]
        }
     }
  ]
}
``` 


```json
{
  "@context": {
    "@vocab": "https://schema.org/",
    "doos": "https://example.com/doos#",
    "doos:conformsToDeepOceanProfile": {"@reverse": "itemListElement"}
  },
  "@graph":[
     {   
       "@id": "urn:example:deep-ocean:depth",
       "@type": "ItemList"
     },
     {
       "@type": "Dataset",
       "@id": "urn:example:dataset-01",
       "doos:conformsToDeepOceanProfile": {"@id": "urn:example:deep-ocean:depth"}
     }
  ]
}
```


DOOS: put this at "https://example.com/doos/context.jsonld"
```json
{
  "@context": {
    "@vocab": "https://schema.org/",
    "doos_conformsToDeepOceanProfile": {"@reverse": "itemListElement"}
  },
  "@graph":[
     {   
       "@id": "urn:example:deep-ocean:depth",
       "@type": "ItemList"
     }
  ]
}
```


ADOPTER:
```json
{
  "@context": {
    "@vocab": "https://schema.org/",
    "https://example.com/doos/context.jsonld"
  },
  "@type": "Dataset",
  "@id": "urn:example:dataset-01",
  "doos_conformsToDeepOceanProfile": {"@id": "urn:example:deep-ocean:depth"}
}
```


