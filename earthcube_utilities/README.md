# Earthcube Utilities

A package of utilities for the NSF Earthcube Geocodes Project.

**Version:** 0.2.00
**Python:** >= 3.11
**PyPI:** https://pypi.org/project/earthcube-utilities/

## Features

- **Graph Management**: Create, delete, and manage graph database namespaces (BlazegraphDB, GraphDB)
- **SPARQL Querying**: Template-based SPARQL queries with sparqldataframe wrapper
- **qLever Manager**: Generate and deploy qLever configurations for EarthCube communities
- **Portainer Integration**: Deploy qLever instances to Portainer as Docker stacks
- **Data Stores**: S3-compatible storage utilities (MinIO)
- **Reporting**: Generate reports on repository status and metadata
- **Validation**: Science on Schema JSON-LD validation and summarization
- **Collections**: RO-Crate archive handling

## Installation

### Requirements
- Python 3.11 or higher

### Install from PyPI
```bash
pip install earthcube-utilities
```

### Development Install
```bash
cd earthcube_utilities
pip install -e '.[dev]'
```

## Command-Line Tools

The package provides several CLI tools:

### Graph and Reporting Tools
```bash
generategraphstats      # Generate graph statistics
check_sitemap           # Check sitemap validity
query_graph             # Query the graph database
missing_report          # Generate missing metadata reports
summarize_identifier_metadata  # Summarize identifier metadata
ec_reports              # Generate EC reports
bucketutil              # S3 bucket utilities
```

### qLever Manager (`qleverctl`)

Manage qLever instances for EarthCube communities.

#### Generate qLever Configurations

Generate Qleverfiles from tenant configuration:
```bash
qleverctl generate \
  --tenant path/to/tenant.yaml \
  --gleaner path/to/gleanerconfig.yaml \
  --base-release https://oss.geocodes-aws.earthcube.org/decoder/graphs/latest \
  --out build/qlever_generated
```

Generate from shared configuration location:
```bash
qleverctl generate-from-location \
  --config-base earthcube_utilities/resources/gleanerio \
  --base-release https://oss.geocodes-aws.earthcube.org/decoder/graphs/latest \
  --out build/qlever_generated
```

#### Portainer Integration

List all Portainer stacks:
```bash
export PORTAINER_TOKEN=ptr_xxx
qleverctl portainer-list --portainer-url http://localhost:9000
```

Restart a stack:
```bash
qleverctl portainer-restart \
  --portainer-url http://localhost:9000 \
  --stack-name my-stack
```

Deploy configurations to Portainer:
```bash
qleverctl portainer-deploy \
  --portainer-url http://localhost:9000 \
  --stack-name qlever-test \
  --config-dir build/qlever_generated/test \
  --community test \
  --compose-file earthcube_utilities/resources/qlever/deployment/qlever_namespace.yaml
```

Update existing stack:
```bash
qleverctl portainer-update \
  --portainer-url http://localhost:9000 \
  --stack-name qlever-test \
  --config-dir build/qlever_generated/test \
  --community test \
  --restart
```

#### End-to-End Deployment

Deploy from tenant configuration to Portainer in one command:
```bash
qleverctl deploy-from-tenant \
  --config-base earthcube_utilities/resources/gleanerio \
  --base-release https://oss.geocodes-aws.earthcube.org/decoder/graphs/latest \
  --portainer-url http://localhost:9000 \
  --stack-prefix qlever- \
  --dry-run
```

Remove `--dry-run` to actually deploy.

## Environment Variables

### Graph Database
- `GRAPHUSER` - Username for GraphDB
- `GRAPHPASSWORD` - Password for GraphDB

### MinIO/S3
- `MINIO_ENDPOINT` or `S3_ENDPOINT` - MinIO/S3 endpoint (default: localhost:9000)
- `MINIO_ACCESS_KEY` - MinIO access key
- `MINIO_SECRET_KEY` - MinIO secret key
- `MINIO_SECURE` - Use HTTPS (default: false)

### Portainer
- `PORTAINER_TOKEN` - Portainer API authentication token (required for all Portainer commands)

## Documentation

- [Reporting](https://earthcube.github.io/earthcube_utilities/earthcube_utilities/reporting/)
- [Summarize a namespace](https://earthcube.github.io/earthcube_utilities/earthcube_utilities/summarize/)
- [Project Homepage](https://www.earthcube.org/)
- [Geocodes Documentation](https://earthcube.github.io/geocodes_documentation/)

## Development

### Setup Development Environment

Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

Install in editable mode with dev dependencies:
```bash
cd earthcube_utilities
pip install -e '.[dev]'
```

### Running Tests

Run all tests:
```bash
python -m unittest discover -s earthcube_utilities/tests
```

Run specific test file:
```bash
python -m unittest earthcube_utilities/tests/managegraph_test.py
```

Run specific test case:
```bash
python -m unittest summarize_materializedview_test.SummarizeMaterializedViewTestCase.test_summaryDF2ttl
```

### Building Package

Install build tools:
```bash
python -m pip install build
```

Build wheel:
```bash
python -m build --wheel
```

The `dist/` directory will contain the package. You can unzip the wheel to inspect contents.

### After Editing pyproject.toml

If you edit `pyproject.toml` and want to test changes:
```bash
pip uninstall earthcube-utilities
pip install -e .
```

## Architecture

### Core Components

- **`ec.graph.manageGraph`** - Create, delete namespaces and insert data into graph databases
- **`ec.graph.qlever_manager`** - Generate and deploy qLever configurations
- **`ec.graph.sparql_query`** - Template-based SPARQL queries
- **`ec.datastore`** - S3-compatible storage handlers
- **`ec.reporting`** - Repository status reports
- **`ec.summarize`** - Repository data summarization
- **`ec.collection`** - RO-Crate archives and collections

### Design Principles

- Abstract interfaces for graph databases (BlazegraphDB, GraphDB)
- Template-based configuration generation (Jinja2)
- Unit tests with approval testing pattern
- Configuration via environment variables
- CLI-first design for automation

## Contributing

See [CLAUDE.md](./CLAUDE.md) for development guidelines and architecture notes.

## Links

- **Source**: https://github.com/earthcube/earthcube_utilities
- **Bug Tracker**: https://github.com/earthcube/earthcube_utilities/issues
- **Documentation**: https://earthcube.github.io/geocodes_documentation/
