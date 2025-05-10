import structlog
from bump import bump_version, print_semver


log = structlog.get_logger()

mock_commits = [
    "chore: initial commit",
    "feat: add stuff",
    "fix: fix stuff",
    "style: beautiful stuff",
    "feat!: sorry broke stuff",
    "fix: stuff is hard.",
    "perf: BREAKING CHANGE: fast stuff goes hard",
    "docs: wrote stuff",
]


def main():
    semver = {
        "major": 0,
        "minor": 1,
        "patch": 0,
    }

    for message in mock_commits:
        bump_version(message, semver)

    log.info(f"final version {print_semver(semver)}")


if __name__ == "__main__":
    main()
