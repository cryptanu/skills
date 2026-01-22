---
name: flatten
description: Flatten contracts/interfaces/libs into a single markdown file with version metadata for LLM consumption.
version: 1.0.0
category: code-analysis
tags: [flatten, bundling, solidity, vyper, llm, notebooklm]
author: Cryptanu
requires: [python3]
---

# Flatten Smart Contracts to Markdown

## Purpose
Bundle all contracts, interfaces, and libraries into one markdown artifact (with version info if available) that can be dropped directly into an LLM or NotebookLM session.

## When to Use
- You need a single-file snapshot of contracts/interfaces/libs for fast LLM ingestion.
- You want to preserve relative paths and package version metadata.
- You plan to review or annotate the flattened code in notebooks or documents.

## When NOT to Use
- The codebase is extremely large and unscoped; confirm directories first.
- You need compiler-ready flattened Solidity (this output is for reading, not compiling).
- You require dependency resolution for imports; this skill only concatenates source files.

## Rationalizations to Reject
- “It’s fine to include node_modules/build outputs.” → Exclude generated/vendor artifacts.
- “We don’t need to note versions.” → Always include package.json version when present.
- “Let’s include every file type.” → Stick to contract-related extensions unless explicitly requested.

## Prerequisites
- [ ] Python 3.8+ available.
- [ ] Target repository accessible and readable.
- [ ] Scope confirmed (directories, extensions, exclusions).
- [ ] `baseDir` points to the plugin root (scripts at `{baseDir}/skills/flatten/scripts/`).

## Defaults
- Directories: `contracts`, `src`, `lib`, `interfaces` (if they exist).
- Extensions: `.sol`, `.vy`, `.vyi`.
- Excludes: `node_modules`, `vendor`, `build`, `artifacts`, `cache`.
- Output: `flatten.md` in the current working directory unless overridden.

## Instructions for Agent
### Step 1: Confirm Scope
Ask the user for:
- Root path of the repo.
- Directories to include (default: contracts, src, lib, interfaces).
- Extensions to include (default: .sol .vy .vyi).
- Output path (default: ./flatten.md).

### Step 2: Run Flatten Script
Use the provided script (read-only):
```bash
python3 {baseDir}/skills/flatten/scripts/flatten.py \
  /path/to/repo \
  --out /path/to/flatten.md \
  --dirs contracts src lib interfaces \
  --extensions .sol .vy .vyi
```

### Step 3: Deliver Artifact
- Provide the output file path.
- Mention whether `package.json` was found and which version was recorded.
- Note any skipped directories or files (e.g., missing, unreadable).

### Output Format (Markdown)
- Header with repo path, timestamp, and version (if package.json exists).
- For each file (sorted by path):
  - `## <relative path>`
  - Code fence with language based on extension.

## Safety & Notes
- Read-only; do not modify the target repository.
- Avoid gigantic outputs—confirm scope if the project is very large.
- This is for LLM consumption, not for compilation/deployment.

## Example Prompt
```
@plugins/flatten/skills/flatten/SKILL.md
Flatten the contracts in ./dapp:
- dirs: contracts src
- extensions: .sol .vy
- out: /tmp/dapp-flatten.md
```

## Example Output (abridged)
```
# Flattened Sources
- repo: /path/to/repo
- version: 1.2.3 (from package.json)
- generated: 2026-02-00T00:00:00Z

## contracts/Token.sol
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;
// ...
```

## contracts/Token.vy
```python
# @version ^0.3.9
# ...
```
```
