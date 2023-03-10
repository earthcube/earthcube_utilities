### RDF to triples
At present, gleaner generates triples, and nabu loads them into the graph as quads.
The summary code needs to know the expected `graph` so this module creates quads from gleaner/milled
Basically, <ins>**rdf2nq.py** takes one form of rdf triples, 
and adds the filename of the file as the last column in its nquads<ins> output
* if it is .ntriples, then you just add a column
* if it is another format like jsonld, then it runs jena's riot RDF I/O technology (RIOT) on it, right now
```shell
rdf2nq.py nabuconfig repository --path (default=milled)
```
The config contains the service secrets, and more importantly the source 'repository' will be in the file.
```python
def s3client(config)
def s3GetFile(s3client, file )
def read_files(s3client, bucket, repo)
def triplesToQuads(triples, graphname)
def appeandToOutput(quads)
def pathToUrn(file) 
   # the path should be summoned/repo/urn.jsonld
   # remove json or jsonld from s3 path
   # returns urn in for urn:repo:file sans extenstion
def __main__
  s3 = s3Client(config)
  files = read_files(s3, config.s3.bucket, repo)
  foreach file in files:
     urn = pathToUrn(file)
     data = s3GetFile(s3client, file.path) # whatever it needs
     quads = triplesToQuads(data, urn)
     appendToOutput(quads)
  outputfile.write() 
```


_Some related could probably be handled by [kglab](https://derwen.ai/docs/kgl/ex4_0/) now_
