from enum import StrEnum


import structlog


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


class SemVer:
    def __init__(self, major: int, minor: int, patch: int):
        self.major = major
        self.minor = minor
        self.patch = patch

        self.log = structlog.get_logger()

    def __repr__(self):
        return f"{self.major}.{self.minor}.{self.patch}"

    @staticmethod
    def is_breaking_change(type: str, message: str) -> bool:
        """
        SemVer defines that a breaking change is a commit with a type ending in '!'
        OR that contains 'BREAKING CHANGE:' in the messsage body

        # Parameters:
        type (str): Commit message type (feat, fix, chore, etc)
        message (str): commit message content
        """
        return type[-1] == "!" or "BREAKING CHANGE:" in message

    def bump_version(self, message: str) -> None:
        head = message.split("\n")[0]

        # TODO: regex?
        parsed_head = head.split(":")

        if len(parsed_head) > 1:
            commit_type = parsed_head[0].strip()
            head_text = parsed_head[1].strip()
            self.log = self.log.bind(tag=commit_type, text=head_text)

            if self.is_breaking_change(commit_type, message):
                self.major += 1
                self.minor = 0
                self.patch = 0
                self.log.debug("bump Major")
            elif commit_type == CommitEnum.FEAT:
                self.minor += 1
                self.patch = 0
                self.log.debug("bump Minor")
            elif commit_type == CommitEnum.FIX:
                self.patch += 1
                self.log.debug("bump Patch")
            else:
                self.log.debug("no bump")
        else:
            self.log.info("not in conventional commit spec", message=head)
