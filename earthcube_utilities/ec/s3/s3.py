from io import BytesIO

import minio

"""
Basic abstraction, in case someone want to store files in a 
different method
"""
class bucketDatastore():
    endpoint = "http://localhost:9000" # basically minio
    options = {}
    paths = {"reports":"reports",
             "summon": "summoned",
             "milled":"milled",
             "graph":"graph",
             "archive":"archive"
    }

    def __init__(self, s3endpoint, options):
        self.endpoint = s3endpoint
        self.options = options

    def listPath(self, bucket, path):
        pass
    def countPath(self, bucket, path):
        count = len(list(self.listRepo(bucket,path)))


    def getFileFromStore(self, s3ObjectInfo):
        pass
    def getFileMetadataFromStore(self, s3ObjectInfo):
        pass

    #### Methods for a getting information using infrastructure information

    """ Method for gleaner store"""
    def listJsonld(self,bucket, repo):
        pass
    def countJsonld(self,bucket, repo):
        count = len(list(self.listJsonld(bucket,repo)))
    def getJsonLD(self, repo, urn):
        pass
    def getJsonLDMetadata(self, bucket, repo, urn):
        pass

    '''Cleans the name of slashes... might need more in the future.'''
    def getCleanObjectName(s3ObjectName):
        return s3ObjectName.replace('/','_')

    ### methods for reporting
    '''
    Reporting will have to pull the original and put back to the datastore
    '''

    def putReportFile(self, bucket, repo, filename):
        pass

    def getReportFile(self, bucket, repo, filename):
        pass


"""
Basic abstraction, in case someone want to store files in a 
different method
"""
class MinioDatastore(bucketDatastore):

    def __init__(self, s3endpoint, options):
        self.endpoint = s3endpoint
        self.options = options
        self.s3client  =minio.Minio(s3endpoint) # this will neeed to be fixed with authentication

    def getFileFromStore(self, s3ObjectInfo):
        resp = self.s3client.get_object(s3ObjectInfo.bucket_name, s3ObjectInfo.object_name)
        return resp.data

    def putReportFile(self, bucket, repo, filename, json_str):
        path = f"/{self.paths['reports']}/{repo}/{filename}"
        f = BytesIO()
        length = f.write(bytes(json_str, 'utf-8'))
        f.seek(0)
        resp = self.s3client.put_object(bucket, path, f,length=length)
        return resp.bucket_name, resp.object_name

    def getReportFile(self, bucket, repo, filename):
        pass