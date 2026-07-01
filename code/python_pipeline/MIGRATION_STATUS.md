# Python Migration Status

## Current State

The project now has a Python baseline pipeline next to the original RapidMiner
workflows.

This is the first migration layer. It is intended to preserve the existing
model logic before improving class imbalance, calibration, or portfolio polish.

## Implemented

- Extract RapidMiner `.rmp` XML specs into `code/python_migration_specs`.
- Rebuild OLD1/OLD2/OLD3 as Python baselines.
- Rebuild NEW1 as a two-member ensemble:
  - 258-feature member.
  - 309-feature member.
  - Risk5 training label.
  - Risk10 evaluation label.
  - `mg002_distance_weight` and `mg035_positive_weight`.
- Rebuild NEW2 as a prequential model:
  - `pq_role = train` rows train each evaluation quarter.
  - `pq_role = score` rows are scored.
  - 258/309 feature members.
  - 75/25 ensemble.
  - Fixed threshold from RapidMiner workflow.
- Export predictions, metrics, feature lists, and class-distribution reports.

## Output Location

```text
outputs/python_baseline
```

Important files:

```text
outputs/python_baseline/old_models_summary.json
outputs/python_baseline/NEW1/new1_metrics.json
outputs/python_baseline/NEW2/validation/new2_validation_metrics.json
outputs/python_baseline/NEW2/test/new2_test_metrics.json
outputs/python_baseline/class_distribution/class_distribution_summary.csv
```

## Baseline Metrics From Current Python Run

These numbers are from the Python reimplementation, not the original
RapidMiner/H2O binary.

| Model | Split | Accuracy | Risk Recall / Macro-F1 Note |
|---|---:|---:|---|
| OLD1 | test | 36.06% | Archived 3-class task |
| OLD2 | test | 43.75% | Archived 3-class task |
| OLD3 | test | 38.94% | Archived 3-class task |
| NEW1 | test at threshold 0.437 | 80.77% | Risk recall 45.00%, macro-F1 66.41% |
| NEW2 | validation | 75.00% | Risk recall 47.37%, macro-F1 65.05% |
| NEW2 | test | 81.62% | Risk recall 52.50%, macro-F1 69.09% |

## Why Metrics Can Differ From RapidMiner

RapidMiner used native H2O Gradient Boosted Trees. The Python baseline uses
XGBoost/sklearn equivalents to preserve the pipeline structure in code. Exact
binary-identical predictions are not expected.

The migration target is:

1. Same datasets.
2. Same temporal split rules.
3. Same labels and sample weights.
4. Same feature-set membership.
5. Same ensemble and threshold formulas.

After those are stable, the model can be improved in Python.

## Next Phase

Do not edit the baseline scripts directly for experiments.

Create a separate experiment layer for class imbalance, for example:

```text
code/python_pipeline/experiments
```

Recommended first experiments:

1. Threshold tuning with Risk recall constraints.
2. Class-weighted XGBoost.
3. NoRisk undersampling inside each train split only.
4. Probability calibration on validation only.
5. Evaluation using balanced accuracy, Risk F1, PR-AUC, and confusion matrix.

