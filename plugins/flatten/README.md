# flatten

Flatten contracts/interfaces/libs into a single markdown file (with package version if available) for direct LLM/NotebookLM ingestion.

## What it does
- Scans scoped directories (contracts/src/lib/interfaces) for `.sol`, `.vy`, `.vyi`.
- Reads `package.json` version when present; labels as `unknown` otherwise.
- Emits one markdown file with path headers and language-tagged code fences.

## Layout
```
plugins/flatten/
├── README.md
└── skills/flatten/
    ├── SKILL.md
    ├── scripts/flatten.py
    ├── references/USAGE.md
    └── examples/sample_output.md
```

## Usage (CLI)
```bash
python3 {baseDir}/skills/flatten/scripts/flatten.py \
  /path/to/repo \
  --out /tmp/flatten.md \
  --dirs contracts src lib interfaces \
  --extensions .sol .vy .vyi
```

## Notes
- Read-only; intended for review/LLM ingestion, not compilation.
- Skips common vendor/build dirs (`node_modules`, `vendor`, `build`, `artifacts`, `cache`, `.git`).
- Keep outputs outside the target repo to avoid noise.
