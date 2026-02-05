#!/usr/bin/env python3
"""Deprecated wrapper for the new qleverctl CLI.

This script was replaced by the entry point `qleverctl` provided by the
`ec.graph` package. Please use that instead. You can run it without
installation via:

  PYTHONPATH=src python3 -m ec.graph.cli <command> [options]

Or after installing the package: `qleverctl <command> [options]`.
"""
import sys

print("[DEPRECATED] scripts/qleverctl.py has moved to the new package entrypoint 'qleverctl'.")
print("Use: PYTHONPATH=src python3 -m ec.graph.cli ... or install the package and run 'qleverctl'")
sys.exit(1)
