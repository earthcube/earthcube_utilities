# utlities to manipulate Science on Schema JSONLD 

## functionality

## Methods
### manipulate jsonld
```python
def validJson(jsonld):
def validToSpec(jsonld, spec="ec_sos"):
def basicInfo(jsonld): # name, identifier
def distributions(jsonld, formats=["all"]): # return a link
```

### From Graphstore: 
is this a good idea
```python
class EC_Graphstore:
    def __init__(self, config):
    def getObject(self, urn): # object as defined by gleanerio, aka loaded rdf
    def getDistributions(self, urn, format=["all"]):
    def getIdentifiers(self, urn, type=None): # none return all
def validToSpec(jsonld, spec="ec_sos"):
def basicInfo(jsonld): # name, identifier
def distributions(jsonld, formats=["all"]): # return a link
```