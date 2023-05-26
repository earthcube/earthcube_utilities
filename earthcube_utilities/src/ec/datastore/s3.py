from datetime import datetime
from io import BytesIO

import minio
import pydash
from minio.commonconfig import CopySource, REPLACE
from pydash.collections import find

def shaFroms3Path(path, extension=None):
    split = path.split("/")
    sha = split[len(split)-1]
    if extension is not None:
        sha = pydash.strings.replace_end(sha, extension, '')
    return sha


"""
Basic abstraction, in case someone want to store files in a 
different method
"""
class bucketDatastore():
    endpoint = "http://localhost:9000" # basically minio
    options = {}
    default_bucket="gleaner"
    paths = {"report":"reports",
             "summon": "summoned",
             "milled":"milled",
             "graph":"graphs",
             "archive":"archive",
             "collection":"collections",
             "sitemap":"sitemaps"
    }

    def __init__(self, s3endpoint, options, default_bucket="gleaner"):
        self.endpoint = s3endpoint
        self.options = options
        self.default_bucket = default_bucket

    def listPath(self, bucket, path, include_user_meta=False):
        pass
    def countPath(self, bucket, path):
        count = len(list(self.listPath(bucket,path)))
        return count

# who knows, we might implement on disk, or in a database. This just separates the data from the annotated metadata
    def getFileFromStore(self, s3ObjectInfo):
        pass
    def getFileMetadataFromStore(self, s3ObjectInfo):
        pass
    def putTextFileToStore(self,data, s3ObjectInfo ):
        f = BytesIO()
        length = f.write(bytes(data, 'utf-8'))
        f.seek(0)
        resp = self.s3client.put_object(s3ObjectInfo.bucket_name, s3ObjectInfo.object_name, f,length=length)
        return resp.bucket_name, resp.object_name
    def copyObject(self,s3ObjectInfoToCopy, ObjectPath ):
        ''' Server Side Copy, eg upload report to latest, make copy to today'''
        self.s3client.copy_object(
            s3ObjectInfoToCopy.bucket_name,
            ObjectPath,
            CopySource(s3ObjectInfoToCopy.bucket_name, s3ObjectInfoToCopy.object_name),
           # metadata=metadata,
            metadata_directive=REPLACE,
        )

    #### Methods for a getting information using infrastructure information

    """ Method for gleaner store"""
    def listJsonld(self,bucket, repo,include_user_meta=False):
        """ urllist returns list of urn;s with urls"""
        # include user meta not working.
        path = f"{self.paths['summon']}/{repo}/"
        return self.listPath(bucket, path,include_user_meta=include_user_meta)

    def countJsonld(self,bucket, repo) -> int:
        count = len(list(self.listJsonld(bucket,repo)))
        return count

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
    def listSummonedSha(self,bucket, repo):
        """  returns list of urns with urls"""
        jsonlds = self.listJsonld(bucket, repo, include_user_meta=False)
        objs = map(lambda f: shaFroms3Path( f.object_name, extension=".jsonld"), jsonlds)
        # for ob in objs:
        #     print(ob)
        o_list = list(objs)
        return o_list

    def getJsonLDMetadata(self, bucket, repo, sha):
        path = f"{self.paths['summon']}/{repo}/{sha}.jsonld"
        s3ObjectInfo = {"bucket_name": bucket, "object_name": path}
        tags = self.getFileMetadataFromStore(s3ObjectInfo)

        return tags

    def getOringalUrl(self, bucket, repo, sha) -> str:
        md = self.getJsonLDMetadata(bucket, repo, sha)
        return md['Url']

    '''Cleans the name of slashes... might need more in the future.'''
    def getCleanObjectName(s3ObjectName) -> str:
        return s3ObjectName.replace('/','__')

    def listMilledRdf(self,bucket, repo,urnonly=False):
        path = f"{self.paths['milled']}/{repo}/"
        return self.listPath(bucket, path)
    def listMilledSha(self,bucket, repo,urnonly=False):
        paths = self.listMilledRdf(bucket,repo)
        shas = list(map(lambda p: shaFroms3Path(p.object_name, extension=".rdf"), paths))
        return shas

    def countMilledRdf(self,bucket, repo) -> int:
        count = len(list(self.listMilledRdf(bucket,repo)))
        return count
    ### methods for reporting
    '''
    Reporting will have to pull the original and put back to the datastore
    '''

    def listReportFile(self,bucket, repo,include_user_meta=False):
        """ urllist returns list of urn;s with urls"""
        # include user meta not working.
        path = f"{self.paths['report']}/{repo}/"
        return self.listPath(bucket, path,include_user_meta=include_user_meta)

    def putReportFile(self, bucket, repo, filename, json_str,  date="latest", copy_to_date=True):

        pass

    def getReportFile(self, bucket, repo, filename):
        path = f"{self.paths['report']}/{repo}/filename"
        s3ObjectInfo = {"bucket_name": bucket, "object_name": path}
        resp = self.getFileFromStore(s3ObjectInfo)
        return resp

    def getLatestRelaseUrl(self, bucket, repo):

        pass

    def getLatestRelaseUrls(self, bucket):

        pass

    def getRoCrateFile(self, filename, bucket="gleaner", user="public"):
        path = f"{self.paths['crate']}/{user}/{filename}"
        s3ObjectInfo = {"bucket_name": bucket, "object_name": path}
        resp = self.getFileFromStore(s3ObjectInfo)
        return resp

    def putRoCrateFile(self, data: str,filename, bucket="gleaner", user="public"):
        path = f"{self.paths['report']}/{user}/{filename}"
        s3ObjectInfo = {"bucket_name": bucket, "object_name": path}
        return self.putTextFileToStore(data, s3ObjectInfo)

    def getSitemapFile(self,bucket, repo, filename):
        path = f"{self.paths['sitemap']}/{repo}/filename"
        s3ObjectInfo = {"bucket_name": bucket, "object_name": path}
        resp = self.getFileFromStore(s3ObjectInfo)
        return resp

    def putSitemapFile(self,data: str, repo: str,filename: str, bucket="gleaner"):
        path = f"{self.paths['sitemap']}/{repo}/{filename}"
        s3ObjectInfo = {"bucket_name": bucket, "object_name": path}
        return self.putTextFileToStore(data, s3ObjectInfo)

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
        resp = self.s3client.list_objects(bucket, path, include_user_meta=include_user_meta, recursive=True)
        # the returned list includes the path
        #o_list = list(resp)
        o_list = filter(lambda f: f.object_name != path, resp)
        return o_list

    def countPath(self, bucket, path):
        count = len(list(self.listPath(bucket, path)))
        return count

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

    def putReportFile(self, bucket, repo, filename, json_str, date="latest", copy_to_date=True):
        path = f"{self.paths['report']}/{repo}/{date}/{filename}"
        f = BytesIO()
        length = f.write(bytes(json_str, 'utf-8'))
        f.seek(0)
        resp = self.s3client.put_object(bucket, path, f,length=length)
        if copy_to_date:
            today_str = datetime.now().strftime("%Y%m%d")
            path = f"{self.paths['report']}/{repo}/{today_str}/{filename}"
            self.copyObject(resp,path)
        return resp.bucket_name, resp.object_name

    def getReportFile(self, bucket, repo, filename):
        path = f"{self.paths['report']}/{repo}/{filename}"
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
        path = f"/{self.paths['collection']}/{user}/{filename}"
        crate = self.s3client.get_object(bucket, path)
        return crate

