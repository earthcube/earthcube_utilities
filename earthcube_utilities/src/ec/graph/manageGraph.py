import requests
import logging

class ManageGraph: #really a manage graph namespace, bc a graph has several of them, &this represents only one
    baseurl = "http://localhost:3030" # basically fuskei
    namespace = "temp_summary"
    path = "namespace"
    sparql = "sparql"

    def __init__(self, graphurl, namespace):
        self.baseurl = graphurl
        self.namespace = namespace

    def createNamespace(self, quads=True):
        pass

    def deleteNamespace(self):
        pass

class ManageBlazegraph(ManageGraph):

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
            return True
        else:
            return False


    def deleteNamespace(self):
        # DELETE /bigdata/namespace/NAMESPACE
        url = f"{self.baseurl}/namespace/{self.namespace}"
        headers = {"Content-Type": "text/plain"}
        r = requests.delete(url, headers=headers)
        if r.status_code == 200:
            return True
        else:
            return False
        pass

    def insert(self, data, content_type="text/x-nquads"):
        # rdf datatypes: https://github.com/blazegraph/database/wiki/REST_API#rdf-data
        # insert: https://github.com/blazegraph/database/wiki/REST_API#insert
        url = f"{self.baseurl}/namespace/{self.namespace}{self.sparql}"
        headers = {"Content-Type": f"{content_type}"}
        r = requests.post(url,data=data, headers=headers)
        if r.status_code == 200:
            # '<?xml version="1.0"?><data modified="0" milliseconds="7"/>'
            if 'data modified="0"'  in r.text:
                raise Exception("No Data Added: " + r.text)
            return True
        else:
            return False
        
    #might still have upload methods here

    #def upload_file(self, filename, namespace=None, content_type="text/x-nquads"):
    def upload_file(self, filename, content_type="text/x-nquads"):
        "to temp namespace or final one if given"
        print(f'upload_file:{filename}')
    #   if namespace:
    #       ns=namespace
    #   else: #best to use the instance's namespace
    #       ns=self.namespace
        #could open file and insert data
        with open(filename, 'rb+') as f:   
            lines = f.read()
            print(f'insert:{filename}')
            self.insert(f, content_type)

    #def upload_nq_file(self, ns="summary"): #this would be for final ttl upload, &I would just pass it in
    def upload_nq_file(self, fn=None):
        "will default to ns.nq"
        if fn:
            filename=fn
        else:
            filename=self.namespace + ".nq"
        self.upload_file(filename)

    def upload_ttl_file(self, fn=None):
        "will default to ns.ttl"
   #def upload_ttl_file(self, ns=None, fn=None):
   #    if ns:
   #        namespace=ns
   #    else:
   #        namespace=self.namespace
        if fn: #will want to upload ns=repo.ttl to ns=summary in the end
            filename=fn
        else:
            filename=self.namespace + ".ttl"
        self.upload_file(filename, 'Content-Type:text/x-turtle')

#will instantiange a graph/namespace instance in summarize code to do the logic below
    # an instance of this is made, 
    #don't have to anymore assume: w/the namespace=repo as one of it's instatiation args
#   def call_summarize(self):
#       print(f'call tsum on:{self.namespace}')

#   def summarize(self, ns="summary"):
#       self.createNamespace()
#       self.upload_nq_file()
#       self.call_summarize() #creates repo.ttl
#       self.deleteNamespace()
#       self.upload_ttl_file(ns)  #uploads it
