# Validation Overview

There are several parts to the system that need to be validated
* [Sitemap](./validation_sitemap.md)
  * sitemap exist
  * can we access the urls in the sitemap
  * Do documents we 'summoned' have jsonld
  * counts
     * how many url's in sitemap
     * how many not 200.
* [JSONLD](./validation_jsonld.md)
  * Is jsonld valid json
  * does it have correct context, etc (this is presently fixed by gleaner but needs to be reported, somehow)
  * Is it a valid JSONLD Dataset? Use a shacl shape to test.
  * Counts
     * how many jsonld files made in into s3
* [Graph ](./validation_graph.md) Converting to RDF and loading to graph
* Did jsonld convert in ways we expected? This is tough, but we need to try to find a quick measure

There also needs to be an implementaiton set of tests that works with a small set of known 
data that we evaluation and know when something unexpected happens.
We we get a quirky jsonld. we need to add it to the test dataset.


## Some methods:

This is just some overall brain dump of possible methods that might be useful.
There should be more details in each validation document.

### Dataloading

When gleaner pushes data into the s3 instance, then an identifier is created

`urn:repo:id`

Previous patterns included the bucket and the
we avoid using slashes and hashes because that can be problematic with url parsing

`urn:bucket:path:repo:id`

eg

`urn:bucket:summoned:repo:id`

#### Methods
```python
def parseLogForErrors(file):
```
### Sitemaps
```python
class SiteMap():
  def __init__(self, url):
  def validSiteMap():
  def siteMapCount():
  def testUrls(sample=0): # 0 = all
    return {"count": 0, "status":{"200":0, "400":0}}
```

### s3
```python
class S3client():
  def __init__(self, config):
  def s3GetFile(self, file ):
  def s3CountFilesInRepo(self, repo, base='summoned'):
  def s3UrnFromPath(filepath):
  def s3RepoFromPath(filepath):
  def subSampleFileList(self, random=False, subsample=0): # return a subset 
  def  uploadFile(self, file, contenttype, etc):
```
Do we want to classify the s3 functionality, and be able to use self?

### JSONLD


#### Methods
```python
def repoCountJson(s3client, repo, base='summoned'): # courtsey function fo s3CountFilesInRepo
def possibleMissingJsonLoad(s3client, sitemap, repo):
def jsonldFormatGuess(file):  #is is expaded, flattend, compact
def validateJson( file):
def validatedContext( file):
def validateJsonSchema(file, schema="sos":
def validateUsingShacl( file, shacl="sos_earthcube"):
```

Need a listing of shacl shapes

### Graph
```python
class manageGraph():
  def __init__(self, graphurl, namespace ):
  def countGraphs(self, repo=None): # if not give entire count, otherwise fancy search for urn:repo
  def getItem(self, urn):
  def getItemsStats(self, urn): # return line count, and other information.
  def compareGraph2s3Jsonstore(self, s3config, repo):  # nabu prune has example

```

## Save to
code to save results to someplace we can keep track of them.

## Quick validation.
do numbers match

jsonld>graph count

Store counts in github/repository/s3

did counts change?


|     | Sitemap         | JSON-LD Count | Milled Count from s3 | Graph Count from Triplestore |
| ---- | -------------   | --------------| -------------------- | ---------------------------- |
| count | {sitemap:count} | {summon:count} | {nabu: milled} | {graph: count} |
| errors | {sitemap:errors} | {summon:errors} | {nabu: errors}  | {graph: errors} |
| loss |  |  |  |  |
