"""
CLI parsing for pyvc command.
"""

import structlog
from pathlib import Path, PurePath
from pygit2.repository import Repository
from pygit2.enums import SortMode

from pyvc.semver import SemVer


log = structlog.get_logger()


def validate_args(root: str, version: str) -> bool:
    is_valid = True
    repo_path = Path(root) / PurePath(".git")
    if not repo_path.exists():
        is_valid = False
        log.error("repo root does not exist", path=repo_path)

    try:
        SemVer.semver_from_string(version)
    except Exception as e:
        log.error("invalid initial version", error=str(e))
        is_valid = False

    return is_valid


def main(root: str, version: str) -> str:
    repo_path = Path(root) / PurePath(".git")
    semver = SemVer.semver_from_string(version)
    repo = Repository(str(repo_path))
    for commit in repo.walk(repo.head.target, SortMode.TOPOLOGICAL | SortMode.REVERSE):
        message = commit.message
        semver.bump_version(message)

    log.info(f"final version {str(semver)}")
    return str(semver)
