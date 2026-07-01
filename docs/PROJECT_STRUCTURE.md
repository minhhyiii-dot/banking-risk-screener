# Project Structure

This document describes the current project layout before deeper cleanup.

## Top Level

```text
README.md
.gitignore
data dictionary.xlsx
code/
data/
outputs/
docs/
```

## code/

```text
code/Models/
```

Legacy RapidMiner workflows and their model-specific input files. Keep for now
as coursework/archive evidence.

```text
code/Notebooks/
```

Original notebooks for crawling, data building, and report EDA.

```text
code/python_migration_specs/
```

JSON specs extracted from RapidMiner `.rmp` workflows. The Python pipeline uses
these specs to preserve feature-set membership and workflow structure.

```text
code/python_pipeline/
```

Current reproducible Python baseline. This is the main codebase for portfolio
migration.

## data/

```text
data/Raw Data/
```

Raw source files. Review before any public push.

```text
data/old master dataset/
```

Archived dataset for the old Growth/Safe/Risky task.

```text
data/new master dataset/
```

Current dataset family for the Risk/NoRisk earnings-risk task.

## outputs/

```text
outputs/python_baseline/
```

Current Python baseline outputs: metrics, feature lists, predictions, and class
distribution reports.

## docs/

Project management and cleanup documentation. This folder is safe to expand
before the app build starts.

## Cleanup Notes

Current safe cleanup already done in the working copy:

```text
- Removed generated Python __pycache__ folders.
- Added docs/ workflow and structure notes.
- Rewrote README around the current migration/deployment plan.
```

Pending cleanup is tracked in `docs/CLEANUP_BACKLOG.md`.
