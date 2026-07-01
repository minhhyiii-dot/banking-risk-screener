# Workflow Lock

## Folder Roles

Official frozen copy:

```text
final (ban de day len github & portfolio)
```

Working copy:

```text
banking-risk-screener-working
```

The official copy is the current source of truth and should remain untouched
until changes from the working copy have been reviewed.

## Change Policy

Do:

```text
- Make all edits in the working copy first.
- Keep model/data changes separate from repo cleanup changes.
- Verify Python scripts before promoting changes.
- Record important structure decisions in docs/.
```

Do not:

```text
- Edit the official frozen copy directly.
- Retrain or tune models during repository cleanup.
- Delete RapidMiner legacy files yet.
- Move core data files until path dependencies are reviewed.
- Push to GitHub before checking raw/sensitive/personal files.
```

## Current Phase

```text
Phase: repository and source organization
Model work: locked
Dataset work: locked
Deployment work: later
```
