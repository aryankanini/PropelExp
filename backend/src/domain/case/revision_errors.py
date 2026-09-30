"""Domain failures for optimistic field revision checks."""


class StaleRevisionError(Exception):
    """Report the current revision when an edit is based on stale state."""

    def __init__(self, expected_revision_id: str, current_revision_id: str) -> None:
        super().__init__("The field revision is stale")
        self.expected_revision_id = expected_revision_id
        self.current_revision_id = current_revision_id