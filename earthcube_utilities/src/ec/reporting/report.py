
class TimeSeriesCount():
    #date
    #hashmap

    def toJson(self):
        pass
    def fromJson(self):
        pass

class History():
    item = ''
    date = None


class Repository():
    name = ''
    # TimeSeriesCount( sitemap, jsonld, graphcount, datasetcount, totaltriplecount )

    # for each one of graphtype and keyword will be an array of timeseries.
    graphtypes = TimeSeriesCount()
    keywords = TimeSeriesCount()

    def GetReport(self,bucket, repo):
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

def graphTypes4Repo(repo, graphendpoint):
    #queryWithSparql("repo_count_types", graphendpoint)
    pass

def getGraphTypes4RepoReport(repo, datastore):
    pass
def putGraphTypes4RepoReport(repo, datastore):
    pass
def updateGraphTypes4RepoReport(repo, datastore):
    pass
def graphKeywordsRepo(repo, graphendpoint):
    #queryWithSparql("repo_count_keywords", graphendpoint)
    pass

def graphKeywords4RepoReport(repo, datastore):
    pass

def putGraphKeywords4RepoReport(repo, datastore):
    pass
def updateGraphKeywords4RepoReport(repo, datastore):
    pass