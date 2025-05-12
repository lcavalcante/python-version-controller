"""
Entry point for running the package as a module.
"""

import os
import sys
import argparse
import structlog
from pyvc.cli import main, validate_args


log = structlog.get_logger()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="PyVC", description=__doc__)
    parser.add_argument("--root", type=str, default=".", required=False)
    parser.add_argument("--initial-version", type=str, required=False, default="0.1.0")
    parser.add_argument("--initial-commit", type=str, required=False, default="")

    args = parser.parse_args()
    root = os.getenv(key="PYVC_REPO_ROOT", default=args.root)
    version = os.getenv(key="PYVC_INITIAL_VERSION", default=args.initial_version)
    commit = os.getenv(key="PYVC_INITIAL_COMMIT", default=args.initial_commit)
    if not validate_args(root=root, version=version):
        sys.exit(1)

    main(root, version, commit)
