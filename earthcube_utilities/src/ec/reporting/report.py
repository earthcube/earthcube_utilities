import json

from ec.graph.sparql_query import queryWithSparql

from ec.datastore.s3 import MinioDatastore, bucketDatastore
## this is overly complex it can be done simply.
## rethink later

class History():
    item = ''
    count=0


class ReportRepository():
    name = ''
    # TimeSeriesCount( sitemap, jsonld, graphcount, datasetcount, totaltriplecount )

    # for each one of graphtype and keyword will be an array of timeseries.
    dates=[] # just use one date in the array.
    summoncount =[]
    graphcount =[]

    graphtypescount = [] # of history
    keywordscount = [] # of history

    def get_last_date(self):
        pass
    def get_report(self,bucket, repo):
        pass


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

