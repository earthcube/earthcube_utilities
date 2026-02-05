#!/usr/bin/env python3
from __future__ import annotations
import argparse
import logging
import os
from ec.graph.qlever_manager import (
    generate_for_tenant,
    generate_from_location,
    PortainerClient,
    load_env_vars,
    slugify,
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main(argv=None):
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

    # Portainer commands
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
    deploy_tenant.add_argument("--portainer-url", required=True, help="Portainer API base URL")
    deploy_tenant.add_argument("--stack-prefix", help="Optional prefix for stack names")
    deploy_tenant.add_argument("--dry-run", action="store_true", help="Generate configs but don't deploy")
    deploy_tenant.add_argument("--endpoint-id", type=int, default=1, help="Portainer endpoint ID")
    deploy_tenant.add_argument("--out", default="build/qlever_generated")

    args = p.parse_args(argv)

    if args.cmd == "generate":
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

    if args.cmd == "generate-from-location":
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

    if args.cmd == "portainer-list":
        client = PortainerClient(args.portainer_url)
        stacks = client.list_stacks()
        print(f"Found {len(stacks)} stacks:")
        for stack in stacks:
            status = stack.get("Status", "unknown")
            name = stack.get("Name", "unknown")
            stack_id = stack.get("Id", "?")
            print(f"  [{stack_id}] {name} - {status}")
        return 0

    if args.cmd == "portainer-restart":
        client = PortainerClient(args.portainer_url)
        stack = client.find_stack(args.stack_name)
        if not stack:
            print(f"Stack {args.stack_name} not found")
            return 1
        stack_id = stack.get("Id")
        if stack_id is None:
            print(f"Stack {args.stack_name} has no ID")
            return 1
        print(f"Restarting stack {args.stack_name} (id={stack_id})...")
        result = client.restart_stack(stack_id, endpoint_id=args.endpoint_id)
        print(f"Stack restarted: {result}")
        return 0

    if args.cmd == "portainer-deploy":
        client = PortainerClient(args.portainer_url)

        # Read Qleverfiles
        qleverfile_path = os.path.join(args.config_dir, f"Qleverfile.{args.community}")
        ui_config_path = os.path.join(args.config_dir, f"Qleverfile-ui-{args.community}.yml")

        if not os.path.exists(qleverfile_path):
            print(f"Qleverfile not found: {qleverfile_path}")
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
        with open(args.compose_file, "r", encoding="utf-8") as f:
            compose_content = f.read()

        # Build environment variables
        env_vars = load_env_vars(args.env_file)
        # Add default env vars
        default_envs = [
            {"name": "PROJECT", "value": slug},
            {"name": "QLEVER_CONFIG", "value": slug},
            {"name": "QLEVER_CONFIG_UI", "value": slug},
            {"name": "QLEVER_NET", "value": slug},
            {"name": "QLEVER_VOL", "value": slug},
        ]
        # Merge, with file values taking precedence
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

    if args.cmd == "portainer-update":
        client = PortainerClient(args.portainer_url)

        # Read updated Qleverfiles
        qleverfile_path = os.path.join(args.config_dir, f"Qleverfile.{args.community}")
        ui_config_path = os.path.join(args.config_dir, f"Qleverfile-ui-{args.community}.yml")

        if not os.path.exists(qleverfile_path):
            print(f"Qleverfile not found: {qleverfile_path}")
            return 1

        with open(qleverfile_path, "r", encoding="utf-8") as f:
            qleverfile_content = f.read()

        ui_content = ""
        if os.path.exists(ui_config_path):
            with open(ui_config_path, "r", encoding="utf-8") as f:
                ui_content = f.read()

        # Upload new configs
        slug = slugify(args.community)
        config_name = f"qlever-config-{slug}"
        ui_config_name = f"qlever-ui-{slug}"

        print(f"Uploading updated Qleverfile: {config_name}")
        config_result = client.create_or_update_config(config_name, qleverfile_content)
        print(f"  Config created: {config_result.get('_versioned_name', config_name)}")

        if ui_content:
            print(f"Uploading updated UI config: {ui_config_name}")
            ui_result = client.create_or_update_config(ui_config_name, ui_content)
            print(f"  UI config created: {ui_result.get('_versioned_name', ui_config_name)}")

        # Read docker-compose template
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
            if stack:
                stack_id = stack.get("Id")
                if stack_id:
                    print(f"Restarting stack {args.stack_name}...")
                    client.restart_stack(stack_id, endpoint_id=args.endpoint_id)
                    print("Stack restarted")

        return 0

    if args.cmd == "deploy-from-tenant":
        # First, generate configs
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
        deployed = []
        failed = []

        for community, paths in out.items():
            stack_name = f"{args.stack_prefix or ''}{community}"
            print(f"\nDeploying {community} as stack {stack_name}...")

            try:
                # Read Qleverfiles
                qleverfile_path = paths.get("facet")
                ui_config_path = paths.get("ui")

                if not qleverfile_path or not os.path.exists(qleverfile_path):
                    print(f"  Skipping - Qleverfile not found")
                    failed.append((community, "Qleverfile not found"))
                    continue

                with open(qleverfile_path, "r", encoding="utf-8") as f:
                    qleverfile_content = f.read()

                ui_content = ""
                if ui_config_path and os.path.exists(ui_config_path):
                    with open(ui_config_path, "r", encoding="utf-8") as f:
                        ui_content = f.read()

                # Upload configs
                slug = slugify(community)
                config_name = f"qlever-config-{slug}"
                ui_config_name = f"qlever-ui-{slug}"

                print(f"  Uploading configs...")
                client.create_or_update_config(config_name, qleverfile_content)
                if ui_content:
                    client.create_or_update_config(ui_config_name, ui_content)

                # Read compose template
                compose_template = args.facet_template.replace("QLeverfile.facetsearch", "../deployment/qlever_namespace.yaml")
                if not os.path.exists(compose_template):
                    compose_template = "earthcube_utilities/resources/qlever/deployment/qlever_namespace.yaml"

                with open(compose_template, "r", encoding="utf-8") as f:
                    compose_content = f.read()

                # Build env vars
                default_envs = [
                    {"name": "PROJECT", "value": slug},
                    {"name": "QLEVER_CONFIG", "value": slug},
                    {"name": "QLEVER_CONFIG_UI", "value": slug},
                    {"name": "QLEVER_NET", "value": slug},
                    {"name": "QLEVER_VOL", "value": slug},
                ]

                # Deploy stack
                print(f"  Creating/updating stack...")
                client.create_or_update_stack(
                    name=stack_name,
                    stackfile_content=compose_content,
                    env=default_envs,
                    endpoint_id=args.endpoint_id
                )
                deployed.append(community)
                print(f"  ✓ Deployed successfully")

            except Exception as e:
                logger.exception(f"Failed to deploy {community}")
                failed.append((community, str(e)))
                print(f"  ✗ Failed: {e}")

        # Print summary
        print(f"\n{'='*60}")
        print(f"Deployment Summary")
        print(f"{'='*60}")
        print(f"Successfully deployed: {len(deployed)}")
        for c in deployed:
            print(f"  ✓ {c}")

        if failed:
            print(f"\nFailed: {len(failed)}")
            for c, err in failed:
                print(f"  ✗ {c}: {err}")

        return 0 if not failed else 1

    p.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
