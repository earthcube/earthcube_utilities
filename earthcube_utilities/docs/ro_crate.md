### RO-CRATE creation
 [RO-Crate issue](https://github.com/earthcube/earthcube_utilities/issues/15) decribes some of the steps needed

**Development happening in:** https://github.com/earthcube/earthcube_utilities/tree/dev_16_nb


The [Notebook Dispatch](https://docs.google.com/document/d/1dIusvhpbJuN7HC8smPPGbn9HIWJGsN7iZafKTRTc42I/edit#heading=h.1izdmil74wk6) describes the possible functionality 

The [Decoder Sprint Document](https://docs.google.com/document/d/1PSPPp3M3OJFUbLPr3zW1Xnt4uQuo-Oruwuh2LqN2yxE/edit#heading=h.muip1py2h08a) includes a diagram of how we might immplement RO-Crate workflows

```python
def s3client(): # public bucket
def s3getFile(s3client, pathToCrate):
def s3PathToRoctate(roCrateQueryParameter):
def roCrateRender(rocrate):
def roCrateGetCollection(rocrate)
def roCrateGetObjectFromJsonLdStore(s3clinet, collectionItem)
def roCrateGetObject(graphstore, collectionItem)
```

```python
roCrateQueryParameter = request.params.rocrate
s3 = s3client()
pathToCrate = s3PathToRocrate(roCrateQueryParameter)
rocrate = s3getFile(s3,pathToCrate)
print(roCrateRender(rocrate))
```
