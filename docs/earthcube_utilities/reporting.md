# Using the Reports scripts

The utilities includes a set of scripts that can generate Q/A and other details about data summoned and loaded to a graph.
When installed as a python package (pip3 install earthcube_utilities) 
or editable developer package (cd earthcube_utilties; pip3 install -e .)

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


