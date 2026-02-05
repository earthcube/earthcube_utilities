Plan: qLever instance manager

TL;DR — Build a small Python library + CLI that reads tenant and gleaner configs (from S3 or HTTP), 
resolves per-community release files (pattern *_release.nq or S3 listing), 
renders per-community `Qleverfile.{community}` and `Qleverfile-ui-{community}.yml` from templates, 
and manages stacks via the Portainer API (create, update, restart) using `qlever_namespace.yaml` and `env.example` 
for env variables.

Steps
1. Parse configs: read `resources/gleanerio/tenant.yaml` and `resources/gleanerio/gleanerconfig.yaml` 
  (or S3 `{bucket}/scheduler/configs/{config_name}`) and produce community -> source lists.
2. Resolve releases: fetch release URLs from base URL `{bucket}/graphs/latest/` or list S3 prefix to gather `*_release.nq` files for each source.
3. Render templates: generate `resources/qlever/catalogues/data-example/Qleverfile.facetsearch`-based `Qleverfile.{community}` and `Qleverfile-ui-example.yml`-based `Qleverfile-ui-{community}.yml` using discovered release URLs.
4. Portainer control: implement API calls to create/update/restart stacks using `resources/qlever/deployment/qlever_namespace.yaml` and env vars from `resources/qlever/deployment/env.example`. Include stop-upload-start sequence for updates.
5. CLI design: provide commands `generate`, `push-configs`, `create-stack`, `update-stack`, `restart-stack` with flags: `--tenant PATH|S3`, `--config-bucket`, `--s3-prefix`, `--portainer-url`, `--portainer-token`, `--dry-run`, `--confirm`.

Further Considerations
1. Auth & API: Do you want Portainer auth via bearer token (recommended) or basic auth? (Option A: token / Option B: basic)
2. S3 access: prefer Python `boto3` (aws creds env-aware) or provide pluggable HTTP listing for public buckets? (Option A: boto3 / Option B: http-only)
3. Defaults & safety: enable `--dry-run` and `--confirm` for destructive operations; allow `--only-generate` to skip Portainer actions.

This is a draft — please confirm Portainer auth method, S3 access preference, and whether to include automatic upload of configs to the Docker swarm (via Portainer) or leave upload as a manual step.
