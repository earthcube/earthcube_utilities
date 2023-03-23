from ec.objects.ecobjectmanager import EcObjectManager

def get_from_geocodes(urn, endpoint="https://graph.geocodes-dev.earthcube.org/blazegraph/namespace/earthcube/sparql"):
    """get an object from the graph, and return as a JSON-LD file """
    manager = EcObjectManager(endpoint, None, None)
    return manager.getFromStore(urn, source='graph', form='jsonld')