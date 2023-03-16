# Python Utility classes for Earthcube

## earthcube_utilities

 For manipulating (meta)data in NoteBook/s from [GeoCODES](https://www.earthcube.org/geocodes) [search](https://geocodes.earthcube.org/) Incl: the crawl & assert of data-repository metadata for search &for the NoteBooks:_

##  Notebook Proxy
[mknb.py](https://github.com/MBcode/ec/blob/master/NoteBook/mknb.py)  creates parameterized NoteBook gists (from a [template](https://github.com/MBcode/ec/blob/master/NoteBook/template.ipynb)) for opening in colab

**Please try the**  [search](https://geocodes.earthcube.org/) & click on it's feedback, incl for use-case that we can try to attain 

## Summarize
A tool to materialize a set of triples that are used to improve search performance.

## Artifacts
### Notebook Proxy:
https://hub.docker.com/repository/docker/nsfearthcube/mknb

See [README.md](./notebook_proxy/README.md) in src/notebook_proxy

There is no pypi package, since this is code that runs in a docker container/local server

### Earthcube Utilties:
https://test.pypi.org/project/earthcube-utilities/
(presently test.pypi)

python3 -m pip install --index-url https://test.pypi.org/simple/ earthcube-utilities

DOCUMENTATION IS NEEDED.

### Earthcube Utility Summarize:
https://test.pypi.org/project/earthcube-utility-summarize/

[documentation](./summarize/README.md)


## Notes:
[From](https://mbcode.github.io/ec/): https://github.com/MBcode/ec &/or [gitlab](https://gitlab.com/MBcode/ec); which includes versions of the server-side code


also an (upcoming) infrastructure enhancement [update](https://mbcode.github.io/ec/)