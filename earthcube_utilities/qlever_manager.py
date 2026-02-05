#!/usr/bin/env python3
"""Deprecated module. The implementation moved to `src/ec/graph/qlever_manager.py`.

Importing this module will raise an informative error directing users to the
new implementation.
"""
raise ImportError(
    "The module 'earthcube_utilities.qlever_manager' has moved to 'ec.graph.qlever_manager'.\n"
    "Use: PYTHONPATH=src python3 -m ec.graph.cli ... or install the package and run 'qleverctl'."
)
