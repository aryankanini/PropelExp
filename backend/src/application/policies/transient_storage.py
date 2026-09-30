"""Composition policy that prohibits durable case storage."""

from application.ports.case_repository import CaseRepository
from application.ports.workspace import Workspace


class DurableStorageProhibitedError(Exception):
    """Raised when case state is wired to a durable store."""


def validate_transient_storage(
    repository: CaseRepository,
    workspace: Workspace,
) -> None:
    """Accept only process memory and temporary workspace storage kinds."""
    if repository.storage_kind != "memory":
        raise DurableStorageProhibitedError("Case repository must use process memory")
    if workspace.storage_kind != "temporary":
        raise DurableStorageProhibitedError("Workspace must use temporary storage")