from ec.objects.ec_object_manager import ec_object_manager

def get_from_geocodes(urn, endpoint="https://graph.geocodes-dev.earthcube.org/blazegraph/namespace/earthcube/"):
    manager = ec_object_manager(endpoint, None, None)
    return manager.getFromStore(urn, source='graph', form='jsonld')