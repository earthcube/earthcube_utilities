# Earthcube Utilities Code Documentation

!!! note
this does not work with multirepo plug, so will need to be linked 



## **Scripts**

## **ec_reports**
```Usage: ec_reports.py [OPTIONS] COMMAND [ARGS]...
Options:
  --cfgfile PATH          gleaner config file
  --s3server TEXT         s3 server address
  --s3bucket TEXT         s3 bucket
  --graphendpoint TEXT    graph endpoint
  --upload / --no-upload  upload to s3 bucket
  --output FILENAME       dump to file
  --debug / --no-debug
  --help                  Show this message and exit.

Commands:
  graph-stats
  missing-report
  identifier-stats
```

```
Usage: ec_reports.py missing-report [OPTIONS]

Options:
  --source TEXT           gone or more repositories (--source a --source b)
  --milled / --no-milled  include milled
  --summon / --no-sommon  check summon only
  --cfgfile PATH          gleaner config file
  --s3server TEXT         s3 server address
  --s3bucket TEXT         s3 bucket
  --graphendpoint TEXT    graph endpoint
  --upload / --no-upload  upload to s3 bucket
  --output FILENAME       dump to file
  --debug / --no-debug
  --help                  Show this message and exit.

```

```
Usage: ec_reports.py graph-stats [OPTIONS]

Options:
  --source TEXT           One or more repositories (--source a --source b)
  --detailed              run the detailed version of the reports
  --cfgfile PATH          gleaner config file
  --s3server TEXT         s3 server address
  --s3bucket TEXT         s3 bucket
  --graphendpoint TEXT    graph endpoint
  --upload / --no-upload  upload to s3 bucket
  --output FILENAME       dump to file
  --debug / --no-debug    run the detailed version of the reports
  --help                  Show this message and exit.

```

```
Usage: ec_reports.py identifier-stats [OPTIONS]

Options:
  --source TEXT           One or more repositories (--source a --source b)
  --detailed              run the detailed version of the reports
  --cfgfile PATH          gleaner config file
  --s3server TEXT         s3 server address
  --s3bucket TEXT         s3 bucket
  --graphendpoint TEXT    graph endpoint
  --upload / --no-upload  upload to s3 bucket
  --output FILENAME       dump to file
  --json boolean          output json format (default True for json, False for csv)
  --help                  Show this message and exit.

```

## **bucketutil**
```Usage: bucketutil.py [OPTIONS] COMMAND [ARGS]...
Options:
  --cfgfile PATH          Gleaner config file
  --s3server TEXT         S3 server address
  --s3bucket TEXT         S3 bucket
  --upload Boolean        Upload to s3 bucket. default True
  --output FILENAME       Dump to file
  --help                  Show this message and exit.

Commands:
  count
  urls
  download
  sourceurl
  duplicates
  stats
  cull
```
```
Usage: bucketutil.py count [OPTIONS]

Options:
  --path TEXT             Path to source, e.g. summoned/iris
  --milled Boolean        Include milled, default False
  --summon Boolean        Check summon only, default True
  --cfgfile PATH          Gleaner config file
  --s3server TEXT         S3 server address
  --s3bucket TEXT         S3 bucket
  --upload Boolean        Upload to s3 bucket
  --output FILENAME       dump to file
  --help                  Show this message and exit.
```
```
Usage: bucketutil.py urls [OPTIONS]

Options:
  --source TEXT           A repository
  --cfgfile PATH          Gleaner config file
  --s3server TEXT         S3 server address
  --s3bucket TEXT         S3 bucket
  --graphendpoint TEXT    Graph endpoint
  --upload Boolean        Upload to s3 bucket, default True
  --output FILENAME       Dump to file
  --help                  Show this message and exit.
```
```
Usage: bucketutil.py download [OPTIONS]

Options:
  --urn TEXT              One or more urns (--urn a --urn b)
  --cfgfile PATH          Gleaner config file
  --s3server TEXT         S3 server address
  --s3bucket TEXT         S3 bucket
  --upload Boolean        Upload to s3 bucket, default True
  --output FILENAME       Dump to file
  --help                  Show this message and exit.
```
```
Usage: bucketutil.py sourceurl [OPTIONS]

Options:
  --url TEXT              The X-Amz-Meta-Url in metadata
  --milled Boolean        Include milled, default False
  --summon Boolean        Check summon only, default True
  --cfgfile PATH          Gleaner config file
  --s3server TEXT         S3 server address
  --s3bucket TEXT         S3 bucket
  --upload Boolean        Upload to s3 bucket, default True
  --output FILENAME       Dump to file
  --help                  Show this message and exit.
```
```
Usage: bucketutil.py duplicateurls [OPTIONS]

Options:
  --source TEXT           One or more sources (--source a --source b)
  --cfgfile PATH          Gleaner config file
  --s3server TEXT         S3 server address
  --s3bucket TEXT         S3 bucket
  --upload Boolean        Upload to s3 bucket, default True
  --output FILENAME       Dump to file
  --help                  Show this message and exit.
```
```
Usage: bucketutil.py stats [OPTIONS]

Options:
  --source TEXT           One or more sources (--source a --source b)
  --cfgfile PATH          Gleaner config file
  --s3server TEXT         S3 server address
  --s3bucket TEXT         S3 bucket
  --upload Boolean        Upload to s3 bucket, default True
  --output FILENAME       Dump to file
  --help                  Show this message and exit.
```
```
Usage: bucketutil.py cullurls [OPTIONS]

Options:
  --source TEXT           One or more sources (--source a --source b)
  --cfgfile PATH          Gleaner config file
  --s3server TEXT         S3 server address
  --s3bucket TEXT         S3 bucket
  --graphendpoint TEXT    Graph endpoint
  --upload Boolean        Upload to s3 bucket, default True
  --output FILENAME       Dump to file
  --help                  Show this message and exit.
```

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
                              [--source] [--milled] [--summon]

optional arguments:
  -h, --help            show this help message and exit
  --graphendpoint GRAPHENDPOINT
                        graph endpoint
  --s3 S3SERVER         s3 server address (localhost:9000)
  --s3bucket S3BUCKET   s3 bucket name
  --cfgfile             a gleaner config file
  --no_upload           whether to write the missing report to s3 or not (True/False)
  --output              if no_upload is True, dump the missing report to output
  --source              one or more repositories (--source a --source b)
  --milled              include milled
  --summon              check summon only
```

::: ec.missing_report

## **summarize_identifier_metadata**
`summarize_identifier_metadata --graphendpoint https://graph.geocodes-dev.earthcube.org/blazegraph/namespace/earthcube/ 
--s3 localhost:9000 --s3bucket gleaner --cfgfile gleaner --no_upload True 
--output output.json --json False --source Iris`

```
usage: summarize_identifier_metadata.py [-h] [--graphendpoint GRAPHENDPOINT]
                              [--s3 S3SERVER] [--s3bucket S3BUCKET]
                              [--cfgfile] [--no_upload] [--output]
                              [--json] [--source]

optional arguments:
  -h, --help            show this help message and exit
  --graphendpoint GRAPHENDPOINT
                        graph endpoint
  --s3 S3SERVER         s3 server address (localhost:9000)
  --s3bucket S3BUCKET   s3 bucket name
  --cfgfile             a gleaner config file
  --no_upload           whether to write the missing report to s3 or not (True/False)
  --output              if no_upload is True, dump the report to output
  --json                output as json format, otherwise csv format (True/False)
  --source              one or more repositories (--source a --source b)
```

