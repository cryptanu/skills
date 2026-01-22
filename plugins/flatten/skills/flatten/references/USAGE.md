# Flatten Skill Usage Notes

## Included
- Directories: `contracts`, `src`, `lib`, `interfaces` (if present).
- Extensions: `.sol`, `.vy`, `.vyi`.
- Version: pulled from `package.json` when available (else `unknown`).

## Excluded by default
- `node_modules`, `vendor`, `build`, `artifacts`, `cache`, `.git`.

## Output format
- Single markdown file.
- Header: repo path, version, generated timestamp (UTC).
- Sections: one per file (`## <relative path>`), fenced code with language set from extension.

## Safety
- Read-only; no repo modifications.
- Confirm scope for large repos to avoid huge outputs.
- Not a compiler-ready flatten; intended for review/LLM ingestion.

## CLI reference
```bash
python3 {baseDir}/skills/flatten/scripts/flatten.py \
  /path/to/repo \
  --out /tmp/flatten.md \
  --dirs contracts src lib interfaces \
  --extensions .sol .vy .vyi
```

## Tips
- For very large repos, narrow `--dirs` or `--extensions`.
- Store outputs outside the repo (e.g., `/tmp/flatten.md`) to keep the tree clean.
