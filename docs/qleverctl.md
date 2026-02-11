# qleverctl

CLI tool for managing qLever instances via Portainer. Reads tenant and gleaner configs (from local files, HTTP, or S3), generates per-community Qleverfiles, and manages Docker stacks through the Portainer API.

## Installation

```bash
pip install -e '.[dev]'
```

The `qleverctl` command is installed as a console script entry point.

## Configuration

### Environment variables

`qleverctl` loads a `.env` file from the current directory on startup (via `python-dotenv`). You can also export variables directly.

| Variable | Description |
|---|---|
| `PORTAINER_URL` | Portainer API base URL (used as default for `--portainer-url`) |
| `PORTAINER_TOKEN` | Portainer API key (exchanged for a JWT via `/api/auth` on each invocation) |
| `MINIO_ENDPOINT` | S3/MinIO endpoint (hostname:port, no path) |
| `MINIO_ACCESS_KEY` | S3/MinIO access key |
| `MINIO_SECRET_KEY` | S3/MinIO secret key |
| `MINIO_SECURE` | Use HTTPS for MinIO connections (`true`/`false`) |
| `HOST` | Hostname for qLever stacks (used in stack env vars) |
| `QLEVER_NET` | Docker network name for qLever stacks |

Example `.env` file:

```
PORTAINER_URL=https://portainer.example.com/api/endpoints/1/docker/
PORTAINER_TOKEN=ptr_abc123...
HOST=geocodes-aws-dev.earthcube.org
```

### Stack environment variable resolution

When deploying stacks (`create-stack`, `update-stack`, `deploy-from-tenant`), environment variables are resolved in this order (highest priority first):

1. CLI flags (`--host`, `--qlever-net`)
2. Values from `--env-file`
3. Values from `.env` (loaded into `os.environ` via dotenv)
4. Slug-derived defaults for `PROJECT`, `QLEVER_CONFIG`, `QLEVER_CONFIG_UI`, `QLEVER_VOL`

### Portainer URL format

The `--portainer-url` argument expects the Portainer API base URL including the environment endpoint:

```
https://<portainer-host>/api/endpoints/<ENVIRONMENT_ID>/docker/
```

You can find the environment ID in the Portainer UI under Environments.

## Commands

### generate

Generate Qleverfiles from explicit tenant/gleaner config paths.

```bash
qleverctl generate \
  --tenant path/to/tenant.yaml \
  --gleaner path/to/gleanerconfig.yaml \
  --base-release https://example.com/graphs/latest/ \
  --out build/qlever_generated
```

Config paths accept local files, `http(s)://` URLs, or `s3://` paths.

| Flag | Required | Description |
|---|---|---|
| `--tenant` | yes | Path to tenant.yaml |
| `--gleaner` | no | Path to gleanerconfig.yaml |
| `--base-release` | no | Base HTTP URL for release `.nq` files |
| `--base-url` | no | Base URL written into the Qleverfile `BASE_URL` (defaults to `--base-release`) |
| `--s3-release-prefix` | no | S3 path or HTTP URL to list release files (see [S3 release prefix](#s3-release-prefix)) |
| `--facet-template` | no | Path to Qleverfile facet search template |
| `--ui-template` | no | Path to Qleverfile UI template |
| `--out` | no | Output directory (default: `build/qlever_generated`) |

### generate-from-location

Generate Qleverfiles from a shared config location (directory, HTTP URL, or S3 path) that contains `tenant.yaml` and `gleanerconfig.yaml`.

```bash
qleverctl generate-from-location \
  --config-base https://oss.geocodes-aws.earthcube.org/decoder/scheduler/configs/production \
  --s3-release-prefix https://oss.geocodes-aws.earthcube.org/decoder/graphs/latest
```

With a subfolder:

```bash
qleverctl generate-from-location \
  --config-base s3://configs-bucket/scheduler/configs \
  --config-name production \
  --base-release https://example.com/graphs/latest/
```

When `--base-url` is not provided, it is derived automatically:
- Falls back to `--base-release` if provided
- Otherwise derived from `--config-base` by stripping the `/scheduler/...` path (e.g. `https://oss.geocodes-aws.earthcube.org/decoder/scheduler/configs/production` becomes `https://oss.geocodes-aws.earthcube.org/decoder`)

| Flag | Required | Description |
|---|---|---|
| `--config-base` | yes | Base location containing the config files |
| `--config-name` | no | Subfolder name under config-base |
| `--base-release` | no | Base HTTP URL for release files |
| `--base-url` | no | Base URL written into the Qleverfile `BASE_URL` (defaults to `--base-release`, then derived from `--config-base`) |
| `--s3-release-prefix` | no | S3 path or HTTP URL to list release files (see [S3 release prefix](#s3-release-prefix)) |
| `--out` | no | Output directory (default: `build/qlever_generated`) |

### list-stacks

List all stacks in Portainer.

```bash
qleverctl list-stacks --portainer-url https://portainer.example.com/api/endpoints/1/docker/
```

### list-configs

List all Docker configs in Portainer.

```bash
qleverctl list-configs --portainer-url https://portainer.example.com/api/endpoints/1/docker/
```

### push-configs

Upload Qleverfile and UI config to Portainer as Docker configs, without creating or modifying a stack. Useful for updating configs independently of stack deployment.

```bash
qleverctl push-configs \
  --portainer-url https://portainer.example.com/api/endpoints/1/docker/ \
  --config-dir build/qlever_generated/geocodesproduction \
  --community geocodesproduction
```

| Flag | Required | Description |
|---|---|---|
| `--portainer-url` | yes | Portainer API base URL |
| `--config-dir` | yes | Directory containing generated Qleverfiles |
| `--community` | yes | Community name |
| `--dry-run` | no | Show what would be uploaded without making API calls |

### create-stack

Create (or update) a Portainer stack for a community. Uploads configs, then creates the Docker stack from a compose template.

```bash
qleverctl create-stack \
  --portainer-url https://portainer.example.com/api/endpoints/1/docker/ \
  --config-dir build/qlever_generated/geocodesproduction \
  --community geocodesproduction \
  --host geocodes-aws.earthcube.org \
  --confirm
```

| Flag | Required | Description |
|---|---|---|
| `--portainer-url` | yes | Portainer API base URL |
| `--config-dir` | yes | Directory containing generated Qleverfiles |
| `--community` | yes | Community name |
| `--stack-name` | no | Stack name (defaults to `qlever-<community>`) |
| `--compose-file` | no | Docker compose template |
| `--env-file` | no | `.env` file with stack environment variables |
| `--host` | no | Hostname for the stack (overrides env-file and `.env`) |
| `--qlever-net` | no | Docker network name (overrides env-file and `.env`) |
| `--endpoint-id` | no | Portainer endpoint ID (default: 1) |
| `--dry-run` | no | Show what would be deployed without making API calls |
| `--confirm` | no | Skip interactive confirmation prompt |

### update-stack

Update an existing stack's configs and redeploy.

```bash
qleverctl update-stack \
  --portainer-url https://portainer.example.com/api/endpoints/1/docker/ \
  --stack-name qlever-geocodesproduction \
  --config-dir build/qlever_generated/geocodesproduction \
  --community geocodesproduction \
  --restart \
  --confirm
```

| Flag | Required | Description |
|---|---|---|
| `--portainer-url` | yes | Portainer API base URL |
| `--stack-name` | yes | Stack name to update |
| `--config-dir` | yes | Directory containing updated Qleverfiles |
| `--community` | yes | Community name |
| `--compose-file` | no | Docker compose template |
| `--env-file` | no | `.env` file with stack environment variables |
| `--host` | no | Hostname for the stack (overrides env-file and `.env`) |
| `--qlever-net` | no | Docker network name (overrides env-file and `.env`) |
| `--restart` | no | Restart the stack after update |
| `--endpoint-id` | no | Portainer endpoint ID (default: 1) |
| `--dry-run` | no | Show what would be updated without making API calls |
| `--confirm` | no | Skip interactive confirmation prompt |

### restart-stack

Restart an existing stack.

```bash
qleverctl restart-stack \
  --portainer-url https://portainer.example.com/api/endpoints/1/docker/ \
  --stack-name qlever-geocodesproduction \
  --confirm
```

| Flag | Required | Description |
|---|---|---|
| `--portainer-url` | yes | Portainer API base URL |
| `--stack-name` | yes | Stack name to restart |
| `--endpoint-id` | no | Portainer endpoint ID (default: 1) |
| `--confirm` | no | Skip interactive confirmation prompt |

### deploy-from-tenant

End-to-end workflow: reads tenant/gleaner configs from a shared location, generates Qleverfiles for all communities, and deploys each as a Portainer stack.

```bash
qleverctl deploy-from-tenant \
  --config-base https://oss.geocodes-aws.earthcube.org/decoder/scheduler/configs/production \
  --portainer-url https://portainer.example.com/api/endpoints/1/docker/ \
  --s3-release-prefix https://oss.geocodes-aws.earthcube.org/decoder/graphs/latest \
  --host geocodes-aws.earthcube.org \
  --confirm
```

| Flag | Required | Description |
|---|---|---|
| `--config-base` | yes | Base location for tenant.yaml and gleanerconfig.yaml |
| `--config-name` | no | Subfolder name under config-base |
| `--portainer-url` | yes | Portainer API base URL |
| `--base-release` | no | Base HTTP URL for release files |
| `--base-url` | no | Base URL written into the Qleverfile `BASE_URL` (defaults to `--base-release`, then derived from `--config-base`) |
| `--s3-release-prefix` | no | S3 path or HTTP URL to list release files (see [S3 release prefix](#s3-release-prefix)) |
| `--stack-prefix` | no | Prefix for generated stack names |
| `--env-file` | no | `.env` file with stack environment variables |
| `--host` | no | Hostname for the stacks (overrides env-file and `.env`) |
| `--qlever-net` | no | Docker network name (overrides env-file and `.env`) |
| `--dry-run` | no | Generate configs but don't deploy |
| `--confirm` | no | Skip interactive confirmation prompt |
| `--endpoint-id` | no | Portainer endpoint ID (default: 1) |
| `--out` | no | Output directory (default: `build/qlever_generated`) |

## S3 release prefix

The `--s3-release-prefix` flag tells `qleverctl` to list actual release files from an S3-compatible store, rather than constructing URLs from the source names in the tenant config.

It accepts three formats:

| Format | Example |
|---|---|
| HTTP(S) URL | `https://oss.geocodes-aws.earthcube.org/decoder/graphs/latest` |
| S3 URI | `s3://decoder/graphs/latest` |
| Bucket name | `decoder` (with `MINIO_ENDPOINT` configured) |

When an HTTP URL is provided, the endpoint, bucket, and prefix are parsed from the URL:
- `https://oss.geocodes-aws.earthcube.org/decoder/graphs/latest` -> endpoint `oss.geocodes-aws.earthcube.org`, bucket `decoder`, prefix `graphs/latest`

S3 credentials are read from `MINIO_ACCESS_KEY` and `MINIO_SECRET_KEY` environment variables.

### `-all` sources

When a community in `tenant.yaml` has its sources set to `-all`, the S3 listing becomes the source of truth:

- Only release files that actually exist in the S3 path are included
- Source names are derived from the filenames (e.g. `bcodmo_release.nq` -> `bcodmo`)
- Sources that don't have a release file in S3 are excluded

Communities with explicit source lists still use the tenant config as-is, regardless of `--s3-release-prefix`.

## Typical workflow

```bash
# 1. Generate Qleverfiles using S3 as the source of truth for release files
qleverctl generate-from-location \
  --config-base https://oss.geocodes-aws.earthcube.org/decoder/scheduler/configs/production \
  --s3-release-prefix https://oss.geocodes-aws.earthcube.org/decoder/graphs/latest

# 2. Review generated files
ls build/qlever_generated/

# 3. Push configs only (no stack changes)
qleverctl push-configs \
  --config-dir build/qlever_generated/geocodesproduction \
  --community geocodesproduction

# 4. Create the stack
qleverctl create-stack \
  --config-dir build/qlever_generated/geocodesproduction \
  --community geocodesproduction \
  --host geocodes-aws.earthcube.org \
  --confirm

# 5. Later, update and restart
qleverctl update-stack \
  --stack-name qlever-geocodesproduction \
  --config-dir build/qlever_generated/geocodesproduction \
  --community geocodesproduction \
  --restart --confirm
```

Or use `deploy-from-tenant` for the full pipeline in one command:

```bash
qleverctl deploy-from-tenant \
  --config-base https://oss.geocodes-aws.earthcube.org/decoder/scheduler/configs/production \
  --s3-release-prefix https://oss.geocodes-aws.earthcube.org/decoder/graphs/latest \
  --host geocodes-aws.earthcube.org \
  --dry-run
```

## Safety

- Destructive operations (`create-stack`, `update-stack`, `restart-stack`, `deploy-from-tenant`) prompt for interactive confirmation by default. Pass `--confirm` to skip the prompt (e.g. in CI/CD).
- Use `--dry-run` to preview what would happen without making any API calls.
- `PORTAINER_TOKEN` is never logged; token values are sanitized in error messages.
- S3 credentials (`access_key`, `secret_key`) are redacted in log output.

## File structure

```
earthcube_utilities/
  src/ec/graph/
    cli.py                  # CLI entry point (qleverctl)
    qlever_manager.py       # Core library: config parsing, template rendering, Portainer API client
  resources/qlever/
    catalogues/data-example/
      Qleverfile.facetsearch    # Jinja2 template for facet search Qleverfile
      Qleverfile-ui.yml         # Jinja2 template for UI config
    deployment/
      qlever_namespace.yaml     # Docker compose template for stack deployment
  env.example                   # Example environment variables
```