#!/usr/bin/env python3
"""
Entry point script for Gizmo.

This script allows running Gizmo directly from the repository without installing it.
"""

import sys
from gizmo.cli import main

if __name__ == "__main__":
    sys.exit(main())