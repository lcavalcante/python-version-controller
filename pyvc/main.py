import structlog
from semver import SemVer
from pygit2.repository import Repository
from pygit2.enums import SortMode


log = structlog.get_logger()


def main():
    semver = SemVer(0, 1, 0)

    repo = Repository(".git")

    for commit in repo.walk(repo.head.target, SortMode.TOPOLOGICAL | SortMode.REVERSE):
        message = commit.message
        semver.bump_version(message)

    log.info(f"final version {str(semver)}")


if __name__ == "__main__":
    main()
