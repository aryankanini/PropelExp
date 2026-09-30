import ast
from pathlib import Path


FORBIDDEN_IMPORT_ROOTS = {
    "anthropic",
    "azure",
    "boto3",
    "botocore",
    "django",
    "fastapi",
    "flask",
    "google.cloud",
    "openai",
    "starlette",
    "uvicorn",
}


def find_forbidden_imports(source_roots: tuple[Path, ...]) -> list[str]:
    violations: list[str] = []
    for source_root in source_roots:
        if not source_root.exists():
            continue
        for source_file in source_root.rglob("*.py"):
            imported_modules = _read_imports(source_file)
            for module_name in imported_modules:
                if _is_forbidden(module_name):
                    violations.append(f"{source_file}: forbidden import {module_name}")
    return violations


def _read_imports(source_file: Path) -> tuple[str, ...]:
    tree = ast.parse(source_file.read_text(encoding="utf-8"), filename=source_file)
    imports: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.append(node.module)
    return tuple(imports)


def _is_forbidden(module_name: str) -> bool:
    return any(
        module_name == root or module_name.startswith(f"{root}.")
        for root in FORBIDDEN_IMPORT_ROOTS
    )


def test_domain_and_application_packages_have_inward_dependencies() -> None:
    source_root = Path(__file__).parents[2] / "src"
    core_roots = (
        source_root / "domain",
        source_root / "application",
        source_root / "cms_planner" / "domain",
        source_root / "cms_planner" / "application",
    )

    violations = find_forbidden_imports(core_roots)

    assert violations == [], "\n".join(violations)


def test_forbidden_import_diagnostic_identifies_importing_file(
    tmp_path: Path,
) -> None:
    importing_file = tmp_path / "application" / "unsafe_service.py"
    importing_file.parent.mkdir()
    importing_file.write_text("from fastapi import Request\n", encoding="utf-8")

    violations = find_forbidden_imports((tmp_path,))

    assert violations == [f"{importing_file}: forbidden import fastapi"]