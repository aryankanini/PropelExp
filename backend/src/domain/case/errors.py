"""Domain failures for transient case ownership."""


class ActiveCaseExistsError(Exception):
    """Raised when a session already owns an active case."""

    def __init__(self, session_id: str) -> None:
        super().__init__(f"Session {session_id!r} already has an active case")
        self.session_id = session_id


class CaseNotFoundError(Exception):
    """Raised when a session has no active case to update."""

    def __init__(self, session_id: str) -> None:
        super().__init__(f"Session {session_id!r} has no active case")
        self.session_id = session_id