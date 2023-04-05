# Python Utility classes for Earthcube

[Rendered Documentation with Code Documentation](https://earthcube.github.io/earthcube_utilities/)

## earthcube_utilities

[Utilites](./earthcube_utilities/) used in the [Earthcube Geocodes Infrastructure](https://earthcube.github.io/geocodes_documentation/developers/services-infrastructure/)
A set of modules to connect to the backend services, query the graph store, and to gather infomrmation about 
the Science on Schema JSONLD stored in the graph store.

* [GeoCODES](https://www.earthcube.org/geocodes) 
* [search](https://geocodes.earthcube.org/) 
* and [Notebooks]( https://github.com/earthcube/NotebookTemplates/tree/geocodes_template/GeoCODEStemplates)


##  Notebook Proxy
[mknb.py](./notebook_proxy/mknb.py) 
Creates parameterized NoteBook gists (from a [template](./notebook_proxy/templates)) for opening in binder or collab

**Please try the**  [search](https://geocodes.earthcube.org/) & click on its' feedback, incl for use-case that we can try to attain 

## Summarize
[Summarize](./summarize/) is  tool to materialize a set of triples that are used to improve search performance.

## Artifacts
### Notebook Proxy:
There is no pypi package, since this is code that runs in a docker container/local server

https://hub.docker.com/repository/docker/nsfearthcube/mknb

See [README.md](./notebook_proxy/) in src/notebook_proxy



### Earthcube Utilties:
https://pypi.org/project/earthcube-utilities/

python3 -m pip install earthcube-utilities

[Code Documentation](https://earthcube.github.io/earthcube_utilities/)

### Earthcube Utility Summarize:
https://test.pypi.org/project/earthcube-summarize/

python3 -m pip install --index-url https://test.pypi.org/simple/ earthcube_summarize

[Documentation](https://earthcube.github.io/earthcube_utilities/summarize/)


