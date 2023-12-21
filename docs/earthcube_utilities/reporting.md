# Using the Reports scripts

The utilities include a set of scripts that can generate Q/A and other details about data summoned and loaded to a graph.
When installed as a python package (pip3 install earthcube_utilities) 
or editable developer package (cd earthcube_utilties; pip3 install -e .)

In the longer term, this will provide a record of how repostories grow/shrink etc.

These scripts are installed.

* `check_sitemap` - given a sitemap, checks to see if the url work
* `missing_report` = looks a data loss sitemap>summon>graph
* `generate_graph_stats` = provides a summary of the infromation loaded into a graph
* `summarize_identifier_metadata` - For each repo, provides summary on how sha identifers were generated.`
* `query_graph` = tool, not a report. It can be used to run a specific sqarql query from the command line

## Load process
1. [check sitemap](./earthcube_utilities_scripts.md#checksitemap), see that url work
2. run glcon gleaner batch
3. run a [missing_report  --summon](./earthcube_utilities_scripts.md#missingreport) to see what is possibly missing.
    * for a slow load, you can run this and see about possible issues with particular url patterns in the sitemap
4. run `summarize_identifier_metadata` - Do the identifiers seem reasonable
5. run glcon nabu prefix (and glcon nabu prune, if updating)
5. run [missing_report](./earthcube_utilities_scripts.md#missingreport)
6. run [generate_graph_stats](./earthcube_utilities_scripts.md#generategrapstats)


## check_sitemap
This read sitemap, and writes to a file (needs to be pushed to s3 with the sitemaps?)
It uses a head call to see if url is not 404.
Some webistes return 200 for all calls, so this will not be accurate, but

## missing report
Counts

* sitemap how many urls in a sitemap
* summon how many made it into the graphstore. This may be larger if multiple JSONLD's are in a page
* graph_urn_count how many JSONLD loaded into the graph

Records

* Missing_sitemap_Summon == Files w/o jsonld, or not a url
* "missing_summon_graph" URN's of files that did not make it into graph.

```json
{
  "source": "cchdo",
  "graph": "https://graph.geocodes-dev.earthcube.org/blazegraph/namespace/deepoceans/sparql",
  "sitemap": "https://cchdo.ucsd.edu/sitemap.xml",
  "date": "2023-04-19",
  "bucket": "deepoceans",
  "s3store": "oss.geocodes-dev.earthcube.org",
  "sitemap_count": 2527,
  "summoned_count": 2520,
  "missing_sitemap_summon": [
    "http://cchdo.ucsd.edu/search/map",
    "http://cchdo.ucsd.edu/search/advanced",
    "http://cchdo.ucsd.edu/contact",
    "http://cchdo.ucsd.edu/citation",
    "http://cchdo.ucsd.edu/policy",
    "http://cchdo.ucsd.edu/formats",
    "http://cchdo.ucsd.edu/cruise/FKAD20230131"
  ],
  "graph_urn_count": 2521,
  "missing_summon_graph": []
}
```
## Identifier Report
This summarizes which 'identifiers' were used to generate the unique identifier (sha hash)

```json
[
  {
    "Identifiertype":"identifiersha",
    "Matchedpath":"$.url",
    "Uniqueid":1
  },
  {
    "Identifiertype":"identifiersha",
    "Matchedpath":"$['@id']",
    "Uniqueid":2519
  }
]
```


## graph report
This queries the loaded graphstore.
There are two possibilties, all and per-source (repository)

All sources in a gleaner file will have one record, the org record.

A large difference between the JSONLD count and the Loaded graph count should show up in the missing_report

This tells you what Schema.org types are loaded from a source, how many datasets there are, and the diversity of keywords 
and variable naming. How many ways to say latitude, longitude... date, Day, etc 

While for variable names we may not need to address this, in loading since they describe the dataset, for 
discovery, we will need to well, use the graph for what the graph is good at.

```json
{
    "version": 0,
    "repo": "all",
    "date": "2023-04-19",
    "reports": [
        {
            "report": "triple_count",
            "data": [
                {
                    "tripelcount": "2346399"
                }
            ]
        },
        {
            "report": "graph_count_by_repo",
            "data": [
                {
                    "repo": "bco-dmo",
                    "graphs": "825",
                    "triples": "76096"
                },
                {
                    "repo": "cchdo",
                    "graphs": "2520",
                    "triples": "818876"
                },
                {
                    "repo": "r2r",
                    "graphs": "11105",
                    "triples": "613434"
                },
                {
                    "repo": "ssdb.iodp",
                    "graphs": "26155",
                    "triples": "837958"
                },
                {
                    "repo": "orgs:bco-dmo",
                    "graphs": "1",
                    "triples": "8"
                },
                {
                    "repo": "orgs",
                    "graphs": "2",
                    "triples": "16"
                },
             ]
        },
        {
            "report": "dataset_count",
            "data": [
                {
                    "datasetcount": "41137"
                }
            ]
        },
        {
            "report": "dataset_count_by_repo",
            "data": [
                {
                    "repo": "bco-dmo",
                    "graphs": "460",
                    "datasets": "998"
                },
                {
                    "repo": "cchdo",
                    "graphs": "2041",
                    "datasets": "2880"
                },
                {
                    "repo": "r2r",
                    "graphs": "11104",
                    "datasets": "11104"
                },
                {
                    "repo": "ssdb.iodp",
                    "graphs": "26155",
                    "datasets": "26155"
                }
            ]
        },
        {
            "report": "mutilple_version_count",
            "data": [
                {
                    "version": "1",
                    "scount": "69"
                },
                {
                    "version": "2",
                    "scount": "11"
                },
                {
                    "version": "09 September 2014",
                    "scount": "11"
                },
         
            ]
        },
        {
            "report": "mutilple_version_count_by_repo",
            "data": [
                {
                    "repo": "bco-dmo",
                    "versionscount": "259"
                }
            ]
        },
        {
            "report": "keywords_counts_by_repo",
            "data": [
                {
                    "keyword": "ctd",
                    "scount": "1808",
                    "repo": "cchdo"
                },
                {
                    "keyword": "bottle",
                    "scount": "1146",
                    "repo": "cchdo"
                },
                {
                    "keyword": "Timeseries",
                    "scount": "1001",
                    "repo": "cchdo"
                },
               
            ]
        },
        {
            "report": "types_count",
            "data": [
                {
                    "type": "https://schema.org/GeoCoordinates",
                    "scount": "143170"
                },
                {
                    "type": "https://schema.org/DataDownload",
                    "scount": "57770"
                },
                {
                    "type": "https://schema.org/Dataset",
                    "scount": "41137"
                },
                {
                    "type": "https://schema.org/Place",
                    "scount": "39621"
                },
                {
                    "type": "https://schema.org/Person",
                    "scount": "38268"
                },
                {
                    "type": "https://schema.org/GeoShape",
                    "scount": "35022"
                },
                {
                    "type": "https://schema.org/CreativeWork",
                    "scount": "33312"
                },
                {
                    "type": "https://schema.org/Organization",
                    "scount": "22595"
                },
                {
                    "type": "https://schema.org/PropertyValue",
                    "scount": "17119"
                },
                {
                    "type": "https://schema.org/DataCatalog",
                    "scount": "2520"
                },
                {
                    "type": "https://schema.org/DigitalDocument",
                    "scount": "1095"
                },
                {
                    "type": "https://schema.org/FundingAgency",
                    "scount": "607"
                },
                {
                    "type": "https://schema.org/MonetaryGrant",
                    "scount": "607"
                },
                {
                    "type": "https://schema.org/ResearchProject",
                    "scount": "439"
                },
                {
                    "type": "http://spdx.org/rdf/terms#Checksum",
                    "scount": "282"
                },
                {
                    "type": "https://schema.org/Event",
                    "scount": "200"
                },
                {
                    "type": "https://schema.org/Service",
                    "scount": "5"
                },
                {
                    "type": "https://schema.org/SearchAction",
                    "scount": "4"
                },
                {
                    "type": "https://schema.org/ServiceChannel",
                    "scount": "4"
                },
                {
                    "type": "https://schema.org/EntryPoint",
                    "scount": "3"
                },
                {
                    "type": "https://schema.org/OfferCatalog",
                    "scount": "3"
                },
                {
                    "type": "https://schema.org/WebSite",
                    "scount": "2"
                },
                {
                    "type": "https://schema.org/PostalAddress",
                    "scount": "2"
                },
                {
                    "type": "https://schema.org/ContactPoint",
                    "scount": "1"
                },
                {
                    "type": "https://schema.org/ImageObject",
                    "scount": "1"
                },
                {
                    "type": "https://schema.org/thing",
                    "scount": "1"
                },
                {
                    "type": "https://schema.org/Thing",
                    "scount": "1"
                },
                {
                    "type": "https://schema.org/WebPage",
                    "scount": "1"
                }
            ]
        },
        {
            "report": "keywords_count",
            "data": [
                {
                    "keyword": "ctd",
                    "scount": "1808"
                },
                 ]
        },
        {
            "report": "variablename_count",
            "data": [
                {
                    "variableName": "lat",
                    "scount": "116"
                },
                {
                    "variableName": "lon",
                    "scount": "112"
                },
                {
                    "variableName": "year",
                    "scount": "57"
                },
                {
                    "variableName": "date",
                    "scount": "56"
                },
                {
                    "variableName": "depth",
                    "scount": "43"
                },
                {
                    "variableName": "ISO_DateTime_UTC",
                    "scount": "38"
                },
                {
                    "variableName": "day",
                    "scount": "37"
                },
                {
                    "variableName": "time",
                    "scount": "34"
                },
                {
                    "variableName": "temp",
                    "scount": "34"
                },
                
 
                {
                    "variableName": "Latitude",
                    "scount": "28"
                },
                {
                    "variableName": "Longitude",
                    "scount": "28"
                },
                {
                    "variableName": "event",
                    "scount": "26"
                },
                {
                    "variableName": "month",
                    "scount": "26"
                },
                {
                    "variableName": "station",
                    "scount": "25"
                },
 
                {
                    "variableName": "site",
                    "scount": "20"
                },
                {
                    "variableName": "LATITUDE",
                    "scount": "19"
                },
                {
                    "variableName": "LONGITUDE",
                    "scount": "19"
                },
                {
                    "variableName": "time_local",
                    "scount": "19"
                },

                {
                    "variableName": "Date",
                    "scount": "17"
                },
                {
                    "variableName": "Station",
                    "scount": "16"
                },
                {
                    "variableName": "Time",
                    "scount": "15"
                },
                {
                    "variableName": "Lat",
                    "scount": "15"
                },
                {
                    "variableName": "Lon",
                    "scount": "15"
                },

            ]
        },
        {
            "report": "graph_sizes",
            "data": [
                {
                    "triplesize": "31",
                    "triplecount": "12181"
                },
                {
                    "triplesize": "54",
                    "triplecount": "6414"
                },
 
                {
                    "triplesize": "1029",
                    "triplecount": "1"
                },
                {
                    "triplesize": "3",
                    "triplecount": "1"
                }
            ]
        }
    ]
}
```
