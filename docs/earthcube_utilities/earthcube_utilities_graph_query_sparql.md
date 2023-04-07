# Earthcube Utilities Queries


## **query_graph**
`query_graph SPARQL_RESOURCE --graphendpoint https://graph.geocodes-dev.earthcube.org/blazegraph/namespace/earthcube/ `

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

## SPARQL RESOURCES
The naming pattern is if the query starts with all_ then it applies to the overall graph store, and requires no parameters

if the naming patter includes a repo or a urn then those are the parameters

```python

``` 

### Basic Queries
####  select_one

test query, returns one triple
~~~sparql
{%
   include '../../earthcube_utilities/src/ec/graph/sparql_files/select_one.sparql'
   
%}
~~~

#### urn_triples_for_a_graph

parameter:
 urn - the urn identifier of the graph to be retrieved.

returns a list of triples which represents one JSONLD file, aka graph
~~~sparql
{%
   include '../../earthcube_utilities/src/ec/graph/sparql_files/urn_triples_for_a_graph.sparql'
   
%}
~~~

### Information about the overall graph

These may be used to collect information on the overall graph.

In addition, when onboarding a community, these can be used to assess the evaluation
the information for  repository containing a single communities data.

####  all_count_datasets 
~~~sparql
{%
   include '../../earthcube_utilities/src/ec/graph/sparql_files/all_count_datasets.sparql'
   
%}
~~~

####  all_count_keywords
~~~sparql
{%
   include '../../earthcube_utilities/src/ec/graph/sparql_files/all_count_keywords.sparql'
   
%}
~~~

####  all_count_multiple_versioned_datasets 
~~~sparql
{%
   include '../../earthcube_utilities/src/ec/graph/sparql_files/all_count_multiple_versioned_datasets.sparql'
   
%}
~~~

####  all_count_triples 
~~~sparql
{%
   include '../../earthcube_utilities/src/ec/graph/sparql_files/all_count_triples.sparql'
   
%}
~~~

#### all_graph_sizes
Returns aggregate of the size of the generated  triples for each loaded JSON-LD objects,

High triple counts for a triple size may indicate a conversion issue

~~~sparql
{%
   include '../../earthcube_utilities/src/ec/graph/sparql_files/all_graph_sizes.sparql'
   
%}
~~~

####  all_count_types
~~~sparql
{%
   include '../../earthcube_utilities/src/ec/graph/sparql_files/all_count_types.sparql'
   
%}
~~~

####  all_count_variablename 

~~~sparql
{%
   include '../../earthcube_utilities/src/ec/graph/sparql_files/all_count_variablename.sparql'
   
%}
~~~

####  all_repo_count_datasets 
~~~sparql
{%
   include '../../earthcube_utilities/src/ec/graph/sparql_files/all_repo_count_datasets.sparql'
   
%}
~~~

####  all_repo_count_graphs

returns a count of inserted JSON-LD files, where each graph is a file.
~~~sparql
{%
   include '../../earthcube_utilities/src/ec/graph/sparql_files/all_repo_count_graphs.sparql'
   
%}
~~~

####  all_repo_count_keywords 
~~~sparql
{%
   include '../../earthcube_utilities/src/ec/graph/sparql_files/all_repo_count_keywords.sparql'
   
%}
~~~

####  all_repo_count_versioned_datasets

returns a count of graphs including the version field.
~~~sparql
{%
   include '../../earthcube_utilities/src/ec/graph/sparql_files/all_repo_count_versioned_datasets.sparql'
   
%}
~~~

####  all_repo_with_keywords 

Returns rows with a repo brief name, and the count of the keywords in that repo
~~~sparql
{%
   include '../../earthcube_utilities/src/ec/graph/sparql_files/all_repo_with_keywords.sparql'
   
%}
~~~

####  all_select_datasets 

returns a list of Schema.org/Dataset
~~~sparql
{%
   include '../../earthcube_utilities/src/ec/graph/sparql_files/all_select_datasets.sparql'
   
%}
~~~

####  all_select_graphs 

returns a list of graphs, which are the urn's of the JSONLD files
~~~sparql
{%
   include '../../earthcube_utilities/src/ec/graph/sparql_files/all_select_graphs.sparql'
   
%}
~~~

####  all_summary_query

Return records with the fields as a 'summary ' which is used to materialize a view for performance

this will need to be rewritten to use a LIMIT and OFFSET
~~~sparql
{%
   include '../../earthcube_utilities/src/ec/graph/sparql_files/all_summary_query.sparql'
   
%}
~~~

####  all_versioned_datasets_multiple_versions 

returns Schema.org/Dataset with more than one version.

this might need to be a UNION with using SameAs, or another field... someone uses a different pattern
~~~sparql
{%
   include '../../earthcube_utilities/src/ec/graph/sparql_files/all_versioned_datasets_multiple_versions.sparql'
   
%}
~~~

### Information for an individual repository

These queries take a parameter 'repo'


####  repo_count_datasets 

Returns count of Schema.org/Dataset
~~~sparql
{%
   include '../../earthcube_utilities/src/ec/graph/sparql_files/repo_count_datasets.sparql'
   
%}
~~~

####  repo_count_triples_by_graph 

Returns count of triples for each loaded JSON-LD objects,

If the count is small, and the same number, then it is possible that the conversion from JSON-LD to RDF
is broken for this repository.

~~~sparql
{%
   include '../../earthcube_utilities/src/ec/graph/sparql_files/repo_count_triples_by_graph.sparql'
   
%}
~~~

#### repo_graph_sizes
Returns aggregate of the size of the generated  triples for each loaded JSON-LD objects,

If the count is small, and the same number, then it is possible that the conversion from JSON-LD to RDF
is broken for this repository.
~~~sparql
{%
   include '../../earthcube_utilities/src/ec/graph/sparql_files/repo_graph_sizes.sparql'
   
%}
~~~

####  repo_count_graphs

Count of loaded JSON-LD files
~~~sparql
{%
   include '../../earthcube_utilities/src/ec/graph/sparql_files/repo_count_graphs.sparql'
   
%}
~~~

####  repo_count_keywords 
~~~sparql
{%
   include '../../earthcube_utilities/src/ec/graph/sparql_files/repo_count_keywords.sparql'
   
%}
~~~

####  repo_count_multi_versioned_datasets 

Does this repo have multiple dataset versions, if so, what is the count.


~~~sparql
{%
   include '../../earthcube_utilities/src/ec/graph/sparql_files/repo_count_multi_versioned_datasets.sparql'
   
%}
~~~

####  repo_count_triples
~~~sparql
{%
   include '../../earthcube_utilities/src/ec/graph/sparql_files/repo_count_triples.sparql'
   
%}
~~~

####  repo_count_types 
~~~sparql
{%
   include '../../earthcube_utilities/src/ec/graph/sparql_files/repo_count_types.sparql'
   
%}
~~~

####  repo_count_variablename 
~~~sparql
{%
   include '../../earthcube_utilities/src/ec/graph/sparql_files/repo_count_variablename.sparql'
   
%}
~~~

####  repo_graphs_startwith
~~~sparql
{%
   include '../../earthcube_utilities/src/ec/graph/sparql_files/repo_graphs_startwith.sparql'
   
%}
~~~

####  repo_select_datasets 

return urns/graph of Schema.org/Dataset
~~~sparql
{%
   include '../../earthcube_utilities/src/ec/graph/sparql_files/repo_select_datasets.sparql'
   
%}
~~~

####  repo_select_graphs

return urns/graph of all loaded information
~~~sparql
{%
   include '../../earthcube_utilities/src/ec/graph/sparql_files/repo_select_graphs.sparql'
   
%}
~~~

####  repo_summary_query

Return records with the fields as a 'summary ' which is used to materialize a view for performance

this will need to be rewritten to use a LIMIT and OFFSET
~~~sparql
{%
   include '../../earthcube_utilities/src/ec/graph/sparql_files/repo_summary_query.sparql'
   
%}
~~~




## Code

::: ec.generate_graph_stats


