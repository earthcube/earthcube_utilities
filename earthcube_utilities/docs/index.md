# Documentation for Earthcube Utilities

## Overview
Earthcube utilities. Code to retrieve information from Geocodes Data and Graph stores, and to support 
the infrastructure in a python codebase.

### Earthcube Utilities:
https://test.pypi.org/project/earthcube-utilities/
(presently test.pypi)

### manual install
`python3 -m pip install --index-url https://test.pypi.org/simple/ earthcube-utilities`

### requirements.txt
add to your requirements.txt
```python
--extra-index-url https://test.pypi.org/simple/
earthcube-utilities
```

## developers

### scripts
In theory, if pip installed, theree is one script at present,
`generate_repo_stats --graphendpoint https://graph.geocodes-dev.earthcube.org/blazegraph/namespace/earthcube/ -s3 localhost:9000 --s3bucket gleaner`

from [console scripts](https://setuptools.pypa.io/en/latest/userguide/entry_point.html#console-scripts)

### local development mode
```shell
cd earthcube_utiltiies
python -m pip install -e .
```

## building a test package

### test packaging
to see if a package builds
`python3 -m pip install build`

in _build/lib_ you can see what files are included in package

### build a wheel
to see what is added to a package, 

`python -m build --wheel`

_dist_ directory will contain the package. this is actually a zip file so unzip to see 
what got included

## Planning document
* [functionality](./earthcube_utilties_functionality.md)
