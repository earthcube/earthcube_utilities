# additionalProperty for Dataset

## The use of additionalProperty for NV_GLOBAL

When reviewing the variable and attribute values at  https://osmc.noaa.gov/erddap/info/MEOP_profiles/index.html for inclusion in the
JSON-LD representation for a page we can note a few things.

1) the use of additionalProperty is not in the domain of Thing
2) however, GitHub issue https://github.com/schemaorg/schemaorg/issues/3540 notes that this is being discussed.

Based on that we can see that putting

```json
{
    "@context": "https://schema.org/",
    "@type": "Dataset",
    "name": "HOT: Niskin bottle samples",
    "description": "Something, Something, Something, Something, Something, Something, Something, Something, Something",
    "additionalProperty": {
        "@type": "PropertyValue",
        "propertyID": "https://dbpedia.org/page/Spatial_reference_system",
        "value": "https://www.w3.org/2003/01/geo/wgs84_pos"
    }
}
```

into https://validator.schema.org/ results in 0 errors or warnings.

Based on all this it is recommended that additionalProperty be used to encode NC_GLOBAL values for a dataset.  The approach would look something like.

```json
  "additionalProperty": [
     {
            "@type": "PropertyValue",
            "additionalType": "NC_GLOBAL",
            "name": "cdm_altitude_proxy",
            "propertyID": "https://example.org/cdm_altitude_proxy",
            "value": "PRES"
      }
    ],
```

This example uses an array via ```[]``` simply to denote that many of these poperties could be included.

Questions:

- [ ] should be note this as an additionalType of NC_GLOBAL?
- [ ] do CDM values have established URIs for values?
- [ ] for cases where there is no URI is there a wikidata or some of ther refernece that can be used?
