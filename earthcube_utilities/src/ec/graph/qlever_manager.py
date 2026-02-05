"""qLever manager for ec.graph package — moved copy under earthcube_utilities/src.
This is a copy of src/ec/graph/qlever_manager.py to satisfy the requested package location.
"""
from __future__ import annotations
import os
import json
import logging
from typing import Dict, List, Optional, Tuple
import re

try:
    import boto3
except Exception:  # pragma: no cover
    boto3 = None

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
    if boto3 is None:
        raise RuntimeError("boto3 is required for S3 access but is not installed or available")
    bucket, key = parse_s3_path(s3_path)
    s3 = boto3.client("s3")
    obj = s3.get_object(Bucket=bucket, Key=key)
    return obj["Body"].read().decode("utf-8")


def load_text_from_url(url: str) -> str:
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    return r.text


def load_yaml(path_or_url: str) -> Dict:
    text = load_text_from_s3(path_or_url) if is_s3_path(path_or_url) else load_text_from_url(path_or_url)
    return yaml.safe_load(text)


def list_release_files_in_s3(prefix_or_bucket: str, maybe_prefix: Optional[str] = None) -> List[str]:
    if is_s3_path(prefix_or_bucket):
        bucket, prefix = parse_s3_path(prefix_or_bucket)
    else:
        bucket = prefix_or_bucket
        prefix = maybe_prefix or ""

    if boto3 is None:
        raise RuntimeError("boto3 is required for S3 listing but is not installed or available")
    s3 = boto3.client("s3")
    paginator = s3.get_paginator("list_objects_v2")
    results = []
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for obj in page.get("Contents", []):
            key = obj["Key"]
            if key.endswith("_release.nq") or key.endswith("_release.nq.gz"):
                results.append(f"s3://{bucket}/{key}")
    return results


def resolve_community_sources(tenant_yaml: Dict, gleaner_yaml: Dict) -> Dict[str, List[str]]:
    communities = {}
    gleaner_sources = [s for s in gleaner_yaml.get("sources", []) if s.get("active")]
    active_names = [s.get("name") for s in gleaner_sources if s.get("name")]

    for t in tenant_yaml.get("tenant", []):
        community = t.get("community")
        sources = t.get("sources", []) or []
        resolved = []
        for s in sources:
            if s == "all":
                resolved.extend(active_names)
            else:
                resolved.append(s)
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

    # Prefer rendering templates with Jinja so templates can include placeholders
    ctx = {"community": community, "slug": slug, "release_urls": release_urls}
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


class PortainerClient:
    def __init__(self, base_url: str, token: str, verify_ssl: bool = True):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {token}", "Accept": "application/json"})
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
            stack_id = existing.get("Id") or existing.get("Id")
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
        out[community] = generated
    return out


__all__ = ["generate_for_tenant", "PortainerClient"]
