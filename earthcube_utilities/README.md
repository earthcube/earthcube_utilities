# earthcube_utliites

The planned functionality will be found in the docs folder,
[Earthcube Utilities Functionality](./docs/earthcube_utilties_functionality.md)


## Proposed use
### Earthcube Utilties:
https://test.pypi.org/project/earthcube-utilities/
(presently test.pypi)

python3 -m pip install --index-url https://test.pypi.org/simple/ earthcube-utilities

## developers

### scripts
from [console scripts](https://setuptools.pypa.io/en/latest/userguide/entry_point.html#console-scripts)

when installed as a package, this should become a command

` generate_repo_stats`

### local development mode
python -m pip install -e .

## building a test package
### test packaging
`python3 -m pip install build`
### build a wheel
`python -m build --wheel`
