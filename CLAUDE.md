# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Environment Setup

### Installation
```bash
# For regular installation
pip install earthcube-utilities

# For local development mode
cd earthcube_utilities
pip install -e '.[dev]'
```

### Environment Variables
Some tests and functionality require these environment variables:
- GRAPHUSER - Username for GraphDB
- GRAPHPASSWORD - Password for GraphDB

## Common Development Commands

### Testing
```bash
# Run all tests
python -m unittest discover -s earthcube_utilities/tests

# Run a specific test file
python -m unittest earthcube_utilities/tests/managegraph_test.py

# Run a specific test case
python -m unittest summarize_materializedview_test.SummarizeMaterializedViewTestCase.test_summaryDF2ttl
```

### CLI Commands
The package exposes several command-line tools:
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

## Architecture Overview

### Core Components

1. **Graph Management**
   - `ec.graph.manageGraph`: Creates, deletes namespaces and inserts data into graph databases
   - Supports BlazegraphDB and GraphDB with abstracted interface

2. **SPARQL Querying**
   - `ec.graph.sparql_query`: Wrapper around sparqldataframe with template-based SPARQL queries
   - `ec.graph.sparql_files`: Contains SPARQL query templates

3. **Data Stores**
   - `ec.datastore`: Handles S3 compatible storage
   - `ec.bucketutil`: Utilities for working with buckets

4. **Reporting**
   - `ec.reporting`: Generate reports on repository status
   - `ec.ec_reports`: Generate reports for EC

5. **Validation & Summarization**
   - `ec.summarize`: Summarize repository data
   - `ec.sos_json`: Utilities for Science on Schema JSON-LD

6. **Collections**
   - `ec.collection`: Handles RO-Crate archives and collections

7. **Notebook Integration**
   - `ec.notebook`: Utilities for Jupyter notebooks
   - Separate notebook proxy module for creating parameterized notebook gists

### Design Principles

- Abstract interfaces for graph databases (BlazegraphDB, GraphDB)
- Template-based SPARQL queries
- Unit tests with approval testing pattern
- Configuration via environment variables

## Development Guidelines

- Always run tests before submitting changes
- Tests use the `unittest` framework with approval testing via `approvaltests`
- Many tests require specific datasets and configured graph databases
- When adding functionality, follow the existing patterns for abstraction
- Create test data by following instructions in `docs/earthcube_utilities/setup_testing.md`