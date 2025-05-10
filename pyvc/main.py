from enum import StrEnum
import structlog

log = structlog.get_logger()


class CommitEnum(StrEnum):
    FEAT = "feat"
    FIX = "fix"
    BUILD = "build"
    CHORE = "chore"
    CI = "ci"
    DOCS = "docs"
    STYLE = "style"
    REFACTOR = "refactor"
    PERF = "perf"
    TEST = "test"
    BREAKING = "breaking change"


def is_breaking_change(type: str, message: str) -> bool:
    return type[-1] == "!" or "BREAKING CHANGE:" in message


def print_semver(semver: dict) -> str:
    return f"{semver.get('major', 0)}.{semver.get('minor', 0)}.{semver.get('patch')}"


def bump_version(message: str, semver: dict, log=log) -> None:
    head = message.split("\n")[0]

    # TODO: regex?
    parsed_head = head.split(":")

    if len(parsed_head) > 1:
        commit_type = parsed_head[0].strip()
        head_text = parsed_head[1].strip()
        log = log.bind(tag=commit_type, text=head_text)

        if is_breaking_change(commit_type, message):
            semver["major"] += 1
            log.debug("bump Major")
        elif commit_type == CommitEnum.FEAT:
            semver["minor"] += 1
            log.debug("bump Minor")
        elif commit_type == CommitEnum.FIX:
            semver["patch"] += 1
            log.debug("bump Patch")
        else:
            log.debug("no bump")
    else:
        log.info("not in conventional commit spec")


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
