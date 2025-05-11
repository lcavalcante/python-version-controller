"""
CLI parsing for pyvc command.
"""

import structlog
from pathlib import Path, PurePath
from pygit2.repository import Repository
from pygit2.enums import SortMode

from pyvc.semver import SemVer


log = structlog.get_logger()


def main(root: str, version: str):
    repo_path = Path(root) / PurePath(".git")
    if not repo_path.exists():
        log.error("repo root does not exist", path=repo_path)
        raise Exception("repo root invalid path")
    semver = SemVer.semver_from_string(version)

    repo = Repository(str(repo_path))
    for commit in repo.walk(repo.head.target, SortMode.TOPOLOGICAL | SortMode.REVERSE):
        message = commit.message
        semver.bump_version(message)

    log.info(f"final version {str(semver)}")
