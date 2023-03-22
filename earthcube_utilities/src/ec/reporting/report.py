import json

from ec.graph.sparql_query import queryWithSparql

from ec.datastore.s3 import MinioDatastore, bucketDatastore
## this is overly complex it can be done simply.
## rethink later

"""
reports

simplifiying the thinking.
These go into a reports store in the datastore

we can calculate in multiple ways
eg for items that were not summomed due to no jsonld, calculate from s3 compare to sitemap, and pull for gleaner logs 

Let's start with ones we can do easily.

Reports
* PROCESSING REPORT: sitemap count, summoned count, milled count, if approriate.
**  general report with the basics. counts, good, bad, etc.
*** sitemap count
*** summoned count
*** graph count 
*** count of  was summoned but did not make it into the graph

* PROCESSING REPORT DETAILS:
** thought... how to handle what got lost... need to know, or perhaps files with lists of what got lost along the way
*** SITEMAP
**** list of bad urls
**** list of urls for items that had no JSONLD. Grab list of metadater-Url from Datastore, compare to sitemap url list
*** PROCESSING

* GRAPHSTORE REPORTS: 
This runs a list of sparql queries
** What is in the overall graph, 
** Data Loading reports by  Repo 


Probably run the all repo report monthly, or after a large data load
Run the repo report have a repo is reloaded.

FUTURE:
Use repo reports as a qa tool.

"""


def compareSummoned2Milled(bucket, repo, datastore):
    """ return list of missing urns/urls
    Generating milled will be good to catch such errors"""
    # compare using s3, listJsonld(bucket, repo) to  listMilledRdf(bucket, repo)
    pass

def compareSummoned2Graph(bucket, repo, datastore, graphendpoint):
    """ return list of missing .
    we do not alway generate a milled.
    """
    # compare using s3, listJsonld(bucket, repo) to queryWithSparql("repo_select_graphs", graphendpoint)
    pass


def putProcessingReports4Repo(repo, date,  json_str, datastore: bucketDatastore, reportname='processing.json',):
    """put reports about the processing into reports store
    this should be items like the sitemap count, summoned counts, and 'milled' counts if apprporate"""
    # store twice. latest and date
    bucket_name, object_name= bucketDatastore.putReportFile(datastore.default_bucket, repo, reportname, json_str, date=date)
    # might return a url...
    return bucket_name, object_name

##################################
#  REPORT GENERATION USING SPARQL QUERIES
#   this uses defined spaql queries to return counts for reports
###################################
reportTypes ={
    "all": [{"code":"triple_count", "name": "all_count_triples"},
            {"code":"graph_count_by_repo", "name": "all_repo_count_graphs"},
{"code":"kw_count", "name": "all_count_keywords"},
{"code":"kw_count_by_repo", "name": "all_repo_count_keywords"},
{"code":"dataset_count", "name": "all_count_datasets"},
            {"code":"dataset_count_by_repo", "name": "all_repo_count_keywords"},
{"code":"types_count", "name": "all_count_types."},
            {"code":"variablename_count", "name": "all_count_variablename"},
            {"code": "mutilple_version_count", "name": "all_count_multiple_versioned_datasets"}
            ],
    "repo":[
        {"code":"kw_count", "name": "repo_count_keywords"},
{"code":"dataset_count", "name": "repo_count_datasets"},
{"code":"triples_count_by_graph", "name": "repo_count_graph_triples"},
{"code":"triples_count", "name": "repo_count_triples"},
{"code":"types_count", "name": "repo_count_types"},
{"code":"version_count", "name": "repo_count_multi_versioned_datasets"},
{"code":"variablename_count", "name": "repo_count_variablename"},
    ]
}
##  for the 'object reports, we should have a set.these could probably be make a set of methos with (ObjectType[triples,keywords, types, authors, etc], repo, endpoint/datastore)
def generateGraphReportsRepo(repo, graphendpoint):
    #queryWithSparql("repo_count_types", graphendpoint)
    parameters = {"repo": repo}
    if repo== "all":
        reports = map (lambda r:   {"report": r.code,
                                 "data": queryWithSparql(r.name, graphendpoint, parameters=parameters)
                                 }    ,reportTypes["all"])
    else:
        reports = map(lambda r: {"report": r.code,
                                 "data": queryWithSparql(r.name, graphendpoint, parameters=parameters)
                                 },
                                 reportTypes["repo"])
    return {"version": 0, "reports": json.dumps(reports) }

def generateAGraphReportsRepo(repo, code, graphendpoint):
    #queryWithSparql("repo_count_types", graphendpoint)
    parameters = {"repo": repo}
    if repo== "all":
        return  queryWithSparql(reportTypes["all"][code], graphendpoint, parameters=parameters)

    else:
        return queryWithSparql(reportTypes["repo"][code], graphendpoint, parameters=parameters)

def getGraphReportsLatestRepoReports(repo,  datastore: bucketDatastore):
    """get the latest for a dashboard"""
    date="latest"
    path = f"{datastore.paths['reports']}/{repo}/{date}/sparql.json"
    filelist = datastore.getReportFile(datastore.default_bucket, repo, path)

def listGraphReportDates4Repo(repo,  datastore: bucketDatastore):
    """get the latest for a dashboard"""
    path = f"{datastore.paths['reports']}/{repo}/"
    filelist = datastore.listPath(path)
    return filelist
def putGraphReports4RepoReport(repo, date,  json_str, datastore: bucketDatastore, reportname='sparql.json',):
    """put the latest for a dashboard. report.GetLastDate to store"""
    # store twice. latest and date
    bucket_name, object_name= bucketDatastore.putReportFile(datastore.default_bucket, repo, reportname, json_str, date=date)
    # might return a url...
    return bucket_name, object_name

