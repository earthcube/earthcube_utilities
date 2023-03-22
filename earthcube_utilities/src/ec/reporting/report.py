
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

##  for the 'object reports, we should have a set.these could probably be make a set of methos with (ObjectType[triples,keywords, types, authors, etc], repo, endpoint/datastore)
def graphTypes4Repo(repo, graphendpoint):
    #queryWithSparql("repo_count_types", graphendpoint)
    pass

def getGraphTypes4RepoReport(repo, datastore):
    """get the latest for a dashboard"""
    pass
def putGraphTypes4RepoReport(repo, date, datastore):
    """put the latest for a dashboard. report.GetLastDate to store"""
    # store twice. latest and date
    pass

def graphKeywordsRepo(repo, graphendpoint):
    #queryWithSparql("repo_count_keywords", graphendpoint)
    pass

def getgGraphKeywords4RepoReport(repo, datastore):
    """get the latest for a dashboard"""
    pass

def putGraphKeywords4RepoReport(repo, date, datastore):
    """put the latest for a dashboard. report.GetLastDate to store"""
    # store twice. latest and date
    pass
