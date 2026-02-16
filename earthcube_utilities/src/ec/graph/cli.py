#!/usr/bin/env python3
from __future__ import annotations
import argparse
import logging
import logging.handlers
import os
import re
import sys
from typing import List, Optional
from ec.graph.qlever_manager import (
    generate_for_tenant,
    generate_from_location,
    PortainerClient,
    load_env_vars,
    slugify,
)


def _setup_logging(log_file: str = "qleverctl.log") -> None:
    """Setup logging to both file and console."""
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)


def _sanitize_token(text: str, token_pattern: str = r'ptr_[a-zA-Z0-9]+') -> str:
    """Sanitize sensitive tokens from text for safe logging."""
    return re.sub(token_pattern, 'ptr_***', text)


def _validate_template_files(facet_path: str, ui_path: str) -> None:
    """Validate that template files exist.

    Args:
        facet_path: Path to facet template
        ui_path: Path to UI template

    Raises:
        FileNotFoundError: If any template file doesn't exist
    """
    for name, path in [("facet", facet_path), ("ui", ui_path)]:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Template file not found ({name}): {path}")


def _confirm_action(action_description: str, confirm_flag: bool) -> bool:
    """Check --confirm flag or prompt interactively before a destructive action."""
    if confirm_flag:
        return True
    try:
        answer = input(f"{action_description}\nProceed? [y/N] ").strip().lower()
        return answer in ("y", "yes")
    except (EOFError, KeyboardInterrupt):
        print()
        return False


def _handle_push_configs(args) -> int:
    """Upload Qleverfile and UI config to Portainer/Docker configs without deploying a stack.

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code (0 for success, 1 for error)
    """
    try:
        slug = slugify(args.community)
        qleverfile_path = os.path.join(args.config_dir, f"Qleverfile.{args.community}")
        ui_config_path = os.path.join(args.config_dir, f"Qleverfile-ui-{args.community}.yml")

        if not os.path.exists(qleverfile_path):
            logging.error(f"Qleverfile not found: {qleverfile_path}")
            return 1

        with open(qleverfile_path, "r", encoding="utf-8") as f:
            qleverfile_content = f.read()

        ui_content = ""
        if os.path.exists(ui_config_path):
            with open(ui_config_path, "r", encoding="utf-8") as f:
                ui_content = f.read()

        config_name = f"qlever-config-{slug}"
        ui_config_name = f"qlever-ui-{slug}"

        if getattr(args, "dry_run", False):
            print(f"[dry-run] Would upload config: {config_name} from {qleverfile_path}")
            if ui_content:
                print(f"[dry-run] Would upload UI config: {ui_config_name} from {ui_config_path}")
            return 0

        client = PortainerClient(args.portainer_url)

        print(f"Uploading Qleverfile as config: {config_name}")
        config_result = client.create_or_update_config(config_name, qleverfile_content)
        print(f"  Config created: {config_result.get('_versioned_name', config_name)}")

        if ui_content:
            print(f"Uploading UI config: {ui_config_name}")
            ui_result = client.create_or_update_config(ui_config_name, ui_content)
            print(f"  UI config created: {ui_result.get('_versioned_name', ui_config_name)}")

        return 0
    except Exception as e:
        logging.error(f"Failed to push configs: {_sanitize_token(str(e))}")
        return 1


def _handle_generate(args) -> int:
    """Generate Qleverfiles from explicit tenant/gleaner paths.

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code (0 for success, 1 for error)
    """
    try:
        _validate_template_files(args.facet_template, args.ui_template)

        templates = {"facet": args.facet_template, "ui": args.ui_template}
        out = generate_for_tenant(
            tenant_path=args.tenant,
            gleanerconfig_path=args.gleaner,
            base_release_url=args.base_release,
            s3_release_prefix=args.s3_release_prefix,
            templates=templates,
            out_base=args.out,
            base_url=getattr(args, "base_url", None) or args.base_release,
        )
        print("Generated files:")
        for c, paths in out.items():
            print(c)
            for k, v in paths.items():
                print(f"  {k}: {v}")
        return 0
    except Exception as e:
        logging.error(f"Failed to generate: {e}")
        return 1


def _derive_base_url(config_base: str) -> str:
    """Derive base_url from config_base by stripping the scheduler path.

    E.g. https://oss.geocodes-aws.earthcube.org/decoder/scheduler/configs/production
      -> https://oss.geocodes-aws.earthcube.org/decoder
    """
    idx = config_base.find("/scheduler/")
    if idx != -1:
        return config_base[:idx].rstrip("/")
    return config_base.rstrip("/")


def _handle_generate_from_location(args) -> int:
    """Generate Qleverfiles from a shared config location.

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code (0 for success, 1 for error)
    """
    try:
        _validate_template_files(args.facet_template, args.ui_template)

        base_url = getattr(args, "base_url", None) or args.base_release
        if not base_url and args.config_base:
            base_url = _derive_base_url(args.config_base)

        templates = {"facet": args.facet_template, "ui": args.ui_template}
        out = generate_from_location(
            config_base=args.config_base,
            config_name=args.config_name,
            templates=templates,
            out_base=args.out,
            base_release_url=args.base_release,
            s3_release_prefix=args.s3_release_prefix,
            base_url=base_url,
        )
        print("Generated files:")
        for c, paths in out.items():
            print(c)
            for k, v in paths.items():
                print(f"  {k}: {v}")
        return 0
    except Exception as e:
        logging.error(f"Failed to generate from location: {e}")
        return 1


def _handle_portainer_list(args) -> int:
    """List all Portainer stacks.

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code (0 for success, 1 for error)
    """
    try:
        client = PortainerClient(args.portainer_url)
        stacks = client.list_stacks()
        print(f"Found {len(stacks)} stacks:")
        for s in stacks:
            print(f"  {s.get('Name')} (ID: {s.get('Id')})")
        return 0
    except Exception as e:
        logging.error(f"Failed to list stacks: {_sanitize_token(str(e))}")
        return 1


def _handle_list_configs(args) -> int:
    """List all Docker configs in Portainer.

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code (0 for success, 1 for error)
    """
    try:
        client = PortainerClient(args.portainer_url)
        configs = client.list_configs()
        print(f"Found {len(configs)} configs:")
        for c in configs:
            spec = c.get("Spec", {})
            name = spec.get("Name") or c.get("Name", "<unknown>")
            created = c.get("CreatedAt", "")
            updated = c.get("UpdatedAt", "")
            config_id = c.get("ID", "")
            parts = [f"  {name}"]
            if config_id:
                parts.append(f"(ID: {config_id[:12]})")
            if created:
                parts.append(f"created={created[:19]}")
            if updated and updated != created:
                parts.append(f"updated={updated[:19]}")
            print(" ".join(parts))
        return 0
    except Exception as e:
        logging.error(f"Failed to list configs: {_sanitize_token(str(e))}")
        return 1


def _handle_portainer_restart(args) -> int:
    """Restart a Portainer stack.

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code (0 for success, 1 for error)
    """
    try:
        client = PortainerClient(args.portainer_url)
        stack = client.find_stack(args.stack_name)

        if not stack:
            logging.error(f"Stack not found: {args.stack_name}")
            return 1

        stack_id = stack.get("Id")
        if not stack_id:
            logging.error(f"Stack found but has no ID: {args.stack_name}")
            return 1

        if not _confirm_action(
            f"Restart stack '{args.stack_name}' on {args.portainer_url}",
            getattr(args, "confirm", False),
        ):
            print("Aborted.")
            return 0

        print(f"Restarting stack: {args.stack_name}")
        client.restart_stack(stack_id, endpoint_id=args.endpoint_id)
        print("Stack restarted successfully")
        return 0
    except Exception as e:
        logging.error(f"Failed to restart stack: {_sanitize_token(str(e))}")
        return 1


def _build_stack_env(slug: str, env_file: Optional[str], qlever_net: Optional[str] = None, host: Optional[str] = None) -> List[dict]:
    """Build the environment variable list for a stack deployment.

    Resolution order (highest priority first):
      1. CLI flags (--host, --qlever-net)
      2. Values from --env-file
      3. Values from .env (loaded into os.environ via dotenv)
    """
    # Start with relevant vars from .env / os.environ as the base layer
    _dotenv_keys = ("HOST", "QLEVER_NET", "PROJECT", "QLEVER_CONFIG", "QLEVER_CONFIG_UI", "QLEVER_VOL")
    env_dict: dict[str, str] = {}
    for key in _dotenv_keys:
        val = os.environ.get(key)
        if val:
            env_dict[key] = val

    # Override with --env-file values (middle priority)
    env_vars = load_env_vars(env_file)
    for e in env_vars:
        env_dict[e["name"]] = e["value"]

    # Defaults derived from community slug (only if not set by either layer)
    for key in ("PROJECT", "QLEVER_CONFIG", "QLEVER_CONFIG_UI", "QLEVER_VOL"):
        env_dict.setdefault(key, slug)

    # CLI flags override everything
    if qlever_net:
        env_dict["QLEVER_NET"] = qlever_net
    if host:
        env_dict["HOST"] = host

    return [{"name": k, "value": v} for k, v in env_dict.items()]


def _handle_portainer_deploy(args) -> int:
    """Deploy Qleverfiles to Portainer.

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code (0 for success, 1 for error)
    """
    try:
        _validate_template_files(args.compose_file, args.compose_file)

        # Read Qleverfiles
        qleverfile_path = os.path.join(args.config_dir, f"Qleverfile.{args.community}")
        ui_config_path = os.path.join(args.config_dir, f"Qleverfile-ui-{args.community}.yml")

        if not os.path.exists(qleverfile_path):
            logging.error(f"Qleverfile not found: {qleverfile_path}")
            return 1

        with open(qleverfile_path, "r", encoding="utf-8") as f:
            qleverfile_content = f.read()

        ui_content = ""
        if os.path.exists(ui_config_path):
            with open(ui_config_path, "r", encoding="utf-8") as f:
                ui_content = f.read()

        slug = slugify(args.community)
        config_name = f"qlever-config-{slug}"
        ui_config_name = f"qlever-ui-{slug}"

        # Read docker-compose template
        if not os.path.exists(args.compose_file):
            logging.error(f"Compose file not found: {args.compose_file}")
            return 1

        with open(args.compose_file, "r", encoding="utf-8") as f:
            compose_content = f.read()

        # Build environment variables
        final_env = _build_stack_env(slug, args.env_file, getattr(args, "qlever_net", None), getattr(args, "host", None))

        if getattr(args, "dry_run", False):
            print(f"[dry-run] Would upload config: {config_name}")
            if ui_content:
                print(f"[dry-run] Would upload UI config: {ui_config_name}")
            print(f"[dry-run] Would deploy stack: {args.stack_name}")
            print(f"[dry-run] Environment variables: {[e['name'] for e in final_env]}")
            return 0

        if not _confirm_action(
            f"Deploy stack '{args.stack_name}' to {args.portainer_url}",
            getattr(args, "confirm", False),
        ):
            print("Aborted.")
            return 0

        client = PortainerClient(args.portainer_url)

        # Upload configs to Portainer
        print(f"Uploading Qleverfile as config: {config_name}")
        config_result = client.create_or_update_config(config_name, qleverfile_content)
        print(f"  Config created: {config_result.get('_versioned_name', config_name)}")

        if ui_content:
            print(f"Uploading UI config: {ui_config_name}")
            ui_result = client.create_or_update_config(ui_config_name, ui_content)
            print(f"  UI config created: {ui_result.get('_versioned_name', ui_config_name)}")

        # Create or update stack
        print(f"Deploying stack: {args.stack_name}")
        stack_result = client.create_or_update_stack(
            name=args.stack_name,
            stackfile_content=compose_content,
            env=final_env,
            endpoint_id=args.endpoint_id
        )
        print(f"Stack deployed successfully: {stack_result.get('Name', args.stack_name)}")
        return 0
    except Exception as e:
        logging.error(f"Failed to deploy: {_sanitize_token(str(e))}")
        return 1


def _handle_portainer_update(args) -> int:
    """Update an existing Portainer stack.

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code (0 for success, 1 for error)
    """
    try:
        _validate_template_files(args.compose_file, args.compose_file)

        # Read Qleverfiles
        qleverfile_path = os.path.join(args.config_dir, f"Qleverfile.{args.community}")
        ui_config_path = os.path.join(args.config_dir, f"Qleverfile-ui-{args.community}.yml")

        if not os.path.exists(qleverfile_path):
            logging.error(f"Qleverfile not found: {qleverfile_path}")
            return 1

        with open(qleverfile_path, "r", encoding="utf-8") as f:
            qleverfile_content = f.read()

        ui_content = ""
        if os.path.exists(ui_config_path):
            with open(ui_config_path, "r", encoding="utf-8") as f:
                ui_content = f.read()

        slug = slugify(args.community)
        config_name = f"qlever-config-{slug}"
        ui_config_name = f"qlever-ui-{slug}"

        # Read docker-compose template
        if not os.path.exists(args.compose_file):
            logging.error(f"Compose file not found: {args.compose_file}")
            return 1

        with open(args.compose_file, "r", encoding="utf-8") as f:
            compose_content = f.read()

        # Build environment variables

        final_env = _build_stack_env(slug, args.env_file, getattr(args, "qlever_net", None), getattr(args, "host", None))

        if getattr(args, "dry_run", False):
            print(f"[dry-run] Would update config: {config_name}")
            if ui_content:
                print(f"[dry-run] Would update UI config: {ui_config_name}")
            print(f"[dry-run] Would update stack: {args.stack_name}")
            if args.restart:
                print(f"[dry-run] Would restart stack: {args.stack_name}")
            return 0

        if not _confirm_action(
            f"Update stack '{args.stack_name}' on {args.portainer_url}",
            getattr(args, "confirm", False),
        ):
            print("Aborted.")
            return 0

        client = PortainerClient(args.portainer_url)

        # Upload configs
        print(f"Updating Qleverfile config: {config_name}")
        client.create_or_update_config(config_name, qleverfile_content)
        print(f"  Config updated")

        if ui_content:
            print(f"Updating UI config: {ui_config_name}")
            client.create_or_update_config(ui_config_name, ui_content)
            print(f"  UI config updated")

        # Update stack
        print(f"Updating stack: {args.stack_name}")
        stack_result = client.create_or_update_stack(
            name=args.stack_name,
            stackfile_content=compose_content,
            env=final_env,
            endpoint_id=args.endpoint_id
        )
        print(f"Stack updated successfully: {stack_result.get('Name', args.stack_name)}")

        # Optionally restart
        if args.restart:
            stack = client.find_stack(args.stack_name)
            if not stack:
                logging.warning(f"Stack {args.stack_name} not found for restart; skipping")
                return 0

            stack_id = stack.get("Id")
            if not stack_id:
                logging.error(f"Stack found but has no ID: {args.stack_name}")
                return 1

            print(f"Restarting stack {args.stack_name}...")
            client.restart_stack(stack_id, endpoint_id=args.endpoint_id)
            print("Stack restarted")

        return 0
    except Exception as e:
        logging.error(f"Failed to update stack: {_sanitize_token(str(e))}")
        return 1


def _handle_deploy_from_tenant(args) -> int:
    """Complete workflow from tenant to deployed stacks.

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code (0 for success, 1 for error)
    """
    try:
        _validate_template_files(args.facet_template, args.ui_template)

        # Generate configs
        base_url = getattr(args, "base_url", None) or args.base_release
        if not base_url and args.config_base:
            base_url = _derive_base_url(args.config_base)

        templates = {"facet": args.facet_template, "ui": args.ui_template}
        print("Generating Qleverfiles...")
        out = generate_from_location(
            config_base=args.config_base,
            config_name=args.config_name,
            templates=templates,
            out_base=args.out,
            base_release_url=args.base_release,
            s3_release_prefix=args.s3_release_prefix,
            base_url=base_url,
        )
        print(f"Generated configs for {len(out)} communities")

        if args.dry_run:
            print("Dry run mode - skipping deployment")
            for c in out.keys():
                stack_name = f"{args.stack_prefix}{c}"
                print(f"  Would deploy: {stack_name}")
            return 0

        # Deploy each community
        if not _confirm_action(
            f"Deploy {len(out)} community stacks to {args.portainer_url}",
            getattr(args, "confirm", False),
        ):
            print("Aborted.")
            return 0

        client = PortainerClient(args.portainer_url)
        for community in out.keys():
            stack_name = f"{args.stack_prefix}{community}"
            print(f"\nDeploying community: {community}")

            # Reuse deploy logic via direct call
            try:
                # Read Qleverfiles
                qleverfile_path = os.path.join(args.out, community, f"Qleverfile.{community}")
                ui_config_path = os.path.join(args.out, community, f"Qleverfile-ui-{community}.yml")

                with open(qleverfile_path, "r", encoding="utf-8") as f:
                    qleverfile_content = f.read()

                ui_content = ""
                if os.path.exists(ui_config_path):
                    with open(ui_config_path, "r", encoding="utf-8") as f:
                        ui_content = f.read()

                slug = slugify(community)
                config_name = f"qlever-config-{slug}"
                ui_config_name = f"qlever-ui-{slug}"

                print(f"  Uploading config: {config_name}")
                client.create_or_update_config(config_name, qleverfile_content)

                if ui_content:
                    print(f"  Uploading UI config: {ui_config_name}")
                    client.create_or_update_config(ui_config_name, ui_content)

                # Deploy stack
                with open(args.compose_file, "r", encoding="utf-8") as f:
                    compose_content = f.read()

                final_env = _build_stack_env(slug, args.env_file, getattr(args, "qlever_net", None), getattr(args, "host", None))

                print(f"  Deploying stack: {stack_name}")
                client.create_or_update_stack(
                    name=stack_name,
                    stackfile_content=compose_content,
                    env=final_env,
                    endpoint_id=args.endpoint_id
                )
                print(f"  Stack deployed: {stack_name}")
            except Exception as e:
                logging.error(f"Failed to deploy community {community}: {e}")
                return 1

        print("\nAll communities deployed successfully")
        return 0
    except Exception as e:
        logging.error(f"Failed deploy-from-tenant: {_sanitize_token(str(e))}")
        return 1


def main(argv=None):
    # Load .env file if present (e.g. PORTAINER_TOKEN, MINIO_ACCESS_KEY)
    from dotenv import load_dotenv
    load_dotenv()

    # Setup logging to file and console
    _setup_logging()

    p = argparse.ArgumentParser(prog="qleverctl")
    sub = p.add_subparsers(dest="cmd")

    gen = sub.add_parser("generate", help="Generate Qlever files for a tenant")
    gen.add_argument("--tenant", required=True, help="path to tenant.yaml (s3:// or http(s) or local file)")
    gen.add_argument("--gleaner", help="path to gleanerconfig.yaml")
    gen.add_argument("--base-release", help="base http URL for releases")
    gen.add_argument("--base-url", help="base URL written into the Qleverfile BASE_URL (defaults to --base-release)")
    gen.add_argument("--s3-release-prefix", help="s3://bucket/prefix to list release files")
    gen.add_argument("--facet-template", default="earthcube_utilities/resources/qlever/catalogues/data-example/QLeverfile.facetsearch")
    gen.add_argument("--ui-template", default="earthcube_utilities/resources/qlever/catalogues/data-example/QLeverfile-ui-example.yml")
    gen.add_argument("--out", default="build/qlever_generated")

    gfl = sub.add_parser("generate-from-location", help="Read tenant/gleaner configs from a shared location and generate Qlever files")
    gfl.add_argument("--config-base", required=True, help="base location (dir, http(s) or s3://) containing tenant.yaml and gleanerconfig.yaml or a folder of config_name")
    gfl.add_argument("--config-name", help="optional subfolder name under config-base where tenant.yaml and gleanerconfig.yaml live")
    gfl.add_argument("--base-release", help="base http URL for releases")
    gfl.add_argument("--base-url", help="base URL written into the Qleverfile BASE_URL (defaults to --base-release)")
    gfl.add_argument("--s3-release-prefix", help="s3://bucket/prefix to list release files")
    gfl.add_argument("--facet-template", default="earthcube_utilities/resources/qlever/catalogues/data-example/QLeverfile.facetsearch")
    gfl.add_argument("--ui-template", default="earthcube_utilities/resources/qlever/catalogues/data-example/QLeverfile-ui-example.yml")
    gfl.add_argument("--out", default="build/qlever_generated")

    _portainer_url_default = os.environ.get("PORTAINER_URL")
    _portainer_url_help = "Portainer API base URL (e.g. https://<host>/api/endpoints/<ENV_ID>/docker/). Falls back to PORTAINER_URL env var."

    plist = sub.add_parser("list-stacks", help="List all Portainer stacks")
    plist.add_argument("--portainer-url", default=_portainer_url_default, help=_portainer_url_help)

    pclist = sub.add_parser("list-configs", help="List all Docker configs in Portainer")
    pclist.add_argument("--portainer-url", default=_portainer_url_default, help=_portainer_url_help)

    # push-configs: upload Qleverfile/UI configs to Docker without deploying a stack
    ppush = sub.add_parser("push-configs", help="Upload Qleverfile and UI config to Portainer/Docker configs")
    ppush.add_argument("--portainer-url", default=_portainer_url_default, help=_portainer_url_help)
    ppush.add_argument("--config-dir", required=True, help="Directory containing generated Qleverfiles")
    ppush.add_argument("--community", required=True, help="Community name")
    ppush.add_argument("--dry-run", action="store_true", help="Show what would be uploaded without making API calls")

    # create-stack: create or update a Portainer stack
    pcreate = sub.add_parser("create-stack", help="Create (or update) a Portainer stack for a community")
    pcreate.add_argument("--portainer-url", default=_portainer_url_default, help=_portainer_url_help)
    pcreate.add_argument("--stack-name", help="Name for the Docker stack (defaults to qlever-<community>)")
    pcreate.add_argument("--config-dir", required=True, help="Directory containing generated Qleverfiles")
    pcreate.add_argument("--community", required=True, help="Community name")
    pcreate.add_argument("--compose-file", default="earthcube_utilities/resources/qlever/deployment/qlever_namespace.yaml", help="Path to docker-compose template")
    pcreate.add_argument("--env-file", help="Optional .env file with environment variables")
    pcreate.add_argument("--qlever-net", help="Docker network name for the qLever stack (default: from env-file)")
    pcreate.add_argument("--host", help="Hostname for the qLever stack (default: from env-file)")
    pcreate.add_argument("--endpoint-id", type=int, default=None, help="Portainer endpoint ID")
    pcreate.add_argument("--dry-run", action="store_true", help="Show what would be deployed without making API calls")
    pcreate.add_argument("--confirm", action="store_true", help="Skip interactive confirmation prompt")

    # update-stack: update an existing stack
    pupdate = sub.add_parser("update-stack", help="Update an existing Portainer stack")
    pupdate.add_argument("--portainer-url", default=_portainer_url_default, help=_portainer_url_help)
    pupdate.add_argument("--stack-name", required=True, help="Stack name to update")
    pupdate.add_argument("--config-dir", required=True, help="Directory containing updated Qleverfiles")
    pupdate.add_argument("--community", required=True, help="Community name")
    pupdate.add_argument("--compose-file", default="earthcube_utilities/resources/qlever/deployment/qlever_namespace.yaml", help="Path to docker-compose template")
    pupdate.add_argument("--env-file", help="Optional .env file with environment variables")
    pupdate.add_argument("--qlever-net", help="Docker network name for the qLever stack (default: from env-file)")
    pupdate.add_argument("--host", help="Hostname for the qLever stack (default: from env-file)")
    pupdate.add_argument("--restart", action="store_true", help="Restart stack after update")
    pupdate.add_argument("--endpoint-id", type=int, default=None, help="Portainer endpoint ID")
    pupdate.add_argument("--dry-run", action="store_true", help="Show what would be updated without making API calls")
    pupdate.add_argument("--confirm", action="store_true", help="Skip interactive confirmation prompt")

    # restart-stack: restart a stack
    prestart = sub.add_parser("restart-stack", help="Restart a Portainer stack")
    prestart.add_argument("--portainer-url", default=_portainer_url_default, help=_portainer_url_help)
    prestart.add_argument("--stack-name", required=True, help="Stack name to restart")
    prestart.add_argument("--endpoint-id", type=int, default=None, help="Portainer endpoint ID")
    prestart.add_argument("--confirm", action="store_true", help="Skip interactive confirmation prompt")

    deploy_tenant = sub.add_parser("deploy-from-tenant", help="Complete workflow from tenant.yaml to deployed Docker stacks")
    deploy_tenant.add_argument("--config-base", required=True, help="Base location containing tenant.yaml and gleanerconfig.yaml")
    deploy_tenant.add_argument("--config-name", help="Optional subfolder name under config-base")
    deploy_tenant.add_argument("--base-release", help="Base http URL for releases")
    deploy_tenant.add_argument("--base-url", help="base URL written into the Qleverfile BASE_URL (defaults to --base-release)")
    deploy_tenant.add_argument("--s3-release-prefix", help="s3://bucket/prefix to list release files")
    deploy_tenant.add_argument("--facet-template", default="earthcube_utilities/resources/qlever/catalogues/data-example/QLeverfile.facetsearch")
    deploy_tenant.add_argument("--ui-template", default="earthcube_utilities/resources/qlever/catalogues/data-example/QLeverfile-ui-example.yml")
    deploy_tenant.add_argument("--compose-file", default="earthcube_utilities/resources/qlever/deployment/qlever_namespace.yaml")
    deploy_tenant.add_argument("--portainer-url", default=_portainer_url_default, help=_portainer_url_help)
    deploy_tenant.add_argument("--stack-prefix", default="qlever_", help="Prefix for stack names (default: qlever_)")
    deploy_tenant.add_argument("--env-file", help="Optional .env file")
    deploy_tenant.add_argument("--qlever-net", help="Docker network name for the qLever stack (default: from env-file)")
    deploy_tenant.add_argument("--host", help="Hostname for the qLever stack (default: from env-file)")
    deploy_tenant.add_argument("--dry-run", action="store_true", help="Generate configs but don't deploy")
    deploy_tenant.add_argument("--confirm", action="store_true", help="Skip interactive confirmation prompt")
    deploy_tenant.add_argument("--endpoint-id", type=int,default=None, help="Portainer endpoint ID")
    deploy_tenant.add_argument("--out", default="build/qlever_generated")

    args = p.parse_args(argv)

    # Validate --portainer-url for commands that require it
    _needs_portainer = {"list-stacks", "list-configs", "push-configs", "create-stack", "update-stack", "restart-stack", "deploy-from-tenant"}
    if args.cmd in _needs_portainer and not getattr(args, "portainer_url", None):
        p.error("--portainer-url is required (or set PORTAINER_URL in environment / .env file)")

    # Dispatch to handler functions
    if args.cmd == "generate":
        return _handle_generate(args)
    elif args.cmd == "generate-from-location":
        return _handle_generate_from_location(args)
    elif args.cmd == "list-stacks":
        return _handle_portainer_list(args)
    elif args.cmd == "list-configs":
        return _handle_list_configs(args)
    elif args.cmd == "push-configs":
        return _handle_push_configs(args)
    elif args.cmd == "create-stack":
        if not getattr(args, "stack_name", None):
            args.stack_name = f"qlever-{slugify(args.community)}"
        return _handle_portainer_deploy(args)
    elif args.cmd == "update-stack":
        return _handle_portainer_update(args)
    elif args.cmd == "restart-stack":
        return _handle_portainer_restart(args)
    elif args.cmd == "deploy-from-tenant":
        return _handle_deploy_from_tenant(args)
    else:
        p.print_help()
        return 2


if __name__ == "__main__":
    sys.exit(main())
