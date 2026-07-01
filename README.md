# Vietnamese Banking Earnings Risk Screener

This repository is the working copy for preparing a portfolio/demo version of:

```text
Machine Learning-based Stock Investment Decision Support
for Vietnamese Banking Stocks Using Earnings-Risk Screening
```

Current priority: keep the existing Python baseline reproducible. Do not change
the model, target, dataset, or web app scope until the project files are clean
and the baseline can be run end to end.

## Repository Status

This is the working copy. The frozen official copy is kept separately and should
not be edited directly.

Use this workflow:

```text
1. Make changes in the working copy.
2. Verify the Python baseline and project files.
3. Only after review, copy approved changes into the official copy.
4. Push/deploy from the official copy later.
```

See `docs/WORKFLOW_LOCK.md` for the current folder policy.

## Current Structure

```text
code/
  Models/                    Legacy RapidMiner workflows and model input files
  Notebooks/                 Coursework notebooks for data build and EDA
  python_migration_specs/    Extracted RapidMiner workflow specs
  python_pipeline/           Reproducible Python baseline

data/
  Raw Data/                  Raw source files
  old master dataset/        Archived Growth/Safe/Risky dataset
  new master dataset/        Earnings Risk/NoRisk datasets

outputs/
  python_baseline/           Current Python baseline metrics and predictions

docs/
  Project workflow and cleanup notes for the portfolio migration
```

More detail is in `docs/PROJECT_STRUCTURE.md`.

## Python Baseline

The Python baseline lives in:

```text
code/python_pipeline
```

Run all current baselines from the repository root:

```bash
python code/python_pipeline/run_all_baselines.py
```

Run class distribution report:

```bash
python code/python_pipeline/class_balance_report.py
```

Outputs are written to:

```text
outputs/python_baseline
```

## Current Modeling Scope

Archived old task:

```text
Growth / Safe / Risky
```

Current earnings-risk task:

```text
Risk / NoRisk
```

Important rule for this phase:

```text
Do not retrain, redesign targets, tune thresholds, or add imbalance experiments
until the file/source structure is stable.
```

## Demo/App Scope For Later

The intended MVP demo is a static Cloudflare Pages app:

```text
Home
Screener
Model
Limitations
```

For now, do not build or deploy the app. The next immediate task is repository
cleanup and reproducibility.

## Notes

- RapidMiner files are legacy/coursework artifacts.
- The Python pipeline is the base for the portfolio version.
- Raw data and large generated files should be reviewed before any public GitHub
  push.
- The project is an educational decision-support demo, not a buy/sell signal.
