# Earthcube Utilities


## Users

### Earthcube Utilities:
https://pypi.org/project/earthcube-utilities/


### scripts
When installed via pip:

* [Reporting](https://earthcube.github.io/earthcube_utilities/earthcube_utilities/reporting/)
* [Summarize a namespace](https://earthcube.github.io/earthcube_utilities/earthcube_utilities/summarize/)


### Manual Install
`python3 -m pip install  earthcube-utilities`



## Developers

from [console scripts](https://setuptools.pypa.io/en/latest/userguide/entry_point.html#console-scripts)

### local development mode
```shell
cd earthcube_utiltiies
pip3 install -e .
```
## Developement

create a virutal env and activate

`source {envname}/bin/activate`


use editable install

```shell
cd earthcube_utiltiies
pip3 install -e .
```

If you edit the pyproject.toml and want to test an added script, 
```shell
cd summarize
pip3 uninstall -e earthcube_utiltiies
pip3 install -e .
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
