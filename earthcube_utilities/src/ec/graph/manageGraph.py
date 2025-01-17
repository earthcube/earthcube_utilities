import requests
from string import Template
from abc import ABC, abstractmethod
import logging as log  #have some dgb prints, that will go to logs soon/but I find it slow to have to cat the small logs everytime
log.basicConfig(filename='mgraph.log', encoding='utf-8', level=log.DEBUG,
                format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

"""
Goal of manage graph is to allow for the creation deletion of namespaces, and the insertion of data
This is not a class to handle querying.

DEVELOPERS: 
USE TESTS... REPEAT USE TESTS.
in the tests folders, there is a managedgraph_test.py

REPEAT USE TESTS.
"""
class ManageGraph( ABC): #really a manage graph namespace, bc a graph has several of them, &this represents only one
    """ Abstract class for managing a Graph Store
     instance for a single namespace
    """
    baseurl = "http://localhost:3030" # basically fuskei
    namespace = "temp_summary"
    path = "namespace"
    sparql = "/sparql" # blazegraph uses sparql after namespace, but let's not assume this
    username=None
    password=None
    authorization=None
    def __init__(self, graphurl: str, namespace :str, username:str=None, password:str=None):
        """initialize a class for a namespace"""
        self.baseurl = graphurl
        self.namespace = namespace

        self.username = username
        self.password = password
        if self.username is not None and self.password is not None:
            self.authenticate(username, password)

    @abstractmethod
    def authenticate(self, username: str, password: str) -> bool:
        return NotImplemented
    @abstractmethod
    def graphFromEndpoint(endpoint: str) -> str:
        paths = endpoint.split('/')
        paths = paths[0:len(paths) -3]
        newurl = '/'.join(paths)
        return newurl
    @abstractmethod
    def createNamespace(self, quads=True):
        """ create a new namespace"""
        return NotImplemented

    @abstractmethod
    def deleteNamespace(self):
        """delete a namespace"""
        return NotImplemented

    @abstractmethod
    def loadReleaseFromUrl(self, url=None, source=None, namespace=None, suffix='release'):
        return NotImplemented

    # insert is private, i think
    @abstractmethod
    def insert(self, data, content_type="text/x-nquads"):
        return NotImplemented

    def upload_file(self, filename, content_type="text/x-nquads"):
        "to temp namespace or final one if given"
        log.debug(f'upload_file:{filename}')
        log.info(f'upload_file:{filename}')
        # open file and insert data
        data = open(filename, 'rb').read()
        log.debug(f'insert:{filename}')
        log.info(f'insert:{filename}')
        self.insert(data, content_type)

    def upload_nq_file(self, fn=None):
        "will default to ns.nq"
        if fn:
            filename = fn
        else:
            filename = self.namespace + ".nq"
        self.upload_file(filename)

    def upload_ttl_file(self, fn=None):
        "will default to ns.ttl"
        if fn:  # will want to upload ns=repo.ttl to ns=summary in the end
            filename = fn
        else:
            filename = self.namespace + ".ttl"
        self.upload_file(filename, 'Content-Type:text/x-turtle')
"""
Goal of manage graph is to allow for the creation deletion of namespaces, and the insertion of data
for a BLAZEGRAPH INSTANCE
This is not a class to handle querying.
"""
class ManageBlazegraph(ManageGraph):
    """ Manages a blazegraph instance for a single namespace
    implements needed portions of the blazegraph rest API"""

    createTemplateQuad ="""com.bigdata.namespace.fffff.spo.com.bigdata.btree.BTree.branchingFactor=1024
com.bigdata.rdf.store.AbstractTripleStore.textIndex=true
com.bigdata.namespace.fffff.lex.com.bigdata.btree.BTree.branchingFactor=400
com.bigdata.rdf.store.AbstractTripleStore.axiomsClass=com.bigdata.rdf.axioms.NoAxioms
com.bigdata.rdf.sail.isolatableIndices=false
com.bigdata.rdf.sail.truthMaintenance=false
com.bigdata.rdf.store.AbstractTripleStore.justify=false
com.bigdata.rdf.store.AbstractTripleStore.quads=true
com.bigdata.journal.Journal.groupCommit=false
com.bigdata.rdf.store.AbstractTripleStore.geoSpatial=false
com.bigdata.rdf.store.AbstractTripleStore.statementIdentifiers=false
"""

    createTemplateTriples = """com.bigdata.namespace.fffff.spo.com.bigdata.btree.BTree.branchingFactor=1024
com.bigdata.rdf.store.AbstractTripleStore.textIndex=true
com.bigdata.namespace.fffff.lex.com.bigdata.btree.BTree.branchingFactor=400
com.bigdata.rdf.store.AbstractTripleStore.axiomsClass=com.bigdata.rdf.axioms.NoAxioms
com.bigdata.rdf.sail.isolatableIndices=false
com.bigdata.rdf.sail.truthMaintenance=false
com.bigdata.rdf.store.AbstractTripleStore.justify=false
com.bigdata.rdf.sail.namespace=fffff
com.bigdata.rdf.store.AbstractTripleStore.quads=false
com.bigdata.journal.Journal.groupCommit=false
com.bigdata.rdf.store.AbstractTripleStore.geoSpatial=false
com.bigdata.rdf.store.AbstractTripleStore.statementIdentifiers=false
"""

    def authenticate(self, username: str, password: str) -> bool:
        return NotImplemented

    def GraphEndpoint(self, namespace):
        url = f"{self.baseurl}/namespace/{namespace}/sparql"
        return url
    #init w/namespace
    def graphFromEndpoint(endpoint: str) -> str:
        paths = endpoint.split('/')
        paths = paths[0:len(paths) -3]
        newurl = '/'.join(paths)
        return newurl
    def createNamespace(self, quads=True):
        """ Creates a new namespace"""
        # POST / bigdata / namespace
        # ...
        # Content - Type
        # ...
        # BODY
       # add this to the createTemplates
        # # com.bigdata.rdf.sail.namespace = {namespace}
        if quads:
            template = self.createTemplateQuad
        else:
            template = self.createTemplateTriples
        template = template + f"com.bigdata.rdf.sail.namespace = {self.namespace}\n"
        url = f"{self.baseurl}/namespace"
        headers = {"Content-Type": "text/plain"}
        r = requests.post(url,data=template, headers=headers)
        if r.status_code==201:
            return "Created"
        elif  r.status_code==409:
            return "Exists"
        else:
            raise Exception(f"Create Failed. Status code: {r.status_code} {r.reason}")


    def deleteNamespace(self):
        """ deletes a blazegraph namespace"""
        # DELETE /bigdata/namespace/NAMESPACE
        url = f"{self.baseurl}/namespace/{self.namespace}"
        headers = {"Content-Type": "text/plain"}
        r = requests.delete(url, headers=headers)
        if r.status_code == 200:
            return "Deleted"
        else:
            raise Exception("Delete Failed.")

    def loadReleaseFromUrl(self, url=None, source=None, namespace=None, suffix='release'):
        if url is None:
            raise ValueError("url must be provided")
        else:
            release_url = url
        if namespace is None:
            graphendpoint = self.GraphEndpoint()
        else:
            graphendpoint = self.GraphEndpoint(namespace=namespace)

        url = f"{graphendpoint}"  # f"{os.environ.get('GLEANER_GRAPH_URL')}/namespace/{os.environ.get('GLEANER_GRAPH_NAMESPACE')}/sparql?uri={release_url}"
        log.info(f'graph: insert "{source}" to {url} ')
        loadfrom = {'update': f'LOAD <{release_url}>'}
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        r = requests.post(url, headers=headers, data=loadfrom)
        log.debug(f' status:{r.status_code}')  # status:404
        log.info(f'graph: LOAD from {release_url}: status:{r.status_code}')
        if r.status_code == 200:
            log.info(f'graph load response: {str(r.text)} ')
            # '<?xml version="1.0"?><data modified="0" milliseconds="7"/>'
            if 'mutationCount=0' in r.text:
                log.info(f'graph: no data inserted ')
                # raise Exception("No Data Added: " + r.text)
            return True
        else:
            log.info(f'graph: error {str(r.text)} stauscode {r.status_code} {r.reason}')
            raise Exception(f' graph: failed,  LOAD from {release_url}: status:{r.status_code}')

    def insert(self, data, content_type="text/x-nquads"):
        """inserts data into a blazegraph namespace"""
        # rdf datatypes: https://github.com/blazegraph/database/wiki/REST_API#rdf-data
        # insert: https://github.com/blazegraph/database/wiki/REST_API#insert
       #url = f"{self.baseurl}/namespace/{self.namespace}{self.sparql}"
       #could call insure final slash
        url = f"{self.baseurl}/namespace/{self.namespace}/{self.sparql}"
        log.info(f'insert to {url} ')
        headers = {"Content-Type": f"{content_type}"}
        r = requests.post(url,data=data, headers=headers)
        log.debug(f' status:{r.status_code}') #status:404
        log.info(f' status:{r.status_code}') #status:404
        if r.status_code == 200:
            # '<?xml version="1.0"?><data modified="0" milliseconds="7"/>'
            if 'data modified="0"'  in r.text:
                raise Exception("No Data Added: " + r.text)
            return True
        else:
            return False

    #have upload methods here
    #have graph instance:<manageGraph.ManageBlazegraph object at ..>, for url:https://graph.geocodes.ncsa.illinois.edu/blazegraph
    #tmp_endpoint=f'https://graph.geocodes.ncsa.illinois.edu/blazegraph/namespace/{repo}/sparql'



class ManageGraphdb(ManageGraph):
    """ Manages a blazegraph instance for a single namespace
    implements needed portions of the blazegraph rest API"""

    createTemplateQuad ="""
# RDF4J configuration template for a GraphDB repository
#
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>.
@prefix rep: <http://www.openrdf.org/config/repository#>.
@prefix sr: <http://www.openrdf.org/config/repository/sail#>.
@prefix sail: <http://www.openrdf.org/config/sail#>.
@prefix graphdb: <http://www.ontotext.com/config/graphdb#>.

[] a rep:Repository ;
    rep:repositoryID "$REPO" ;
    rdfs:label "" ;
    rep:repositoryImpl [
        rep:repositoryType "graphdb:SailRepository" ;
        sr:sailImpl [
            sail:sailType "graphdb:Sail" ;

            graphdb:read-only "false" ;

            # Inference and Validation
            graphdb:ruleset "rdfsplus-optimized" ;
            graphdb:disable-sameAs "true" ;
            graphdb:check-for-inconsistencies "false" ;

            # Indexing
            graphdb:entity-id-size "40" ;
            graphdb:enable-context-index "true" ;
            graphdb:enablePredicateList "true" ;
            graphdb:enable-fts-index "true" ;
            graphdb:fts-indexes ("default" "iri") ;
            graphdb:fts-string-literals-index "default" ;
            graphdb:fts-iris-index "none" ;

            # Queries and Updates
            graphdb:query-timeout "0" ;
            graphdb:throw-QueryEvaluationException-on-timeout "false" ;
            graphdb:query-limit-results "0" ;

            # Settable in the file but otherwise hidden in the UI and in the RDF4J console
            graphdb:base-URL "http://example.org/owlim#" ;
            graphdb:defaultNS "" ;
            graphdb:imports "" ;
            graphdb:repository-type "file-repository" ;
            graphdb:storage-folder "storage" ;
            graphdb:entity-index-size "10000000" ;
            graphdb:in-memory-literal-properties "true" ;
            graphdb:enable-literal-index "true" ;
        ]
    ].
"""

    createTemplateTriples = """
#RDF4J configuration template for a GraphDB repository
#
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>.
@prefix rep: <http://www.openrdf.org/config/repository#>.
@prefix sr: <http://www.openrdf.org/config/repository/sail#>.
@prefix sail: <http://www.openrdf.org/config/sail#>.
@prefix graphdb: <http://www.ontotext.com/config/graphdb#>.

[] a rep:Repository ;
    rep:repositoryID "$REPO" ;
    rdfs:label "" ;
    rep:repositoryImpl [
        rep:repositoryType "graphdb:SailRepository" ;
        sr:sailImpl [
            sail:sailType "graphdb:Sail" ;

            graphdb:read-only "false" ;

            # Inference and Validation
            graphdb:ruleset "rdfsplus-optimized" ;
            graphdb:disable-sameAs "true" ;
            graphdb:check-for-inconsistencies "false" ;

            # Indexing
            graphdb:entity-id-size "40" ;
            graphdb:enable-context-index "true" ;
            graphdb:enablePredicateList "true" ;
            graphdb:enable-fts-index "true" ;
            graphdb:fts-indexes ("default" "iri") ;
            graphdb:fts-string-literals-index "default" ;
            graphdb:fts-iris-index "none" ;

            # Queries and Updates
            graphdb:query-timeout "0" ;
            graphdb:throw-QueryEvaluationException-on-timeout "false" ;
            graphdb:query-limit-results "0" ;

            # Settable in the file but otherwise hidden in the UI and in the RDF4J console
            graphdb:base-URL "http://example.org/owlim#" ;
            graphdb:defaultNS "" ;
            graphdb:imports "" ;
            graphdb:repository-type "file-repository" ;
            graphdb:storage-folder "storage" ;
            graphdb:entity-index-size "10000000" ;
            graphdb:in-memory-literal-properties "true" ;
            graphdb:enable-literal-index "true" ;
        ]
    ].
"""
    #init w/namespace
    def graphFromEndpoint(endpoint: str) -> str:
        paths = endpoint.split('/')
        paths = paths[0:len(paths) -3]
        newurl = '/'.join(paths)
        return newurl
    def authenticate(self, username: str, password: str) -> bool:
         """

       POST /rest/login/**
Example:

curl <base_url>/rest/login/<username> -X POST -H 'X-GraphDB-Password: <password>'
"""
         url = f"{self.baseurl}rest/login/{username}"
         headers = {"X-GraphDB-Password": f"{password}"}

         r = requests.post(url, headers=headers)
         if r.status_code == 200:
             self.authorization = r.headers['Authorization']
             return True
         else:
             raise Exception(f"failed to login. Status code: {r.status_code} {r.reason}")


    def GraphEndpoint(self, namespace):
        if namespace is None or namespace == '' :
            url = f"{self.baseurl}repositories/{self.namespace}/"
        else:
            url = f"{self.baseurl}repositories/{namespace}/"
        return url
    def createNamespace(self, quads=True):
        """ Creates a new namespace"""
        # POST / rest / repositories
        # Example:
        #
        # curl - X
        # POST < base_url > / rest / repositories?location = < encoded_location_uri > -H
        # 'Content-Type: multipart/form-data' - F
        # config =
        #
        # @
        #
        # < repo_ttl_config_filename >
       # add this to the createTemplates
        # # com.bigdata.rdf.sail.namespace = {namespace}
        if quads:
            template = Template(self.createTemplateQuad)
        else:
            template = Template(self.createTemplateTriples)
        template = template.safe_substitute(REPO=self.namespace)
        url = f"{self.baseurl}rest/repositories/"
        if self.authorization is  None:
            raise Exception("Autenticate")
        headers = {"Content-Type": "multipart/form-data", "Authorization": self.authorization}
        headers = {"Authorization": self.authorization}
        data = {"config":template}
        #r = requests.post(url,data=data, headers=headers)
        r = requests.post(url,files=data, headers=headers)

        if r.status_code==201:
            return "Created"
        elif  r.status_code==400:
            return "Exists"
        else:
            raise Exception(f"Create Failed. Status code: {r.status_code} {r.text} {r.reason}")


    def deleteNamespace(self):
        """ deletes a blazegraph namespace"""
        # Get
        # all
        # repositories in the
        # current or another
        # location
        #
        # GET / rest / repositories
        # DELETE / rest / repositories / < repo_id >
        # Example:
        #
        # curl - X
        # DELETE < base_url > / rest / repositories / < repo_id >?location = < encoded_location_uri >
        url = f"{self.baseurl}rest/repositories/{self.namespace}"
        headers = {"Content-Type": "text/plain", "Authorization": self.authorization}
        if self.authorization is  None:
            raise Exception("Autenticate")
        r = requests.delete(url, headers=headers)
        if r.status_code == 200:
            return "Deleted"
        else:
            raise Exception("Delete Failed.")

    def loadReleaseFromUrl(self, url=None, source=None, namespace=None, suffix='release'):
        if url is None:
            raise ValueError("url must be provided")
        else:
            release_url = url
        if namespace is None:
            graphendpoint = self.GraphEndpoint(None)
        else:
            graphendpoint = self.GraphEndpoint(namespace=namespace)

        url = f"{graphendpoint}statements"  # f"{os.environ.get('GLEANER_GRAPH_URL')}/namespace/{os.environ.get('GLEANER_GRAPH_NAMESPACE')}/sparql?uri={release_url}"
        log.info(f'graph: insert "{source}" to {url} ')
        loadfrom = {'update': f'LOAD <{release_url}>',
                    'infer': 'true',
                    'sameAs': 'true'
                    }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
           # 'Content-Type': 'application/x-turtle',
           # 'Content-Type': 'application/n-quads',
            "Authorization": self.authorization
        }
        r = requests.post(url, headers=headers, data=loadfrom)
        log.debug(f' status:{r.status_code}')  # status:404
        log.info(f'graph: LOAD from {release_url}: status:{r.status_code}')
        if r.status_code == 204:
            log.info(f'graph load response: {str(r.text)} ')

            return True
        else:
            log.info(f'graph: error {str(r.text)} stauscode {r.status_code} {r.reason}')
            raise Exception(f' graph: failed,  LOAD from {release_url}: status:{r.status_code}')

    def insert(self, data, content_type="text/x-nquads"):
        """inserts data into a blazegraph namespace"""

        #http://132.249.238.155/repositories/eco_quads
        #content-type:application/x-www-form-urlencoded;charset=UTF-8
        # ACCEPT: application/x-sparqlstar-results+json, application/sparql-results+json;q=0.9, */*;q=0.8
        # post formdata to the above url
        # PREFIX
        # geof: < http: // www.opengis.net /
        #
        # def /function / geosparql / >
        #
        # PREFIX
        # unit: < http: // www.opengis.net /
        #
        # def /uom / OGC / 1.0 / >
        #
        # PREFIX
        # schema: < https: // schema.org / >
        # PREFIX
        # rdfs: < http: // www.w3.org / 2000 / 01 / rdf - schema  # >
        #
        # SELECT ?observationDate ?depth ?s(?o as ?ufokn) ?building  ?impact_name ?impact_id
        # WHERE
        # {
        # ?s
        # a < https: // schema.org / Observation >.
        # ?s < https: // schema.org / measuredProperty > ?mpb.
        # ?mpb < https: // schema.org / identifier > "https://www.wikidata.org/wiki/Q8068".
        # ?s < https: // schema.org / value > "true".
        # ?s < https: // schema.org / observationAbout > ?o.
        # ?s < https: // schema.org / observationDate > ?observationDate.
        # ?o < https: // schema.org / identifier > ?building.
        # ?s < https: // schema.org / variableMeasured > ?vmb.
        # ?s < https: // schema.org / measuredProperty > ?mpb.
        # ?vmb < https: // schema.org / value > ?depth.
        # ?vmb < https: // schema.org / unitCode > ?depth_units.
        #
        # ?mpb < https: // schema.org / identifier > ?impact_id.
        # ?mpb < https: // schema.org / name > ?impact_name
        #
        # } limit
        # 5
        # infer: true
        # sameAs: true
        # limit: 1001
        # offset: 0
        # rdf datatypes: https://github.com/blazegraph/database/wiki/REST_API#rdf-data
        # insert: https://github.com/blazegraph/database/wiki/REST_API#insert
       #url = f"{self.baseurl}/namespace/{self.namespace}{self.sparql}"
       #could call insure final slash
        url = f"{self.baseurl}repositories/{self.namespace}/statements"
        log.info(f'insert to {url} ')
        headers = {"Content-Type": f"{content_type}", "Authorization": self.authorization}
        r = requests.post(url,data=data, headers=headers)
        log.debug(f' status:{r.status_code}') #status:404
        log.info(f' status:{r.status_code}') #status:404
        if r.status_code == 200 or r.status_code == 204:
            return True
        else:
            return False



