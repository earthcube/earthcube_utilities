# Earthcube Utilities Code Documentation

!!! note
this does not work with multirepo plug, so will need ot be linked 



## **Scripts**

 `

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

## **query_graph**
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

Queries 
all_count_datasets 
all_count_keywords
all_count_multiple_versioned_datasets 
all_count_triples all_count_types
all_count_variablename 
all_repo_count_datasets 
all_repo_count_graphs
all_repo_count_keywords 
all_repo_count_versioned_datasets
all_repo_with_keywords 
all_select_datasets 
all_select_graphs 
all_summary_query
all_versioned_datasets_multiple_versions 
get_triples_for_a_graph
repo_count_datasets 
repo_count_graph_triples 
repo_count_graphs
repo_count_keywords 
repo_count_multi_versioned_datasets 
repo_count_triples
repo_count_types 
repo_count_variablename 
repo_graphs_startwith
repo_select_datasets 
repo_select_graphs 
repo_summary_query 
select_one
```
~~~sparql
{%
   include '../src/ec/graph/sparql_files/*.sparql'
   
%}
~~~

::: ec.query_graph

##  **generaterepostats**
`generaterepostats --graphendpoint https://graph.geocodes-dev.earthcube.org/blazegraph/namespace/earthcube/ -s3 localhost:9000 --s3bucket gleaner`

```
usage: generaterepostats [-h] [--graphendpoint GRAPHENDPOINT] [--s3 S3SERVER] [--s3bucket S3BUCKET]

optional arguments:
  -h, --help            show this help message and exit
  --graphendpoint GRAPHENDPOINT
                        graph endpoint
  --s3 S3SERVER         s3 server address (localhost:9000)
  --s3bucket S3BUCKET   s3 server address (localhost:9000)

```

::: ec.generate_repo_stats


