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


def is_breaking_change(type: str, message: str) -> bool:
    """
    SemVer defines that a breaking change is a commit with a type ending in '!'
    OR that contains 'BREAKING CHANGE:' in the messsage body

    # Parameters:
    type (str): Commit message type (feat, fix, chore, etc)
    message (str): commit message content
    """
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
            semver["minor"] = 0
            semver["patch"] = 0
            log.debug("bump Major")
        elif commit_type == CommitEnum.FEAT:
            semver["minor"] += 1
            semver["patch"] = 0
            log.debug("bump Minor")
        elif commit_type == CommitEnum.FIX:
            semver["patch"] += 1
            log.debug("bump Patch")
        else:
            log.debug("no bump")
    else:
        log.info("not in conventional commit spec")
