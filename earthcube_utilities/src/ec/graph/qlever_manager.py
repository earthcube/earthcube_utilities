"""qLever manager for ec.graph package — moved copy under earthcube_utilities/src.
This is a copy of src/ec/graph/qlever_manager.py to satisfy the requested package location.
"""
from __future__ import annotations
import os
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
        return _sanitize_yaml_text(data.decode("utf-8"))
    return _sanitize_yaml_text(str(data))


def _sanitize_yaml_text(text: str) -> str:
    """Strip C1 control characters (U+0080-U+009F) that are invalid in YAML."""
    cleaned = re.sub(r"[\x80-\x9f]", "", text)
    if cleaned != text:
        logger.warning("Stripped invalid C1 control characters from YAML input")
    return cleaned


def load_text_from_url(url: str) -> str:
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return _sanitize_yaml_text(r.text)


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
    import os
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
            # normalize: remove leading dashes/spaces and lower
            norm = str(s).strip()
            # remove leading hyphens that might be embedded in strings like "-all"
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
    source_names: Optional[List[str]] = None,
) -> Dict[str, str]:
    os.makedirs(out_dir, exist_ok=True)

    with open(template_facetsearch_path, "r", encoding="utf-8") as fh:
        facet_base = fh.read()
    with open(template_ui_path, "r", encoding="utf-8") as fh:
        ui_base = fh.read()

    # Create a normalized slug for the community to use in filenames and UI slugs
    slug = slugify(community)

    # Use explicitly provided source names, or extract from release URLs as fallback
    if not source_names:
        source_names = []
        for url in release_urls:
            filename = url.split('/')[-1]
            name = re.sub(r'_release\.nq(\.gz)?$', '', filename)
            if name:
                source_names.append(name)

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

        Authenticates to the Portainer API by exchanging an API key for a JWT
        via POST /api/auth. The API key is read from the ``token`` parameter
        or the ``PORTAINER_TOKEN`` environment variable.

        The ``base_url`` can be either the Portainer root
        (e.g. ``https://portainer.example.com``) or a full Docker endpoint URL
        (e.g. ``https://portainer.example.com/api/endpoints/2/docker``).
        If the URL contains ``/api/endpoints/<id>/docker``, the endpoint ID is
        extracted automatically.

        Args:
            base_url: Portainer URL (root or endpoint-specific)
            token: Portainer API key. If None, reads from PORTAINER_TOKEN environment variable.
            verify_ssl: Whether to verify SSL certificates
        """
        self.session = requests.Session()
        self.verify_ssl = verify_ssl

        # Parse the URL: extract root and optional endpoint ID
        url = base_url.rstrip("/")
        ep_match = re.search(r'(/api/endpoints/(\d+)(/docker)?)', url)
        if ep_match:
            self._root = url[:ep_match.start()]
            self._default_endpoint_id = int(ep_match.group(2))
        else:
            self._root = url
            self._default_endpoint_id = 2

        api_key = token or os.environ.get("PORTAINER_TOKEN")
        if not api_key:
            raise ValueError("Portainer API key required. Provide via token parameter or PORTAINER_TOKEN environment variable.")

        self.session.headers.update({"X-API-Key": api_key, "Accept": "application/json"})

    def _authenticate(self, api_key: str) -> str:
        """Exchange an API key for a JWT via Portainer's /api/auth endpoint."""
        url = f"{self._root}/api/auth"
        payload = {"apiKey": api_key}
        r = self.session.post(url, json=payload, verify=self.verify_ssl, timeout=30)
        r.raise_for_status()
        jwt = r.json().get("jwt")
        if not jwt:
            raise ValueError("Portainer /api/auth response did not contain a jwt")
        logger.debug("Authenticated to Portainer successfully")
        return jwt

    def _docker_url(self, path: str, endpoint_id: Optional[int] = None) -> str:
        """Build a Docker proxy URL: /api/endpoints/{id}/docker/{path}."""
        eid = endpoint_id or self._default_endpoint_id
        return f"{self._root}/api/endpoints/{eid}/docker/{path.lstrip('/')}"

    def list_stacks(self) -> List[Dict]:
        url = f"{self._root}/api/stacks"
        r = self.session.get(url, verify=self.verify_ssl, timeout=30)
        r.raise_for_status()
        return r.json()

    def find_stack(self, name: str) -> Optional[Dict]:
        stacks = self.list_stacks()
        for s in stacks:
            if s.get("Name") == name or s.get("Name", "").endswith(f"_{name}"):
                return s
        return None

    def get_swarm_id(self, endpoint_id: Optional[int] = None) -> Optional[str]:
        """Get the Docker Swarm ID via GET /swarm. Returns None if not in swarm mode."""
        url = self._docker_url("swarm", endpoint_id)
        try:
            r = self.session.get(url, verify=self.verify_ssl, timeout=30)
            r.raise_for_status()
            return r.json().get("ID")
        except Exception:
            logger.debug("Swarm not available on this endpoint")
            return None

    def create_stack(self, name: str, stackfile_content: str, env: Optional[List[Dict]] = None,
                     endpoint_id: Optional[int] = None) -> Dict:
        """Create a stack via Portainer.

        Auto-detects whether the endpoint runs Docker Swarm. If so, uses the
        swarm stack endpoint; otherwise uses standalone/compose.
        """
        eid = endpoint_id or self._default_endpoint_id
        payload: Dict = {"name": name, "stackFileContent": stackfile_content}
        if env:
            payload["env"] = env

        swarm_id = self.get_swarm_id(endpoint_id=eid)
        if swarm_id:
            payload["swarmID"] = swarm_id
            url = f"{self._root}/api/stacks/create/swarm/string?endpointId={eid}"
            logger.info("Creating swarm stack %s (swarm %s)", name, swarm_id)
        else:
            url = f"{self._root}/api/stacks/create/standalone/string?endpointId={eid}"
            logger.info("Creating standalone stack %s", name)

        r = self.session.post(url, json=payload, verify=self.verify_ssl, timeout=60)
        r.raise_for_status()
        return r.json()

    def update_stack(self, stack_id: int, stackfile_content: str, env: Optional[List[Dict]] = None,
                     endpoint_id: Optional[int] = None) -> Dict:
        """Update a stack via PUT /api/stacks/{id}?endpointId=N."""
        eid = endpoint_id or self._default_endpoint_id
        url = f"{self._root}/api/stacks/{stack_id}?endpointId={eid}"
        payload: Dict = {"stackFileContent": stackfile_content}
        if env is not None:
            payload["env"] = env
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

    def stop_stack(self, stack_id: int, endpoint_id: Optional[int] = None) -> Dict:
        """Stop a stack via POST /api/stacks/{id}/stop?endpointId=N."""
        eid = endpoint_id or self._default_endpoint_id
        url = f"{self._root}/api/stacks/{stack_id}/stop?endpointId={eid}"
        r = self.session.post(url, verify=self.verify_ssl, timeout=60)
        r.raise_for_status()
        try:
            return r.json()
        except Exception:
            return {"status": r.status_code}

    def start_stack(self, stack_id: int, endpoint_id: Optional[int] = None) -> Dict:
        """Start a stack via POST /api/stacks/{id}/start?endpointId=N."""
        eid = endpoint_id or self._default_endpoint_id
        url = f"{self._root}/api/stacks/{stack_id}/start?endpointId={eid}"
        r = self.session.post(url, verify=self.verify_ssl, timeout=60)
        r.raise_for_status()
        try:
            return r.json()
        except Exception:
            return {"status": r.status_code}

    def restart_stack(self, stack_id: int, endpoint_id: Optional[int] = None) -> Dict:
        """Restart a stack by stopping then starting it."""
        eid = endpoint_id or self._default_endpoint_id
        try:
            self.stop_stack(stack_id, endpoint_id=eid)
        except Exception:
            logger.debug("Stop failed (stack may already be stopped), proceeding with start")
        return self.start_stack(stack_id, endpoint_id=eid)

    def _set_resource_admin_ownership(self, rc_id: int) -> None:
        """Update a Portainer resource control to Administrators ownership."""
        url = f"{self._root}/api/resource_controls/{rc_id}"
        payload = {
            "administratorsOnly": False,
            "public": True,
            "users": [],
            "teams": [],
        }
        r = self.session.put(url, json=payload, verify=self.verify_ssl, timeout=30)
        r.raise_for_status()
        logger.info("Set resource control %d ownership to Administrators", rc_id)

    def list_configs(self, endpoint_id: Optional[int] = None) -> List[Dict]:
        """List all Docker configs via the Portainer Docker proxy."""
        url = self._docker_url("configs", endpoint_id)
        r = self.session.get(url, verify=self.verify_ssl, timeout=30)
        r.raise_for_status()
        return r.json()

    def find_config(self, name: str) -> Optional[Dict]:
        """Find a Docker config by name."""
        configs = self.list_configs()
        for c in configs:
            spec = c.get("Spec", {})
            if spec.get("Name") == name or c.get("Name") == name:
                return c
        return None

    def create_config(self, name: str, content: str, labels: Optional[Dict[str, str]] = None, endpoint_id: Optional[int] = None) -> Dict:
        """Create a new Docker config and set ownership to Administrators."""
        import base64
        url = self._docker_url("configs/create", endpoint_id)
        payload: Dict = {
            "Name": name,
            "Data": base64.b64encode(content.encode("utf-8")).decode("ascii"),
        }
        if labels:
            payload["Labels"] = labels
        r = self.session.post(url, json=payload, verify=self.verify_ssl, timeout=60)
        r.raise_for_status()
        result = r.json()

        # Portainer wraps the Docker response and includes a ResourceControl
        rc_id = (result.get("Portainer", {}).get("ResourceControl", {}).get("Id"))
        if rc_id:
            try:
                self._set_resource_admin_ownership(rc_id)
            except Exception as e:
                logger.warning("Failed to set config %s ownership to Administrators: %s", name, e)

        return result

    def create_or_update_config(self, name: str, content: str) -> Dict:
        """Create or update a Docker config.

        Since Docker configs are immutable, updating creates a new version with incremented name.
        For example: qlever-config-test -> qlever-config-test-v2 -> qlever-config-test-v3

        Args:
            name: Config name (e.g., "qlever-config-test")
            content: Config content as string

        Returns:
            Dict with config information including the actual created name

        Raises:
            ValueError: If config name would exceed Docker's 64-character limit
        """
        # Check name length (leave buffer for version suffix)
        if len(name) > 60:
            raise ValueError(f"Config name too long (>60 chars, exceeds Docker limit): {name}")

        existing = self.find_config(name)

        if existing:
            # Config exists, create new version
            # Extract version number if it exists (match the LAST -vN pattern)
            version_match = re.search(r'-v(\d+)(?!.*-v\d)', name)
            if version_match:
                current_version = int(version_match.group(1))
                new_version = current_version + 1
                # Replace the version number in the name
                new_name = re.sub(r'-v\d+(?!.*-v\d)', f'-v{new_version}', name)
            else:
                # No version yet, add -v2
                new_name = f"{name}-v2"

            # Recursively check if new version already exists (shouldn't happen in practice)
            if self.find_config(new_name):
                logger.info(f"Version {new_name} already exists, trying next version")
                # Try to find the highest existing version
                configs = self.list_configs()
                versions = []
                for c in configs:
                    match = re.search(rf'^{re.escape(name)}-v(\d+)$', c.get('Name', ''))
                    if match:
                        versions.append(int(match.group(1)))
                if versions:
                    highest = max(versions)
                    new_name = f"{name}-v{highest + 1}"
                else:
                    new_name = f"{name}-v2"

            logger.info(f"Creating new config version: {new_name}")
            return self.create_config(new_name, content, labels={"version": "new"})
        else:
            # Config doesn't exist, create initial version
            logger.info(f"Creating new config: {name}")
            return self.create_config(name, content)


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
            source_names=sources,
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
