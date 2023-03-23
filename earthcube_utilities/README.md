# Earthcube Utilities



## Proposed use
### Earthcube Utilities:
https://pypi.org/project/earthcube-utilities/


### Manual Install
`python3 -m pip install  earthcube-utilities`



## Developers

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
Locally,  see if a package builds
`python3 -m pip install build`

in _build/lib_ you can see what files are included in package

### build a wheel
to see what is added to a package, 

`python -m build --wheel`

_dist_ directory will contain the package. This is actually a zip file so unzip to see 
what got included

## Planning:
The planned functionality will be found in the docs folder,
[Earthcube Utilities Functionality](./docs/earthcube_utilties_functionality.md)
