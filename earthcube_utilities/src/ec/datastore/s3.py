from io import BytesIO

import minio
import pydash
from pydash.collections import find

def shaFroms3Path(path):
    split = path.split()
    return split[len(split)-1]


"""
Basic abstraction, in case someone want to store files in a 
different method
"""
class bucketDatastore():
    endpoint = "http://localhost:9000" # basically minio
    options = {}
    default_bucket="gleaner"
    paths = {"reports":"reports",
             "summon": "summoned",
             "milled":"milled",
             "graph":"graphs",
             "archive":"archive",
             "collections":"collections"
    }

    def __init__(self, s3endpoint, options, default_bucket="gleaner"):
        self.endpoint = s3endpoint
        self.options = options
        self.default_bucket = default_bucket

    def listPath(self, bucket, path, include_user_meta=False):
        pass
    def countPath(self, bucket, path):
        count = len(list(self.listPath(bucket,path)))

# who knows, we might implement on disk, or in a database. This just separates the data from the annotated metadata
    def getFileFromStore(self, s3ObjectInfo):
        pass
    def getFileMetadataFromStore(self, s3ObjectInfo):
        pass

    #### Methods for a getting information using infrastructure information

    """ Method for gleaner store"""
    def listJsonld(self,bucket, repo,include_user_meta=False):
        """ urllist returns list of urn;s with urls"""
        # include user meta not working.
        path = f"{self.paths['summon']}/{repo}/"
        return self.listPath(bucket, path,include_user_meta=include_user_meta)

    def countJsonld(self,bucket, repo):
        count = len(list(self.listJsonld(bucket,repo)))

    def getJsonLD(self, bucket, repo, sha):
        path = f"{self.paths['summon']}/{repo}/{sha}.jsonld"
        s3ObjectInfo = {"bucket_name": bucket, "object_name": path}
        resp = self.getFileFromStore(s3ObjectInfo)
        return resp
    def listSummonedUrls(self,bucket, repo):
        """  returns list of urns with urls"""
        jsonlds = self.listJsonld(bucket, repo, include_user_meta=True)
        objs = map(lambda f: self.s3client.stat_object(f.bucket_name, f.object_name), jsonlds)
        # for ob in objs:
        #     print(ob)
        o_list = list(map(lambda f: {"sha": shaFroms3Path(f.object_name), "url": f.metadata["X-Amz-Meta-Url"]}, objs))
        return o_list

    def getJsonLDMetadata(self, bucket, repo, sha):
        path = f"{self.paths['summon']}/{repo}/{sha}.jsonld"
        s3ObjectInfo = {"bucket_name": bucket, "object_name": path}
        tags = self.getFileMetadataFromStore(s3ObjectInfo)

        return tags

    def getOringalUrl(self, bucket, repo, sha):
        md = self.getJsonLDMetadata(bucket, repo, sha)
        return md['Url']

    '''Cleans the name of slashes... might need more in the future.'''
    def getCleanObjectName(s3ObjectName):
        return s3ObjectName.replace('/','__')

    def listMilledRdf(self,bucket, repo,urnonly=False):
        path = f"{self.paths['milled']}/{repo}/"
        return self.listPath(bucket, path)

    def countMilledRdf(self,bucket, repo):
        count = len(list(self.listMilledRdf(bucket,repo)))
    ### methods for reporting
    '''
    Reporting will have to pull the original and put back to the datastore
    '''

    def putReportFile(self, bucket, repo, filename, json_str, date="latest"):
        pass

    def getReportFile(self, bucket, repo, filename):
        pass

    def getLatestRelaseUrl(self, bucket, repo):

        pass

    def getLatestRelaseUrls(self, bucket):

        pass

    def getRoCrateFile(self, filename, bucket="gleaner", user="public"):
        pass
    def putRoCrateFile(self, filename, bucket="gleaner", user="public"):
        pass

"""
Basic abstraction, in case someone want to store files in a 
different method
"""
class MinioDatastore(bucketDatastore):
    """ Instance of a minio datastore with utility methods to retreive information"""
    def __init__(self, s3endpoint, options,default_bucket="gleaner"):
        """ Initilize with
        Parameters:
            s3endpoint: endpoint. If this is aws, include the region. eg s3.us-west-2.amazon....
            options: creditials, other parameters to pass to client
            default_bucket: 'gleaner'
            """
        self.endpoint = s3endpoint
        self.options = options
        self.default_bucket= default_bucket
        self.s3client  =minio.Minio(s3endpoint) # this will neeed to be fixed with authentication


    def listPath(self, bucket, path, include_user_meta=False):
        """ returns the filelist for a path with the starting path removed from the list"""
        resp = self.s3client.list_objects(bucket, path, include_user_meta=include_user_meta)
        # the returned list includes the path
        #o_list = list(resp)
        o_list = filter(lambda f: f.object_name != path, resp)
        return o_list

    def getFileFromStore(self, s3ObjectInfo):
        """ get an s3 file from teh store
        Parameters:
          s3ObjectInfo: {"bucket_name":obj.bucket_name, "object_name":obj.object_name }

        """
        resp = self.s3client.get_object(s3ObjectInfo["bucket_name"], s3ObjectInfo["object_name"])
        return resp.data

    def getFileMetadataFromStore(self, s3ObjectInfo):
        """ get metadata s3 file from teh store
               Parameters:
                 s3ObjectInfo: {"bucket_name":obj.bucket_name, "object_name":obj.object_name }

               """
        s3obj = self.s3client.stat_object(s3ObjectInfo.bucket_name, s3ObjectInfo.object_name)
        for o in s3obj:
            user_meta = pydash.collections.filter_(o,lambda m: m.startswith("X-Amz-Meta") )
        # this needs to return the metadata
        return user_meta

    def putReportFile(self, bucket, repo, filename, json_str, date="latest"):
        path = f"{self.paths['reports']}/{repo}/{date}/{filename}"
        f = BytesIO()
        length = f.write(bytes(json_str, 'utf-8'))
        f.seek(0)
        resp = self.s3client.put_object(bucket, path, f,length=length)
        return resp.bucket_name, resp.object_name

    def getReportFile(self, bucket, repo, filename):
        path = f"{self.paths['reports']}/{repo}/{filename}"
        s3ObjectInfo = {"bucket_name": bucket, "object_name": path}
        resp = self.getFileFromStore(s3ObjectInfo)
        return resp

    def getLatestRelaseFile(self, bucket, repo):
        path = f"{self.paths['graph']}/latest/summonded{repo}_latest_release.nq"
        s3ObjectInfo = {"bucket_name":bucket,"object_name": path}
        resp = self.getFileFromStore(s3ObjectInfo)
        return resp

    def getRelasePaths(self, bucket):
        path = f"{self.paths['graph']}/latest/"
        files = self.listPath(bucket, path)
        paths = list(map(lambda f:  f.object_name, files))
        return paths

    def getRoCrateFile(self, filename, bucket="gleaner", user="public"):
        path = f"/{self.paths['collections']}/{user}/{filename}"
        crate = self.s3client.get_object(bucket, path)
        return crate

    def putRoCrateFile(self, filename, bucket="gleaner", user="public"):
        path = f"/{self.paths['collections']}/{user}/{filename}"
        s3ObjectInfo = {"bucket_name": bucket, "object_name": path}
        crate = self.getFileFromStore(s3ObjectInfo)
        return crate