#!/usr/bin/env python3
"""
Flatten contracts/interfaces/libs into a single markdown file for LLM/NotebookLM ingestion.
"""

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, List, Set, Tuple


DEFAULT_DIRS = ["contracts", "src", "lib", "interfaces"]
DEFAULT_EXTS = [".sol", ".vy", ".vyi"]
DEFAULT_EXCLUDES = {"node_modules", "vendor", "build", "artifacts", "cache", ".git"}


def load_package_version(root: Path) -> str:
    pkg = root / "package.json"
    if not pkg.exists():
        return "unknown"
    try:
        with pkg.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return str(data.get("version", "unknown"))
    except Exception:
        return "unknown"


def language_for(ext: str) -> str:
    return {
        ".sol": "solidity",
        ".vy": "python",
        ".vyi": "python",
    }.get(ext.lower(), "")


def gather_files(root: Path, include_dirs: Iterable[str], extensions: Set[str]) -> List[Path]:
    files: List[Path] = []
    for rel in include_dirs:
        base = root / rel
        if not base.exists():
            continue
        for dirpath, dirnames, filenames in os.walk(base):
            # prune excluded dirs
            dirnames[:] = [d for d in dirnames if d not in DEFAULT_EXCLUDES]
            for name in filenames:
                if Path(name).suffix.lower() in extensions:
                    files.append(Path(dirpath) / name)
    return sorted(files)


def build_markdown(root: Path, files: List[Path], version: str) -> str:
    lines: List[str] = []
    lines.append("# Flattened Sources")
    lines.append(f"- repo: {root}")
    lines.append(f"- version: {version}")
    lines.append(f"- generated: {datetime.now(timezone.utc).isoformat()}")
    lines.append("")
    for path in files:
        rel = path.relative_to(root)
        lang = language_for(path.suffix)
        lines.append(f"## {rel.as_posix()}")
        lines.append(f"```{lang}".rstrip())
        try:
            with path.open("r", encoding="utf-8", errors="ignore") as f:
                lines.append(f.read())
        except Exception as e:
            lines.append(f"[error reading file: {e}]")
        lines.append("```")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Flatten contracts/interfaces/libs into a markdown file.")
    p.add_argument("repo_root", help="Path to the repository root.")
    p.add_argument(
        "--out",
        default="flatten.md",
        help="Output markdown file path (default: flatten.md in CWD).",
    )
    p.add_argument(
        "--dirs",
        nargs="+",
        default=DEFAULT_DIRS,
        help=f"Directories to include (default: {', '.join(DEFAULT_DIRS)}).",
    )
    p.add_argument(
        "--extensions",
        nargs="+",
        default=DEFAULT_EXTS,
        help="Extensions to include (default: .sol .vy .vyi).",
    )
    return p.parse_args()


def main() -> None:
    args = parse_args()
    root = Path(args.repo_root).resolve()
    out_path = Path(args.out).resolve()

    exts = {ext.lower() if ext.startswith(".") else f".{ext.lower()}" for ext in args.extensions}
    files = gather_files(root, args.dirs, exts)
    version = load_package_version(root)

    md = build_markdown(root, files, version)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(md, encoding="utf-8")

    print(f"Flattened {len(files)} files to {out_path}")
    print(f"Version: {version}")


if __name__ == "__main__":
    main()
