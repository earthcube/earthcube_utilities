# qleverctl deployment Makefile
#
# Usage:
#   make dry-run-dev      # Preview what would be deployed (dev)
#   make deploy-dev       # Deploy all tenants to dev Portainer
#   make deploy-prod      # Deploy all tenants to production Portainer
#   make list-stacks      # List current stacks
#   make help             # Show all targets

# Configurable paths
CONFIG_BASE        ?= https://oss.geocodes-aws-dev.earthcube.org/geocodes/scheduler/configs/production
OUT_DIR            ?= build/qlever_generated
COMPOSE_FILE       ?= resources/qlever/deployment/qlever_namespace.yaml
FACET_TEMPLATE     ?= resources/qlever/catalogues/data-example/QLeverfile.facetsearch
UI_TEMPLATE        ?= resources/qlever/catalogues/data-example/QLeverfile-ui-example.yml

# S3 bucket and release path — used to discover *_release.nq files for communities with sources: [all]
QLEVER_BUCKET      ?= geocodes
S3_RELEASE_PREFIX  ?= https://oss.geocodes-aws-dev.earthcube.org/$(QLEVER_BUCKET)/graphs/latest

# Environment files
ENV_DEV  = .env
ENV_PROD = .env.production

# Common qleverctl flags
DEPLOY_FLAGS = --config-base $(CONFIG_BASE) \
               --compose-file $(COMPOSE_FILE) \
               --facet-template $(FACET_TEMPLATE) \
               --ui-template $(UI_TEMPLATE) \
               --s3-release-prefix $(S3_RELEASE_PREFIX) \
               --base-release $(S3_RELEASE_PREFIX) \
               --out $(OUT_DIR) \
               --confirm

# Helper to source env file and run qleverctl
define run_qleverctl
	set -a && . $(1) && set +a && qleverctl $(2)
endef

.PHONY: deploy-dev deploy-prod dry-run-dev dry-run-prod \
        generate list-stacks list-configs clean help

deploy-dev:
	@echo "==> Deploying all tenants (dev)..."
	$(call run_qleverctl,$(ENV_DEV),deploy-from-tenant $(DEPLOY_FLAGS) --env-file $(ENV_DEV))

deploy-prod:
	@echo "==> Deploying all tenants (production)..."
	$(call run_qleverctl,$(ENV_PROD),deploy-from-tenant $(DEPLOY_FLAGS) --env-file $(ENV_PROD))

dry-run-dev:
	@echo "==> Dry-run deploy (dev)..."
	$(call run_qleverctl,$(ENV_DEV),deploy-from-tenant $(DEPLOY_FLAGS) --dry-run)

dry-run-prod:
	@echo "==> Dry-run deploy (production)..."
	$(call run_qleverctl,$(ENV_PROD),deploy-from-tenant $(DEPLOY_FLAGS) --dry-run)

generate:
	qleverctl generate-from-location --config-base $(CONFIG_BASE) \
	    --facet-template $(FACET_TEMPLATE) --ui-template $(UI_TEMPLATE) \
	    --s3-release-prefix $(S3_RELEASE_PREFIX) --base-release $(S3_RELEASE_PREFIX) \
	    --out $(OUT_DIR)

list-stacks:
	$(call run_qleverctl,$(ENV_DEV),list-stacks)

list-configs:
	$(call run_qleverctl,$(ENV_DEV),list-configs)

clean:
	rm -rf $(OUT_DIR)

help:
	@echo "Targets:"
	@echo "  deploy-dev    Deploy all tenants to dev Portainer"
	@echo "  deploy-prod   Deploy all tenants to production Portainer"
	@echo "  dry-run-dev   Preview dev deployment (no changes)"
	@echo "  dry-run-prod  Preview production deployment (no changes)"
	@echo "  generate      Generate Qleverfiles only"
	@echo "  list-stacks   List Portainer stacks"
	@echo "  list-configs  List Docker configs"
	@echo "  clean         Remove generated files"
