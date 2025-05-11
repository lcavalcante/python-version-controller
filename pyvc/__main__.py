"""
Entry point for running the package as a module.
"""

import sys
import argparse
import structlog
from pyvc.cli import main


log = structlog.get_logger()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="PyVC", description=__doc__)
    parser.add_argument("--root", type=str, default=".", required=False)
    parser.add_argument("--initial-version", type=str, required=False, default="0.1.0")

    args = parser.parse_args()

    try:
        main(args.root, args.initial_version)
    except Exception as e:
        log.error(f"Exception: {str(e)}")
        sys.exit(1)
