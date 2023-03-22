import logging

import pyld.jsonld
import rdflib

from  ec.sos_json.rdf import get_rdfgraph
import utils

class ec_object_manager():
    datastore = None
    bucket=None

    graphendpoint = None
    def __init(self,  graphsendpoint, datastore,bucket):
        self.graphendpoint = graphsendpoint
        self.datastore = datastore
        self.bucket=bucket

    # Thinking this could be
    #  form= pyld
    # forrm = rdflib
    # form = somthing easy to add to a pandas dataframe?
    def getFromStore(self, urn, source='graph', form='rdflib'):

        if  source is 'datastore':
            logging.debug('datastore')
            self.json_obj = self._getFromDatastore(urn)
        else:
            logging.debug('default, graph')
            self.graph_obj = self._getFromGraphstore(urn)
#####

        if  form is  'jsonld':
            logging.debug('jsonld')
            if self.json_obj is not None:
                return self.json_obj
            else:
                logging.debug('need to convert')
                # not sure how nquads will be handled. know it can only be loaded as RDFlb Dataset...
                #options={"format":  'application/n-quads',"processingMode": 'json-ld-1.1'}
                options = { "processingMode": 'json-ld-1.1'}
                rdf_str = pyld.jsonld.to_rdf(self.json_obj, options=options)
                g = rdflib.Graph()
                g.parse(data=rdf_str)
                return g

        elif source is 'rdflib':
            logging.debug('rdflib')
            if self.graph_obj is not None:
                return self.graph_obj
            else:
                return self.graph_obj.serialize(format="json-ld")

        else:
             logging.debug('default, pyld')

####
    def _getFromDatastore(self, urn):
        client = self.datastore
        # pull the repo from the urn
        identifier = utils.parts_from_urn(urn)
        return client.getJsonLD(self.bucket,identifier.id, identifier.repo )


    def _getFromGraphstore(self, urn):
        return get_rdfgraph(urn, self.graphendpoint)

    #####

