"""Safe store identifiers for lifecycle cleanup failures."""

from enum import StrEnum


class CleanupStore(StrEnum):
    """Identify a transient store without exposing failure details."""

    CASE_MEMORY = "case_memory"
    WORKSPACE = "workspace"