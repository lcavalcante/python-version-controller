from enum import StrEnum


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


def bump_version(type: str, message: str, semver: dict) -> None:
    if is_breaking_change(type, message):
        semver["major"] += 1
        print(f"{type} commit bump MAJOR")
    elif type == CommitEnum.FEAT:
        semver["minor"] += 1
        print(f"{type} commit bump MINOR")
    elif type == CommitEnum.FIX:
        semver["patch"] += 1
        print(f"{type} commit bump PATCH")
    else:
        print(f"{type} commit has no bump")


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
        head = message.split("\n")[0]
        parsed_head = head.split(":")
        if len(parsed_head) > 1:
            commit_type = parsed_head[0]
            bump_version(commit_type, message, semver)

        print(f"final version: {print_semver(semver)}")


if __name__ == "__main__":
    main()
