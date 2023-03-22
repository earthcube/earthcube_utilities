import json
import logging

import pandas
import pydash

from ec.graph.sparql_query import queryWithSparql

from ec.datastore.s3 import MinioDatastore, bucketDatastore


"""
reports

simplifying the thinking.
These go into a reports store in the datastore

we can calculate in multiple ways
eg for items that were not summoned due to no jsonld, calculate from s3 compare to sitemap, and pull for gleaner logs 

Let's start with ones we can do easily.

Reports
* PROCESSING REPORT: (processing.json) 
**  general report with the basics. counts, good, bad, etc.
*** sitemap count
*** summoned count ec.datastore.s3.countJsonld
*** milled count ec.datastore.s3.countMilled
*** graph count repo_count_graphs.sparql ec.graph.sparql_query.queryWithSparql("repo_count_graphs", graphendpoint, parameters={"repo": repo})
*** when processing details is working, then add counts of  was summoned but did not make it into the graph

* PROCESSING REPORT DETAILS:
** thought... how to handle what got lost... need to know, or perhaps files with lists of what got lost along the way
*** SITEMAP Details and issues
**** (sitemap_badurls.csv)list of bad urls
**** (sitemap_summon_issues.csv) list of urls for items that had no JSONLD. 
*****  Grab list of metadater-Url from Datastore, ec.datastore.s3.listSummonedUrls
*****  compare to sitemap url list
*****  remove bad urls. if it cannot be retrieved, we don't need to chase it down
*** PROCESSING Detials and issues
**** (summon_graph_missing.csv; summon_milled_missing.csv;) what made and did not make it. Parameters
**** summoned ids: ec.datastore.s3.listJsonld
# will need to do a list(map(lambda , collection) to get a list of urls.
o_list = list(map(lambda f: ec.datastore.s3.urnFroms3Path(f.object_name), objs))
**** milled ids: ec.datastore.s3.listMilledRdf
**** graph ids:  ec.graph.sparql_query.queryWithSparql("repo_select_graphs", graphendpoint, parameters={"repo": repo})

***** suggest compare using pydash, or use pandas...
then look up the urls' using: ec.datastore.s3.getJsonLDMetadata

* GRAPHSTORE REPORTS: sparql.json
This runs a list of sparql queries
** What is in the overall graph, 
** Data Loading reports by  Repo 


Probably run the all repo report monthly, or after a large data load
Run the repo report have a repo is reloaded.

FUTURE:
Use issues from repo reports as data for a tool that can evaluate the failures

"""

def compareSitemap2Summoned(valid_sitemap_urls, bucket, repo, datastore: bucketDatastore):
    #Grab list of metadater-Url from Datastore, ec.datastore.s3.listSummonedUrls
    pass

def compareSummoned2Milled(bucket, repo, datastore: bucketDatastore):
    """ return list of missing urns/urls
    Generating milled will be good to catch such errors"""
    # compare using s3, listJsonld(bucket, repo) to  listMilledRdf(bucket, repo)
    pass

def compareSummoned2Graph(bucket, repo, datastore: bucketDatastore, graphendpoint):
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
reportTypes = {
    "all": [
        {"code": "triple_count", "name": "all_count_triples"},
            {"code": "graph_count_by_repo", "name": "all_repo_count_graphs"},
            {"code": "kw_count", "name": "all_count_keywords"},
            {"code": "kw_count_by_repo", "name": "all_repo_count_keywords"},
            {"code": "dataset_count", "name": "all_count_datasets"},
            {"code": "dataset_count_by_repo", "name": "all_repo_count_keywords"},
            {"code": "types_count", "name": "all_count_types"},
            {"code": "variablename_count", "name": "all_count_variablename"},
            {"code": "mutilple_version_count", "name": "all_count_multiple_versioned_datasets"}
     ],
    "repo": [
        {"code": "kw_count", "name": "repo_count_keywords"},
        {"code": "dataset_count", "name": "repo_count_datasets"},
        {"code": "triple_count_by_graph", "name": "repo_count_graph_triples"},
        {"code": "triple_count", "name": "repo_count_triples"},
        {"code": "type_count", "name": "repo_count_types"},
        {"code": "version_count", "name": "repo_count_multi_versioned_datasets"},
        {"code": "variablename_count", "name": "repo_count_variablename"},
    ]
}

def _get_report_type(repo, code):
    if repo == "all":
        report = pydash.find(reportTypes["all"], lambda r: r["code"] == code)
    else:
        report =pydash.find(reportTypes["repo"], lambda r:  r["code"] == code)
    return report["name"]

##  for the 'object reports, we should have a set.these could probably be make a set of methos with (ObjectType[triples,keywords, types, authors, etc], repo, endpoint/datastore)
def generateGraphReportsRepo(repo, graphendpoint, reportTypes=reportTypes):
    #queryWithSparql("repo_count_types", graphendpoint)
    parameters = {"repo": repo}
    if repo== "all":
        reports = map (lambda r:   {"report": r["code"],
                                 "data": generateAGraphReportsRepo("all", r["code"],graphendpoint).to_dict('records')
                                 }    ,reportTypes["all"])
    else:
        reports = map(lambda r: {"report": r["code"],
                                 "data": generateAGraphReportsRepo("repo", r["code"], graphendpoint).to_dict('records')
                                 },
                                 reportTypes["repo"])
    reports = list(reports)
    return json.dumps({"version": 0, "reports": reports }, indent=4)

def generateAGraphReportsRepo(repo, code, graphendpoint):
    #queryWithSparql("repo_count_types", graphendpoint)
    parameters = {"repo": repo}
    try:
        if repo== "all":
            return  queryWithSparql(_get_report_type("all", code), graphendpoint, parameters=parameters)

        else:
            return queryWithSparql(_get_report_type("repo", code), graphendpoint, parameters=parameters)
    except Exception as ex:
        logging.error(f"query with sparql failed: report:{code}  repo:{repo}   {ex}")
        return pandas.DataFrame()

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

def putGraphReports4RepoReport(repo, json_str, datastore: bucketDatastore, date='latest', reportname='sparql.json'):
    """put the latest for a dashboard. report.GetLastDate to store"""
    # store twice. latest and date
    bucket_name, object_name= datastore.putReportFile(datastore.default_bucket, repo, reportname, json_str, date=date)
    # might return a url...
    return bucket_name, object_name

