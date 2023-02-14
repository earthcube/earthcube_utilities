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

    #might still have upload methods here

    def upload_file(self, filename, namespace=None):
        "to temp namespace or final one if given"
        print(f'upload:{filename}')
        if namespace:
            ns=namespace
        else:
            ns=self.namespace

    def upload_nq_file(self, ns="summary"):
        filename=self.namespace + ".nq"
        self.upload_file(filename,ns)

    def upload_ttl_file(self):
        filename=self.namespace + ".ttl"
        self.upload_file(filename)

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
