"""Verify independent frontend and backend application boundaries."""

import ast
import json
from pathlib import Path
import re
import subprocess
import sys
import tomllib


IMPORT_SPECIFIER = re.compile(
    r"(?:from\s+|import\s*\(|import\s+)[\"']([^\"']+)[\"']"
)


def verify_application_boundaries(repository_root: Path) -> list[str]:
    violations = _verify_application_artifacts(repository_root)
    violations.extend(_find_frontend_boundary_violations(repository_root))
    violations.extend(_find_backend_boundary_violations(repository_root))
    return violations


def _verify_application_artifacts(repository_root: Path) -> list[str]:
    required_paths = (
        "frontend/package.json",
        "frontend/package-lock.json",
        "frontend/.env.example",
        "frontend/dist",
        "backend/pyproject.toml",
        "backend/.env.example",
        "backend/dist",
    )
    violations = [
        f"missing required application artifact: {path}"
        for path in required_paths
        if not (repository_root / path).exists()
    ]

    frontend_manifest = repository_root / "frontend" / "package.json"
    if frontend_manifest.exists():
        package_data = json.loads(frontend_manifest.read_text(encoding="utf-8"))
        scripts = package_data.get("scripts", {})
        for command in ("build", "test"):
            if command not in scripts:
                violations.append(f"frontend/package.json: missing {command} script")

    backend_manifest = repository_root / "backend" / "pyproject.toml"
    if backend_manifest.exists():
        project_data = tomllib.loads(backend_manifest.read_text(encoding="utf-8"))
        if "pytest" not in project_data.get("tool", {}):
            violations.append("backend/pyproject.toml: missing pytest command configuration")
        if "build-system" not in project_data:
            violations.append("backend/pyproject.toml: missing build output configuration")
    return violations


def _find_frontend_boundary_violations(repository_root: Path) -> list[str]:
    frontend_source = repository_root / "frontend" / "src"
    backend_root = (repository_root / "backend").resolve()
    violations: list[str] = []
    for source_file in frontend_source.rglob("*"):
        if source_file.suffix not in {".js", ".jsx", ".ts", ".tsx"}:
            continue
        source = source_file.read_text(encoding="utf-8")
        for specifier in IMPORT_SPECIFIER.findall(source):
            resolved_import = (source_file.parent / specifier).resolve()
            if "backend" in Path(specifier).parts or resolved_import.is_relative_to(
                backend_root
            ):
                violations.append(
                    f"{source_file}: cross-application import {specifier}"
                )
    return violations


def _find_backend_boundary_violations(repository_root: Path) -> list[str]:
    backend_source = repository_root / "backend" / "src"
    violations: list[str] = []
    for source_file in backend_source.rglob("*.py"):
        tree = ast.parse(source_file.read_text(encoding="utf-8"), filename=source_file)
        for node in ast.walk(tree):
            imported_modules = _imported_modules(node)
            for module_name in imported_modules:
                if module_name == "frontend" or module_name.startswith("frontend."):
                    violations.append(
                        f"{source_file}: cross-application import {module_name}"
                    )
    return violations


def _imported_modules(node: ast.AST) -> tuple[str, ...]:
    if isinstance(node, ast.Import):
        return tuple(alias.name for alias in node.names)
    if isinstance(node, ast.ImportFrom) and node.module:
        return (node.module,)
    return ()


def _run_core_dependency_test(repository_root: Path) -> int:
    backend_root = repository_root / "backend"
    test_path = "tests/architecture/test_dependency_boundaries.py"
    result = subprocess.run(
        [sys.executable, "-m", "pytest", test_path, "-q"],
        cwd=backend_root,
        check=False,
    )
    return result.returncode


def main() -> int:
    repository_root = Path(__file__).resolve().parents[1]
    violations = verify_application_boundaries(repository_root)
    if violations:
        print("\n".join(violations), file=sys.stderr)
        return 1
    if _run_core_dependency_test(repository_root) != 0:
        return 1
    print("Application boundaries verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())