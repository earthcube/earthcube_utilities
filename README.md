# EarthCube Utilities

A comprehensive Python toolkit supporting NSF EarthCube GeoCODES Infrastructure, providing utilities for graph database management, SPARQL querying, and Science on Schema JSON-LD processing.

[![PyPI version](https://badge.fury.io/py/earthcube-utilities.svg)](https://badge.fury.io/py/earthcube-utilities)
[![Documentation Status](https://img.shields.io/badge/docs-latest-brightgreen.svg)](https://earthcube.github.io/earthcube_utilities/)

## Overview

EarthCube Utilities provides a set of modules to connect to backend services, query graph stores, and process Science on Schema JSON-LD data for the [EarthCube GeoCODES Infrastructure](https://earthcube.github.io/geocodes_documentation/developers/services-infrastructure/).

This toolkit powers:
- [GeoCODES Project](https://www.earthcube.org/geocodes)
- [GeoCODES Search Interface](https://geocodes.earthcube.org/)
- [Notebook Templates](https://github.com/earthcube/NotebookTemplates/tree/geocodes_template/GeoCODEStemplates)

## Key Components

### Core Functionality

- **Graph Management**: Abstract interfaces for BlazegraphDB and GraphDB databases
- **SPARQL Querying**: Template-based queries with easy-to-use wrappers
- **Data Stores**: S3-compatible storage management
- **Reporting**: Repository status and statistical analysis tools
- **Validation & Summarization**: JSON-LD processing and optimization
- **Collections**: RO-Crate archive management
- **Notebook Integration**: Jupyter notebook utilities

### Summarize

The summarize component materializes graph data into optimized formats for improved query performance. It creates a "materialized view" of repository JSON-LD as triples, which is critical for GeoCODES since Science on Schema implementations can vary widely, causing performance issues with direct querying.

### Notebook Proxy

[mknb.py](./notebook_proxy/mknb.py) creates parameterized Jupyter Notebook gists from templates for opening in Binder or Google Colab. It accepts parameters like URLs, URNs, and encoding formats to generate custom notebooks.

## Installation

### Regular Installation

```bash
pip install earthcube-utilities
```

### Local Development Mode

```bash
cd earthcube_utilities
pip install -e '.[dev]'
```

## Command-line Tools

The package provides several CLI tools:

```bash
# Generate graph statistics
generategraphstats [options]

# Check sitemap
check_sitemap [options]

# Query the graph 
query_graph [options]

# Generate missing reports
missing_report [options]

# Summarize identifier metadata
summarize_identifier_metadata [options]

# Generate EC reports
ec_reports [options]

# Bucket utilities
bucketutil [options]
```

## Artifacts

### Notebook Proxy

Docker image: [nsfearthcube/mknb](https://hub.docker.com/repository/docker/nsfearthcube/mknb)

See [notebook_proxy/README.md](./notebook_proxy/) for more details.

### EarthCube Utilities

- [Documentation](https://earthcube.github.io/earthcube_utilities/)
- [PyPI Package](https://pypi.org/project/earthcube-utilities/)

## Development

For contributing to the project, please follow the guidelines in [CLAUDE.md](./CLAUDE.md) and refer to the testing instructions in the documentation.

```bash
# Run all tests
python -m unittest discover -s earthcube_utilities/tests

# Run a specific test file
python -m unittest earthcube_utilities/tests/managegraph_test.py

# Run a specific test case
python -m unittest summarize_materializedview_test.SummarizeMaterializedViewTestCase.test_summaryDF2ttl
```

## Resources

- [Code Documentation](https://earthcube.github.io/earthcube_utilities/)
- [GeoCODES Documentation](https://earthcube.github.io/geocodes_documentation/)