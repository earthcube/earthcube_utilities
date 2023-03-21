
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

def compareSummoned2Milled(bucket, repo):
    """ return list of missing urls"""
    pass

def compareSummoned2Graph(bucket, repo):
    pass