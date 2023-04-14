# Earthcube Utilities Code Documentation

!!! note
this does not work with multirepo plug, so will need to be linked 



## **Scripts**

## **query_graph**
[Separate Document with Sparql Queries](./earthcube_utilities_graph_query_sparql.md )
`query_graph SPARQL_FILE --graphendpoint https://graph.geocodes-dev.earthcube.org/blazegraph/namespace/earthcube/ `

```
usage: query_graph.py [-h] [--graphendpoint GRAPHENDPOINT] [--output OUTPUT]
                      query

A tool to use the queries in the earthcube utilities

positional arguments:
  query                 select_one

optional arguments:
  -h, --help            show this help message and exit
  --graphendpoint GRAPHENDPOINT
                        graph endpoint
  --output OUTPUT       output file
```

## **check_sitemap**
`check_sitemap SITEMAP_URL --output FILE --no-check-url 

```
usage: check_sitemap.py [-h] [--output OUTPUT] [--no-url-check] [--no-progress] sitemapurl

positional arguments:
  sitemapurl       sitemapurl

optional arguments:
  -h, --help       show this help message and exit
  --output OUTPUT  output file
  --no-url-check   output file
  --no-progress    no progress bar
```

::: ec.check_sitemap


##  **generategrapstats**
`generategrapstats --graphendpoint https://graph.geocodes-dev.earthcube.org/blazegraph/namespace/earthcube/ -s3 localhost:9000 --s3bucket gleaner`

```
usage: generate_graph_stats.py [-h] [--graphendpoint GRAPHENDPOINT]
                               [--s3 S3SERVER] [--s3bucket S3BUCKET]
                               [--repo REPO] [--detailed]

optional arguments:
  -h, --help            show this help message and exit
  --graphendpoint GRAPHENDPOINT
                        graph endpoint
  --s3 S3SERVER         s3 server address (localhost:9000)
  --s3bucket S3BUCKET   s3 bucket name
  --repo REPO           repository
  --detailed            run the detailed version of the reports
```

::: ec.generate_graph_stats


## **missing_report**
`missing_report --graphendpoint https://graph.geocodes-dev.earthcube.org/blazegraph/namespace/earthcube/ 
--s3 localhost:9000 --s3bucket gleaner --cfgfile gleaner --no_upload True --output output.json`

```
usage: missing_report.py [-h] [--graphendpoint GRAPHENDPOINT]
                              [--s3 S3SERVER] [--s3bucket S3BUCKET]
                              [--cfgfile] [--no_upload] [--output]

optional arguments:
  -h, --help            show this help message and exit
  --graphendpoint GRAPHENDPOINT
                        graph endpoint
  --s3 S3SERVER         s3 server address (localhost:9000)
  --s3bucket S3BUCKET   s3 bucket name
  --cfgfile             a gleaner config file
  --no_upload           whether to write the missing report to s3 or not (True/False)
  --output              if no_upload is True, dump the missing report to output
```

::: ec.missing_report


