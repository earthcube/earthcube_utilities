
class ec_object():
    schematype='Dataset'
    schema_obj = None # pyld object

    # need to have a frame
    def __init__(self, urn, object_manager,schematype='Dataset'):
        self.schematype = schematype


    def to_rdf_graph(self):
        pass
    def to_rdf_dataset(self):
        pass

    def to_nquads(self):
        pass
    def to_jsonld(self, form='frame'):
        pass