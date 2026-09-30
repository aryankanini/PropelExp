import ast
from pathlib import Path
from typing import cast

import pytest

from adapters.filesystem.temporary_workspace import TemporaryWorkspace
from application.policies.transient_storage import (
    DurableStorageProhibitedError,
    validate_transient_storage,
)
from application.ports.case_repository import CaseRepository


BANNED_IMPORT_ROOTS = {
    "alembic",
    "django",
    "pymongo",
    "redis",
    "sqlalchemy",
    "sqlite3",
}
BANNED_DIRECTORY_NAMES = {"backups", "migrations"}


class DurableRepository:
    storage_kind = "database"


def test_source_has_no_durable_case_storage_mechanism() -> None:
    source_root = Path(__file__).parents[2] / "src"
    imported_roots: set[str] = set()

    for source_file in source_root.rglob("*.py"):
        tree = ast.parse(source_file.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported_roots.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported_roots.add(node.module.split(".")[0])

    assert imported_roots.isdisjoint(BANNED_IMPORT_ROOTS)
    assert not any(
        path.is_dir() and path.name.lower() in BANNED_DIRECTORY_NAMES
        for path in source_root.rglob("*")
    )


def test_composition_policy_rejects_durable_repository(tmp_path: Path) -> None:
    repository = cast(CaseRepository, DurableRepository())

    with pytest.raises(DurableStorageProhibitedError):
        validate_transient_storage(repository, TemporaryWorkspace(tmp_path))