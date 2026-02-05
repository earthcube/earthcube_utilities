#!/usr/bin/env python3
from __future__ import annotations
import argparse
import logging
import logging.handlers
import os
import re
import sys
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


def _handle_generate_from_location(args) -> int:
    """Generate Qleverfiles from a shared config location.

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code (0 for success, 1 for error)
    """
    try:
        _validate_template_files(args.facet_template, args.ui_template)

        templates = {"facet": args.facet_template, "ui": args.ui_template}
        out = generate_from_location(
            config_base=args.config_base,
            config_name=args.config_name,
            templates=templates,
            out_base=args.out,
            base_release_url=args.base_release,
            s3_release_prefix=args.s3_release_prefix,
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

        print(f"Restarting stack: {args.stack_name}")
        client.restart_stack(stack_id, endpoint_id=args.endpoint_id)
        print("Stack restarted successfully")
        return 0
    except Exception as e:
        logging.error(f"Failed to restart stack: {_sanitize_token(str(e))}")
        return 1


def _handle_portainer_deploy(args) -> int:
    """Deploy Qleverfiles to Portainer.

    Args:
        args: Parsed command-line arguments

    Returns:
        Exit code (0 for success, 1 for error)
    """
    try:
        _validate_template_files(args.compose_file, args.compose_file)

        client = PortainerClient(args.portainer_url)

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

        # Upload configs to Portainer
        slug = slugify(args.community)
        config_name = f"qlever-config-{slug}"
        ui_config_name = f"qlever-ui-{slug}"

        print(f"Uploading Qleverfile as config: {config_name}")
        config_result = client.create_or_update_config(config_name, qleverfile_content)
        print(f"  Config created: {config_result.get('_versioned_name', config_name)}")

        if ui_content:
            print(f"Uploading UI config: {ui_config_name}")
            ui_result = client.create_or_update_config(ui_config_name, ui_content)
            print(f"  UI config created: {ui_result.get('_versioned_name', ui_config_name)}")

        # Read docker-compose template
        if not os.path.exists(args.compose_file):
            logging.error(f"Compose file not found: {args.compose_file}")
            return 1

        with open(args.compose_file, "r", encoding="utf-8") as f:
            compose_content = f.read()

        # Build environment variables
        env_vars = load_env_vars(args.env_file)
        default_envs = [
            {"name": "PROJECT", "value": slug},
            {"name": "QLEVER_CONFIG", "value": slug},
            {"name": "QLEVER_CONFIG_UI", "value": slug},
            {"name": "QLEVER_NET", "value": slug},
            {"name": "QLEVER_VOL", "value": slug},
        ]
        env_dict = {e["name"]: e["value"] for e in default_envs}
        for e in env_vars:
            env_dict[e["name"]] = e["value"]
        final_env = [{"name": k, "value": v} for k, v in env_dict.items()]

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

        client = PortainerClient(args.portainer_url)

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

        # Upload configs
        slug = slugify(args.community)
        config_name = f"qlever-config-{slug}"
        ui_config_name = f"qlever-ui-{slug}"

        print(f"Updating Qleverfile config: {config_name}")
        client.create_or_update_config(config_name, qleverfile_content)
        print(f"  Config updated")

        if ui_content:
            print(f"Updating UI config: {ui_config_name}")
            client.create_or_update_config(ui_config_name, ui_content)
            print(f"  UI config updated")

        # Read docker-compose template
        if not os.path.exists(args.compose_file):
            logging.error(f"Compose file not found: {args.compose_file}")
            return 1

        with open(args.compose_file, "r", encoding="utf-8") as f:
            compose_content = f.read()

        # Build environment variables
        env_vars = load_env_vars(args.env_file)
        default_envs = [
            {"name": "PROJECT", "value": slug},
            {"name": "QLEVER_CONFIG", "value": slug},
            {"name": "QLEVER_CONFIG_UI", "value": slug},
            {"name": "QLEVER_NET", "value": slug},
            {"name": "QLEVER_VOL", "value": slug},
        ]
        env_dict = {e["name"]: e["value"] for e in default_envs}
        for e in env_vars:
            env_dict[e["name"]] = e["value"]
        final_env = [{"name": k, "value": v} for k, v in env_dict.items()]

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
        templates = {"facet": args.facet_template, "ui": args.ui_template}
        print("Generating Qleverfiles...")
        out = generate_from_location(
            config_base=args.config_base,
            config_name=args.config_name,
            templates=templates,
            out_base=args.out,
            base_release_url=args.base_release,
            s3_release_prefix=args.s3_release_prefix,
        )
        print(f"Generated configs for {len(out)} communities")

        if args.dry_run:
            print("Dry run mode - skipping deployment")
            for c in out.keys():
                stack_name = f"{args.stack_prefix or ''}{c}"
                print(f"  Would deploy: {stack_name}")
            return 0

        # Deploy each community
        client = PortainerClient(args.portainer_url)
        for community in out.keys():
            stack_name = f"{args.stack_prefix or ''}{community}"
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

                env_vars = load_env_vars(args.env_file)
                default_envs = [
                    {"name": "PROJECT", "value": slug},
                    {"name": "QLEVER_CONFIG", "value": slug},
                    {"name": "QLEVER_CONFIG_UI", "value": slug},
                    {"name": "QLEVER_NET", "value": slug},
                    {"name": "QLEVER_VOL", "value": slug},
                ]
                env_dict = {e["name"]: e["value"] for e in default_envs}
                for e in env_vars:
                    env_dict[e["name"]] = e["value"]
                final_env = [{"name": k, "value": v} for k, v in env_dict.items()]

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
    # Setup logging to file and console
    _setup_logging()

    p = argparse.ArgumentParser(prog="qleverctl")
    sub = p.add_subparsers(dest="cmd")

    gen = sub.add_parser("generate", help="Generate Qlever files for a tenant")
    gen.add_argument("--tenant", required=True, help="path to tenant.yaml (s3:// or http(s) or local file)")
    gen.add_argument("--gleaner", help="path to gleanerconfig.yaml")
    gen.add_argument("--base-release", help="base http URL for releases")
    gen.add_argument("--s3-release-prefix", help="s3://bucket/prefix to list release files")
    gen.add_argument("--facet-template", default="earthcube_utilities/resources/qlever/catalogues/data-example/QLeverfile.facetsearch")
    gen.add_argument("--ui-template", default="earthcube_utilities/resources/qlever/catalogues/data-example/QLeverfile-ui-example.yml")
    gen.add_argument("--out", default="build/qlever_generated")

    gfl = sub.add_parser("generate-from-location", help="Read tenant/gleaner configs from a shared location and generate Qlever files")
    gfl.add_argument("--config-base", required=True, help="base location (dir, http(s) or s3://) containing tenant.yaml and gleanerconfig.yaml or a folder of config_name")
    gfl.add_argument("--config-name", help="optional subfolder name under config-base where tenant.yaml and gleanerconfig.yaml live")
    gfl.add_argument("--base-release", help="base http URL for releases")
    gfl.add_argument("--s3-release-prefix", help="s3://bucket/prefix to list release files")
    gfl.add_argument("--facet-template", default="earthcube_utilities/resources/qlever/catalogues/data-example/QLeverfile.facetsearch")
    gfl.add_argument("--ui-template", default="earthcube_utilities/resources/qlever/catalogues/data-example/QLeverfile-ui-example.yml")
    gfl.add_argument("--out", default="build/qlever_generated")

    plist = sub.add_parser("portainer-list", help="List all Portainer stacks")
    plist.add_argument("--portainer-url", required=True, help="Portainer API base URL")

    prestart = sub.add_parser("portainer-restart", help="Restart a Portainer stack")
    prestart.add_argument("--portainer-url", required=True, help="Portainer API base URL")
    prestart.add_argument("--stack-name", required=True, help="Stack name to restart")
    prestart.add_argument("--endpoint-id", type=int, default=1, help="Portainer endpoint ID")

    pdeploy = sub.add_parser("portainer-deploy", help="Deploy Qleverfiles to Portainer as a Docker stack")
    pdeploy.add_argument("--portainer-url", required=True, help="Portainer API base URL")
    pdeploy.add_argument("--stack-name", required=True, help="Name for the Docker stack")
    pdeploy.add_argument("--config-dir", required=True, help="Directory containing generated Qleverfiles")
    pdeploy.add_argument("--community", required=True, help="Community name")
    pdeploy.add_argument("--compose-file", default="earthcube_utilities/resources/qlever/deployment/qlever_namespace.yaml", help="Path to docker-compose template")
    pdeploy.add_argument("--env-file", help="Optional .env file with environment variables")
    pdeploy.add_argument("--endpoint-id", type=int, default=1, help="Portainer endpoint ID")

    pupdate = sub.add_parser("portainer-update", help="Update an existing Portainer stack")
    pupdate.add_argument("--portainer-url", required=True, help="Portainer API base URL")
    pupdate.add_argument("--stack-name", required=True, help="Stack name to update")
    pupdate.add_argument("--config-dir", required=True, help="Directory containing updated Qleverfiles")
    pupdate.add_argument("--community", required=True, help="Community name")
    pupdate.add_argument("--compose-file", default="earthcube_utilities/resources/qlever/deployment/qlever_namespace.yaml", help="Path to docker-compose template")
    pupdate.add_argument("--env-file", help="Optional .env file with environment variables")
    pupdate.add_argument("--restart", action="store_true", help="Restart stack after update")
    pupdate.add_argument("--endpoint-id", type=int, default=1, help="Portainer endpoint ID")

    deploy_tenant = sub.add_parser("deploy-from-tenant", help="Complete workflow from tenant.yaml to deployed Docker stacks")
    deploy_tenant.add_argument("--config-base", required=True, help="Base location containing tenant.yaml and gleanerconfig.yaml")
    deploy_tenant.add_argument("--config-name", help="Optional subfolder name under config-base")
    deploy_tenant.add_argument("--base-release", help="Base http URL for releases")
    deploy_tenant.add_argument("--s3-release-prefix", help="s3://bucket/prefix to list release files")
    deploy_tenant.add_argument("--facet-template", default="earthcube_utilities/resources/qlever/catalogues/data-example/QLeverfile.facetsearch")
    deploy_tenant.add_argument("--ui-template", default="earthcube_utilities/resources/qlever/catalogues/data-example/QLeverfile-ui-example.yml")
    deploy_tenant.add_argument("--compose-file", default="earthcube_utilities/resources/qlever/deployment/qlever_namespace.yaml")
    deploy_tenant.add_argument("--portainer-url", required=True, help="Portainer API base URL")
    deploy_tenant.add_argument("--stack-prefix", help="Optional prefix for stack names")
    deploy_tenant.add_argument("--env-file", help="Optional .env file")
    deploy_tenant.add_argument("--dry-run", action="store_true", help="Generate configs but don't deploy")
    deploy_tenant.add_argument("--endpoint-id", type=int, default=1, help="Portainer endpoint ID")
    deploy_tenant.add_argument("--out", default="build/qlever_generated")

    args = p.parse_args(argv)

    # Dispatch to handler functions
    if args.cmd == "generate":
        return _handle_generate(args)
    elif args.cmd == "generate-from-location":
        return _handle_generate_from_location(args)
    elif args.cmd == "portainer-list":
        return _handle_portainer_list(args)
    elif args.cmd == "portainer-restart":
        return _handle_portainer_restart(args)
    elif args.cmd == "portainer-deploy":
        return _handle_portainer_deploy(args)
    elif args.cmd == "portainer-update":
        return _handle_portainer_update(args)
    elif args.cmd == "deploy-from-tenant":
        return _handle_deploy_from_tenant(args)
    else:
        p.print_help()
        return 2


if __name__ == "__main__":
    sys.exit(main())
