#!/usr/bin/env python3
"""Validate repository examples and local Python references."""

from __future__ import annotations

import json
import re
import sys
import warnings
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = Path(__file__).resolve().parents[2]
SKIP_DIRS = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".serena",
    ".tox",
    ".venv",
    "__pycache__",
    "build",
    "dist",
    "venv",
}
MARKDOWN_LINK_RE = re.compile(r"\[[^\]]+\]\((?!https?://|mailto:|#)([^)\s]+?\.py)(?:#[^)]+)?\)")
BARE_PY_RE = re.compile(r"(?<![\w./-])([A-Za-z0-9_][A-Za-z0-9_.-]*\.py)(?![\w./-])")
FENCED_BLOCK_RE = re.compile(r"```.*?```", re.DOTALL)
NOTEBOOK_BAD_MAGIC_RE = re.compile(r"^%(?!(pip|load_ext|matplotlib)\b)\w+")
NOTEBOOK_VENV_PATH_RE = re.compile(r"\S*/\.venv/")


def is_project_file(path: Path, root: Path = ROOT) -> bool:
    relative = path.relative_to(root)
    return not any(part in SKIP_DIRS for part in relative.parts)


def iter_project_files(pattern: str) -> list[Path]:
    return sorted(path for path in ROOT.rglob(pattern) if path.is_file() and is_project_file(path))


def compile_python_files(paths: list[Path]) -> list[str]:
    errors: list[str] = []
    for path in paths:
        relative = path.relative_to(ROOT)
        try:
            source = path.read_text(encoding="utf-8")
            with warnings.catch_warnings():
                warnings.simplefilter("error", SyntaxWarning)
                compile(source, str(relative), "exec")
        except Exception as exc:  # noqa: BLE001 - report every validation failure consistently.
            errors.append(f"{relative}: compile failed: {exc}")
    return errors


def strip_fenced_blocks(text: str) -> str:
    return FENCED_BLOCK_RE.sub("", text)


def resolve_markdown_target(readme: Path, target: str) -> Path:
    clean_target = unquote(target.split("#", 1)[0])
    return (readme.parent / clean_target).resolve()


def validate_markdown_python_references(paths: list[Path]) -> list[str]:
    errors: list[str] = []
    for path in paths:
        relative = path.relative_to(ROOT)
        text = path.read_text(encoding="utf-8")

        for match in MARKDOWN_LINK_RE.finditer(text):
            target = resolve_markdown_target(path, match.group(1))
            if not target.exists():
                errors.append(f"{relative}: broken Python link: {match.group(1)}")

        text_without_code = strip_fenced_blocks(text)
        for match in BARE_PY_RE.finditer(text_without_code):
            target = resolve_markdown_target(path, match.group(1))
            if not target.exists():
                errors.append(f"{relative}: missing Python file reference: {match.group(1)}")
    return errors


def _output_text(output: dict) -> str:
    chunks = output.get("text")
    if not isinstance(chunks, str):
        chunks = "".join(chunks or [])
    data_text = output.get("data", {}).get("text/plain", "")
    if not isinstance(data_text, str):
        data_text = "".join(data_text)
    return f"{chunks}{data_text}"


def collect_notebooks(root: Path) -> list[Path]:
    return sorted(
        path for path in root.rglob("*.ipynb") if path.is_file() and is_project_file(path, root)
    )


def validate_notebooks(notebooks: list[Path]) -> list[str]:
    errors: list[str] = []
    for path in notebooks:
        relative = path.relative_to(REPO_ROOT)
        try:
            notebook = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            errors.append(f"{relative}: invalid JSON: {exc}")
            continue
        for index, cell in enumerate(notebook.get("cells", [])):
            if cell.get("cell_type") != "code":
                continue
            source_lines = "".join(cell.get("source", [])).splitlines()
            for line in source_lines:
                if NOTEBOOK_BAD_MAGIC_RE.search(line):
                    errors.append(f"{relative}: cell {index}: unsupported magic: {line.strip()}")
            for output in cell.get("outputs", []):
                if output.get("output_type") == "error":
                    errors.append(f"{relative}: cell {index}: stored error output")
                text = _output_text(output)
                if NOTEBOOK_VENV_PATH_RE.search(text):
                    errors.append(f"{relative}: cell {index}: output leaks .venv path")
    return errors


def main() -> int:
    python_files = iter_project_files("*.py")
    markdown_files = iter_project_files("*.md")
    notebooks = collect_notebooks(REPO_ROOT)

    errors = [
        *compile_python_files(python_files),
        *validate_markdown_python_references(markdown_files),
        *validate_notebooks(notebooks),
    ]

    if errors:
        print("Validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        f"OK: compiled {len(python_files)} Python files and checked "
        f"{len(markdown_files)} Markdown files and {len(notebooks)} notebooks."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
