import requests
import logging as log  #have some dgb prints, that will go to logs soon/but I find it slow to have to cat the small logs everytime
log.basicConfig(filename='mgraph.log', encoding='utf-8', level=log.DEBUG,
                format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

"""
Goal of manage graph is to allow for the creation deletion of namespaces, and the insertion of data
This is not a class to handle querying.
"""
class ManageGraph: #really a manage graph namespace, bc a graph has several of them, &this represents only one
    """ Abstract class for managing a Graph Store
     instance for a single namespace
    """
    baseurl = "http://localhost:3030" # basically fuskei
    namespace = "temp_summary"
    path = "namespace"
    sparql = "/sparql" # blazegraph uses sparql after namespace, but let's not assume this

    def __init__(self, graphurl, namespace):
        """initialize a class for a namespace"""
        self.baseurl = graphurl
        self.namespace = namespace

    def createNamespace(self, quads=True):
        """ create a new namespace"""
        pass

    def deleteNamespace(self):
        """delete a namespace"""
        pass

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
    #init w/namespace

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
            raise Exception("Create Failed.")


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

    def upload_file(self, filename, content_type="text/x-nquads"):
        "to temp namespace or final one if given"
        log.debug(f'upload_file:{filename}')
        log.info(f'upload_file:{filename}')
        #open file and insert data
        data = open(filename, 'rb').read()
        log.debug(f'insert:{filename}')
        log.info(f'insert:{filename}')
        self.insert(data, content_type)

    def upload_nq_file(self, fn=None):
        "will default to ns.nq"
        if fn:
            filename=fn
        else:
            filename=self.namespace + ".nq"
        self.upload_file(filename)

    def upload_ttl_file(self, fn=None):
        "will default to ns.ttl"
        if fn: #will want to upload ns=repo.ttl to ns=summary in the end
            filename=fn
        else:
            filename=self.namespace + ".ttl"
        self.upload_file(filename, 'Content-Type:text/x-turtle')

