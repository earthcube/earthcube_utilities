# Meeting Notes


## ERDDAP

Questions:
* The URL for the metadata (align with ERDDAP patterns for existing metadata vs embedding)
* depth profile
* if not "depth" "pres" then there should be cdm_altitude_proxy
  * cdm_altitude_proxy is in the description
* Looks at https://osmc.noaa.gov/erddap/info/MEOP_profiles/index.html and see how to encode NC_GLOBAL
  * 

Refs:
* https://osmc.noaa.gov/erddap/categorize/variableName/typedeath/index.html?page=1&itemsPerPage=1000


### Sources

```html
  # Observing System Monitoring Center
  #
  - name: osmc
    propername: Observing System Monitoring Center (OSMC)
    catalogue: https://osmc.noaa.gov/erddap/info/index.html
    domain: https://www.osmc.noaa.gov/
    logo: https://www.osmc.noaa.gov/OSMC_logo.png
    pid: https://catalogue.odis.org/view/3307
    sourcetype: sitemap
    url: https://osmc.noaa.gov/erddap/sitemap.xml
    changefreq: monthly
    backend: ERDDAP
    headless: false
    dateadded: 2023-10-12
    cron: 0 10 * * 0
    active: true
```

```bash
curl -s https://osmc.noaa.gov/erddap/sitemap.xml |   grep -oP '<loc>\K[^<]*'
```



### SHACL

See:  https://github.com/iodepo/odis-in/tree/master/shapeGraphs#erddap


### ML Commons

See: https://mlcommons.org/working-groups/data/croissant/


### Context

```html
<script type="application/ld+json">
{
"@context": "http://schema.org",
"@type": "Dataset",
```


to


```html
<script type="application/ld+json">
{
"@context": {
"@vocab": "http://schema.org/"
},
"@type": "Dataset",
```
