"""qLever manager for ec.graph package — full implementation.

This implementation uses the project's MinioDatastore for S3 access (ec.datastore.s3.MinioDatastore).
"""
from __future__ import annotations
import os
import json
import logging
from typing import Dict, List, Optional, Tuple
import re

try:
    # prefer the project's MinioDatastore wrapper
    from ec.datastore.s3 import MinioDatastore
except Exception:  # pragma: no cover
    MinioDatastore = None

import requests
import yaml
from jinja2 import Template

logger = logging.getLogger(__name__)


def is_s3_path(path: str) -> bool:
    return path.startswith("s3://")


def slugify(name: str) -> str:
    """Normalize a community name into a slug: lowercase, replace non-alnum by '-', collapse dashes."""
    s = (name or "").lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-+", "-", s)
    s = s.strip("-")
    return s or name


def parse_s3_path(path: str) -> Tuple[str, str]:
    assert is_s3_path(path), f"Not an s3 path: {path}"
    no_prefix = path[len("s3://"):]
    parts = no_prefix.split("/", 1)
    bucket = parts[0]
    key = parts[1] if len(parts) > 1 else ""
    return bucket, key


def load_text_from_s3(s3_path: str) -> str:
    # Use MinioDatastore wrapper if available
    if MinioDatastore is None:
        raise RuntimeError("MinioDatastore is required for S3 access but is not available")
    bucket, key = parse_s3_path(s3_path)
    ds = _get_minio_datastore()
    data = ds.getFileFromStore({"bucket_name": bucket, "object_name": key})
    # MinioDatastore.getFileFromStore returns bytes (minio get_object().data)
    if isinstance(data, bytes):
        return data.decode("utf-8")
    return str(data)


def load_text_from_url(url: str) -> str:
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return r.text


def load_yaml(path_or_url: str) -> Dict:
    text = load_text_from_s3(path_or_url) if is_s3_path(path_or_url) else load_text_from_url(path_or_url)
    return yaml.safe_load(text)


def list_release_files_in_s3(prefix_or_bucket: str, maybe_prefix: Optional[str] = None) -> List[str]:
    if MinioDatastore is None:
        raise RuntimeError("MinioDatastore is required for S3 listing but is not available")
    if is_s3_path(prefix_or_bucket):
        bucket, prefix = parse_s3_path(prefix_or_bucket)
    else:
        bucket = prefix_or_bucket
        prefix = maybe_prefix or ""

    ds = _get_minio_datastore()
    objs = ds.listPath(bucket, prefix)
    results = []
    for o in objs:
        key = getattr(o, 'object_name', None) or getattr(o, 'object', None) or str(o)
        if key.endswith("_release.nq") or key.endswith("_release.nq.gz"):
            results.append(f"s3://{bucket}/{key}")
    return results


# Module-level cached datastore
_MINIO_DATASTORE: Optional[MinioDatastore] = None


def _get_minio_datastore() -> MinioDatastore:
    """Create or return a cached MinioDatastore instance.

    Reads environment variables:
      MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_SECURE
    Falls back to 'localhost:9000' if none provided.
    """
    global _MINIO_DATASTORE
    if _MINIO_DATASTORE is not None:
        return _MINIO_DATASTORE
    if MinioDatastore is None:
        raise RuntimeError("MinioDatastore wrapper not available")
    endpoint = os.environ.get('MINIO_ENDPOINT') or os.environ.get('S3_ENDPOINT') or 'localhost:9000'
    access = os.environ.get('MINIO_ACCESS_KEY')
    secret = os.environ.get('MINIO_SECRET_KEY')
    secure = os.environ.get('MINIO_SECURE')
    opts = {}
    if access and secret:
        opts['access_key'] = access
        opts['secret_key'] = secret
    if secure is not None:
        opts['secure'] = secure.lower() not in ('0', 'false', 'no')
    _MINIO_DATASTORE = MinioDatastore(endpoint, options=opts)
    return _MINIO_DATASTORE


def resolve_community_sources(tenant_yaml: Dict, gleaner_yaml: Dict) -> Dict[str, List[str]]:
    communities = {}
    gleaner_sources = [s for s in gleaner_yaml.get("sources", []) if s.get("active")]
    active_names = [s.get("name") for s in gleaner_sources if s.get("name")]

    for t in tenant_yaml.get("tenant", []):
        community = t.get("community")
        raw_sources = t.get("sources", []) or []
        # Accept scalar string or list
        if isinstance(raw_sources, str):
            sources_iter = [raw_sources]
        else:
            sources_iter = list(raw_sources)

        resolved = []
        for s in sources_iter:
            if s is None:
                continue
            norm = str(s).strip()
            norm = re.sub(r"^[-\s]+", "", norm)
            norm_low = norm.lower()
            if norm_low == "all":
                resolved.extend(active_names)
            else:
                resolved.append(norm)
        # deduplicate while keeping order
        seen = set()
        dedup = []
        for name in resolved:
            if name and name not in seen:
                dedup.append(name)
                seen.add(name)
        communities[community] = dedup
    return communities


def render_qleverfile_for_community(
    community: str,
    release_urls: List[str],
    template_facetsearch_path: str,
    template_ui_path: str,
    out_dir: str,
) -> Dict[str, str]:
    os.makedirs(out_dir, exist_ok=True)

    with open(template_facetsearch_path, "r", encoding="utf-8") as fh:
        facet_base = fh.read()
    with open(template_ui_path, "r", encoding="utf-8") as fh:
        ui_base = fh.read()

    # Create a normalized slug for the community to use in filenames and UI slugs
    slug = slugify(community)

    # Extract source names from release URLs
    # From URL like "https://example.com/path/bcodmo_release.nq" → extract "bcodmo"
    # From URL like "s3://bucket/path/hydroshare_release.nq.gz" → extract "hydroshare"
    source_names = []
    for url in release_urls:
        # Get the filename from the URL
        filename = url.split('/')[-1]
        # Remove _release.nq or _release.nq.gz suffix
        source_name = re.sub(r'_release\.nq(\.gz)?$', '', filename)
        if source_name:
            source_names.append(source_name)

    # Create space-separated string for SOURCES variable
    sources_str = ' '.join(source_names)

    # Prefer rendering templates with Jinja so templates can include placeholders
    ctx = {
        "community": community,
        "slug": slug,
        "release_urls": release_urls,
        "sources": sources_str  # space-separated string for SOURCES variable
    }
    try:
        facet_tpl = Template(facet_base)
        rendered_facet = facet_tpl.render(**ctx)
    except Exception:
        # Fallback: replace NAME line directly
        rendered_facet = re.sub(r"(?m)^\s*NAME\s*=.*$", f"NAME              = {slug}", facet_base)

    try:
        ui_tpl = Template(ui_base)
        rendered_ui = ui_tpl.render(**ctx)
    except Exception:
        # Fallback: replace the first occurrences of name/slug
        rendered_ui = ui_base.replace("name: example", f"name: {slug}", 1)
        rendered_ui = rendered_ui.replace("slug: example", f"slug: {slug}", 1)

    facet_out = os.path.join(out_dir, f"Qleverfile.{community}")
    ui_out = os.path.join(out_dir, f"Qleverfile-ui-{community}.yml")

    generated_block = "\n# --- GENERATED datasources ---\n"
    for u in release_urls:
        generated_block += f"# - {u}\n"

    with open(facet_out, "w", encoding="utf-8") as fh:
        fh.write(rendered_facet)
        fh.write(generated_block)

    with open(ui_out, "w", encoding="utf-8") as fh:
        fh.write(rendered_ui)
        fh.write(generated_block)

    return {"facet": facet_out, "ui": ui_out}


def load_env_vars(env_file_path: Optional[str] = None) -> List[Dict]:
    """Load environment variables from a .env file and return as list of dicts.

    Args:
        env_file_path: Optional path to .env file. If None, returns empty list.

    Returns:
        List of dicts in format [{"name": "KEY", "value": "VALUE"}, ...]
    """
    if not env_file_path:
        return []

    env_vars = []
    try:
        with open(env_file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                # Skip empty lines and comments
                if not line or line.startswith("#"):
                    continue
                # Parse KEY=VALUE format
                if "=" in line:
                    key, value = line.split("=", 1)
                    env_vars.append({"name": key.strip(), "value": value.strip()})
    except Exception as e:
        logger.warning(f"Failed to load env file {env_file_path}: {e}")

    return env_vars


class PortainerClient:
    def __init__(self, base_url: str, token: Optional[str] = None, verify_ssl: bool = True):
        """Initialize Portainer client.

        Args:
            base_url: Portainer API base URL
            token: Portainer API token. If None, reads from PORTAINER_TOKEN environment variable.
            verify_ssl: Whether to verify SSL certificates
        """
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()

        # Get token from parameter or environment variable
        api_token = token or os.environ.get("PORTAINER_TOKEN")
        if not api_token:
            raise ValueError("Portainer token required. Provide via token parameter or PORTAINER_TOKEN environment variable.")

        self.session.headers.update({"Authorization": f"Bearer {api_token}", "Accept": "application/json"})
        self.verify_ssl = verify_ssl

    def list_stacks(self) -> List[Dict]:
        url = f"{self.base_url}/api/stacks"
        r = self.session.get(url, verify=self.verify_ssl, timeout=30)
        r.raise_for_status()
        return r.json()

    def find_stack(self, name: str) -> Optional[Dict]:
        stacks = self.list_stacks()
        for s in stacks:
            if s.get("Name") == name or s.get("Name", "").endswith(f"_{name}"):
                return s
        return None

    def create_stack(self, name: str, stackfile_content: str, env: Optional[List[Dict]] = None, endpoint_id: int = 1) -> Dict:
        url = f"{self.base_url}/api/stacks?endpointId={endpoint_id}&method=string"
        form = {"Name": name, "StackFileContent": stackfile_content}
        if env:
            form["Env"] = json.dumps(env)
        r = self.session.post(url, data=form, verify=self.verify_ssl, timeout=60)
        r.raise_for_status()
        return r.json()

    def update_stack(self, stack_id: int, stackfile_content: str, env: Optional[List[Dict]] = None, endpoint_id: int = 1) -> Dict:
        url = f"{self.base_url}/api/stacks/{stack_id}?endpointId={endpoint_id}"
        payload = {"StackFileContent": stackfile_content}
        if env is not None:
            payload["Env"] = json.dumps(env) if not isinstance(env, str) else env
        r = self.session.put(url, json=payload, verify=self.verify_ssl, timeout=60)
        r.raise_for_status()
        return r.json()

    def create_or_update_stack(self, name: str, stackfile_content: str, env: Optional[List[Dict]] = None, endpoint_id: int = 1) -> Dict:
        existing = self.find_stack(name)
        if existing:
            stack_id = existing.get("Id")
            if stack_id is None:
                raise ValueError(f"Stack {name} found but has no ID")
            logger.info(f"Updating existing stack %s (id=%s)", name, stack_id)
            return self.update_stack(stack_id, stackfile_content, env=env, endpoint_id=endpoint_id)
        else:
            logger.info("Creating stack %s", name)
            return self.create_stack(name, stackfile_content, env=env, endpoint_id=endpoint_id)

    def restart_stack(self, stack_id: int, endpoint_id: int = 1) -> Dict:
        url = f"{self.base_url}/api/stacks/{stack_id}/deploy?endpointId={endpoint_id}"
        r = self.session.post(url, verify=self.verify_ssl, timeout=60)
        if r.status_code not in (200, 204):
            r.raise_for_status()
        try:
            return r.json()
        except Exception:
            return {"status": r.status_code}

    def list_configs(self) -> List[Dict]:
        """List all Docker configs in Portainer."""
        url = f"{self.base_url}/api/docker/configs"
        r = self.session.get(url, verify=self.verify_ssl, timeout=30)
        r.raise_for_status()
        return r.json()

    def find_config(self, name: str) -> Optional[Dict]:
        """Find a Docker config by name."""
        configs = self.list_configs()
        for c in configs:
            if c.get("Name") == name:
                return c
        return None

    def create_config(self, name: str, content: str, labels: Optional[Dict[str, str]] = None) -> Dict:
        """Create a new Docker config."""
        url = f"{self.base_url}/api/docker/configs/create"
        payload = {
            "Name": name,
            "Data": content,
        }
        if labels:
            payload["Labels"] = labels
        r = self.session.post(url, json=payload, verify=self.verify_ssl, timeout=60)
        r.raise_for_status()
        return r.json()

    def create_or_update_config(self, name: str, content: str) -> Dict:
        """Create or update a Docker config.

        Since Docker configs are immutable, updating creates a new version with incremented name.
        For example: qlever-config-test -> qlever-config-test-v2 -> qlever-config-test-v3

        Args:
            name: Config name (e.g., "qlever-config-test")
            content: Config content as string

        Returns:
            Dict with config information including the actual created name
        """
        existing = self.find_config(name)

        if existing:
            # Config exists, create new version
            # Extract version number if it exists
            version_match = re.search(r'-v(\d+)$', name)
            if version_match:
                version = int(version_match.group(1)) + 1
                base_name = re.sub(r'-v\d+$', '', name)
                new_name = f"{base_name}-v{version}"
            else:
                new_name = f"{name}-v2"

            logger.info(f"Config {name} exists, creating new version: {new_name}")
            result = self.create_config(new_name, content)
            result["_versioned_name"] = new_name
            return result
        else:
            # Create new config
            logger.info(f"Creating new config: {name}")
            result = self.create_config(name, content)
            result["_versioned_name"] = name
            return result


def generate_for_tenant(
    tenant_path: str,
    gleanerconfig_path: Optional[str],
    base_release_url: Optional[str],
    s3_release_prefix: Optional[str],
    templates: Dict[str, str],
    out_base: str = "build/qlever_generated",
) -> Dict[str, Dict[str, str]]:
    tenant_yaml = None
    if is_s3_path(tenant_path):
        tenant_yaml = yaml.safe_load(load_text_from_s3(tenant_path))
    elif tenant_path.startswith("http://") or tenant_path.startswith("https://"):
        tenant_yaml = yaml.safe_load(load_text_from_url(tenant_path))
    else:
        with open(tenant_path, "r", encoding="utf-8") as fh:
            tenant_yaml = yaml.safe_load(fh)

    gleaner_yaml = None
    if gleanerconfig_path:
        if is_s3_path(gleanerconfig_path):
            gleaner_yaml = yaml.safe_load(load_text_from_s3(gleanerconfig_path))
        elif gleanerconfig_path.startswith("http"):
            gleaner_yaml = yaml.safe_load(load_text_from_url(gleanerconfig_path))
        else:
            with open(gleanerconfig_path, "r", encoding="utf-8") as fh:
                gleaner_yaml = yaml.safe_load(fh)

    communities = resolve_community_sources(tenant_yaml or {}, gleaner_yaml or {})

    out = {}

    for community, sources in communities.items():
        release_urls = []
        for src in sources:
            if s3_release_prefix:
                all_releases = list_release_files_in_s3(s3_release_prefix)
                match = [r for r in all_releases if f"/{src}_release" in r or r.endswith(f"{src}_release.nq")]
                if match:
                    release_urls.extend(match)
                else:
                    logger.warning("No S3 release found for source %s under prefix %s", src, s3_release_prefix)
            elif base_release_url:
                fn = f"{src}_release.nq"
                url = base_release_url.rstrip("/") + "/" + fn
                release_urls.append(url)
            else:
                logger.warning("No release source provided for %s; skipping %s", community, src)

        out_dir = os.path.join(out_base, community)
        generated = render_qleverfile_for_community(
            community=community,
            release_urls=release_urls,
            template_facetsearch_path=templates["facet"],
            template_ui_path=templates["ui"],
            out_dir=out_dir,
        )
        # write a simple sources file for each community
        try:
            os.makedirs(out_dir, exist_ok=True)
            sources_file = os.path.join(out_dir, "sources.txt")
            with open(sources_file, "w", encoding="utf-8") as sf:
                for u in release_urls:
                    sf.write(u + "\n")
        except Exception:
            logger.exception("Failed to write sources file for %s", community)
        out[community] = generated
    return out


def generate_from_location(
    config_base: str,
    config_name: Optional[str],
    templates: Dict[str, str],
    out_base: str = "build/qlever_generated",
    base_release_url: Optional[str] = None,
    s3_release_prefix: Optional[str] = None,
) -> Dict[str, Dict[str, str]]:
    """Read tenant.yaml and gleanerconfig.yaml from a shared location and generate qlever files.

    config_base may be a local directory, a http(s) URL, or an s3:// path. If config_name is
    provided, the files are expected under {config_base}/{config_name}/tenant.yaml and gleanerconfig.yaml.
    If config_base already points to the directory containing tenant.yaml, pass config_name=None.
    """
    def _join(base, name):
        if base.endswith("/"):
            return base + name
        return base + "/" + name

    # build paths
    if config_name:
        tenant_path = _join(config_base.rstrip('/'), config_name + "/tenant.yaml")
        gleaner_path = _join(config_base.rstrip('/'), config_name + "/gleanerconfig.yaml")
    else:
        # assume config_base points to directory containing files
        tenant_path = _join(config_base.rstrip('/'), "tenant.yaml")
        gleaner_path = _join(config_base.rstrip('/'), "gleanerconfig.yaml")

    return generate_for_tenant(
        tenant_path=tenant_path,
        gleanerconfig_path=gleaner_path,
        base_release_url=base_release_url,
        s3_release_prefix=s3_release_prefix,
        templates=templates,
        out_base=out_base,
    )


__all__ = ["generate_for_tenant", "generate_from_location", "PortainerClient"]
