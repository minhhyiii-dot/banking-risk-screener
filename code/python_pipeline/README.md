# Python Migration Baseline

This folder is the Python reimplementation of the original RapidMiner workflows.

The goal of this first migration is not to improve the model yet. The goal is to
reproduce the old workflow logic in readable Python so future class-imbalance and
model-quality experiments can be done safely.

## What This Covers

- `OLD1`: Decision Tree for the archived Growth/Safe/Risky task.
- `OLD2`: Random Forest for the archived Growth/Safe/Risky task.
- `OLD3`: Gradient Boosted Trees-style baseline for the archived Growth/Safe/Risky task.
- `NEW1`: Two-member earnings-risk ensemble using Risk5 training label and Risk10 evaluation label.
- `NEW2`: Prequential earnings-risk challenger using 10-year rolling training windows.

RapidMiner `.rmp` files are treated as legacy specifications. Feature sets,
labels, weights, thresholds, and split rules are extracted from the `.rmp` XML
where possible.

## Run

From the project root:

```bash
python code/python_pipeline/run_all_baselines.py
```

Outputs are written to:

```text
outputs/python_baseline
```

You can also run individual parts:

```bash
python code/python_pipeline/run_old_models.py
python code/python_pipeline/run_new1.py
python code/python_pipeline/run_new2.py --kind both
python code/python_pipeline/class_balance_report.py
```

## Important Notes

- The Python models are not expected to be binary-identical to RapidMiner/H2O.
- The split logic, labels, feature sets, sample weights, and ensemble formulas
  are the parts that must match first.
- After this baseline is stable, class imbalance experiments should be added as
  separate experiment configs rather than changing the baseline scripts directly.

## Current Migration Status

- Dataset loading: done.
- RMP XML spec extraction: done.
- OLD1/OLD2/OLD3 Python baselines: done.
- NEW1 two-member Python baseline: done.
- NEW2 prequential Python baseline: done.
- Class distribution report: done.
- Next phase: add explicit imbalance experiments after freezing these Python
  baseline metrics.
