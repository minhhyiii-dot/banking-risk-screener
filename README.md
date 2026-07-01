# Banking Risk Screener

Vietnamese Banking Earnings Risk Screener is a portfolio MVP for exploring a
machine-learning workflow that flags potential earnings-risk events among
Vietnamese banking stocks.

The project is based on a coursework research project and is being migrated from
RapidMiner workflows into a cleaner Python + static web demo stack.

> This project is an educational decision-support demo. It is not a buy, sell,
> or hold recommendation.

## MVP Goal

The intended public product is a static web demo deployed with Cloudflare Pages.
The demo will show:

```text
1. Overview
   What the project does and what Risk / NoRisk means.

2. Screener
   A sample prediction table with filters for ticker, quarter, and prediction.

3. Model
   Baseline model metrics, threshold, and confusion matrix.

4. Limitations
   Dataset limits, class imbalance, and analyst-review caveats.
```

The UI direction is a clean dashboard-style web app with desktop and mobile
layouts: top navigation, metric cards, a filterable screener table, model result
cards, and a clear limitations section.

## Current Status

```text
Repository setup:        Done
Python baseline:         Done
GitHub source:           Done
Cloudflare app:          Planned
NotebookLM/notebooklm-py: Pending
```

Current priority: keep the Python baseline reproducible and prepare a small
public-facing web demo. Model redesign, new data collection, and retraining are
out of scope for the current deployment phase.

## Repository Structure

```text
banking-risk-screener/
  code/
    Models/                    Legacy RapidMiner workflows and model inputs
    Notebooks/                 Original EDA and data-build notebooks
    python_migration_specs/    Extracted specs from RapidMiner workflows
    python_pipeline/           Reproducible Python baseline

  data/
    Raw Data/                  Original raw input files
    old master dataset/        Archived Growth/Safe/Risky dataset
    new master dataset/        Current Risk/NoRisk dataset family

  outputs/
    python_baseline/           Metrics, feature lists, and predictions

  docs/
    Project notes, workflow notes, and future NotebookLM outputs

  README.md
```

Planned web/demo structure:

```text
banking-risk-screener/
  app/                         Frontend deployed to Cloudflare Pages
  data/
    sample/                    Small public demo data
    processed/                 JSON/CSV files prepared for the app
  model/
    model_card.md              Model summary and caveats
    metrics.json               Public model metrics
    predictions_sample.csv     Small prediction sample for the screener
  docs/
    notebooklm_outputs/        NotebookLM-generated summaries and FAQ
```

## Modeling Summary

The current project focuses on a binary earnings-risk screening task:

```text
Risk / NoRisk
```

The target is based on whether next-quarter net income shows a material
year-over-year decline. The Python baseline approximates the original
RapidMiner/H2O workflows using Python and XGBoost-style models.

Important note: the Python implementation is a reproducible migration layer. It
is not expected to produce binary-identical predictions to the original
RapidMiner/H2O model.

## Baseline Metrics

Current Python baseline metrics:

| Model | Split | Accuracy | Risk Recall | Macro-F1 |
|---|---:|---:|---:|---:|
| OLD1 Decision Tree | test | 36.06% | Archived 3-class task | - |
| OLD2 Random Forest | test | 43.75% | Archived 3-class task | - |
| OLD3 Gradient Boosted Trees | test | 38.94% | Archived 3-class task | - |
| NEW1 Ensemble | test | 80.77% | 45.00% | 66.41% |
| NEW2 Prequential Ensemble | validation | 75.00% | 47.37% | 65.05% |
| NEW2 Prequential Ensemble | test | 81.62% | 52.50% | 69.09% |

For the public demo, NEW1 is the simplest model story:

```text
Model: NEW1
Threshold: 0.437
Task: Risk / NoRisk earnings-risk screening
```

## Run The Python Baseline

Install dependencies:

```bash
pip install -r code/python_pipeline/requirements.txt
```

Run all baselines:

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

## Deployment Plan

The planned delivery flow is:

```text
Codex / Antigravity-style build flow
-> GitHub repository
-> Cloudflare Pages public demo
-> Wrangler deployment check
```

Cloudflare deployment will be added after the frontend app is created.

Expected command later:

```bash
npm run build
npx wrangler pages deploy dist --project-name banking-risk-screener
```

## NotebookLM Plan

NotebookLM / notebooklm-py is planned for the knowledge/report workflow, not for
model training.

Expected outputs:

```text
docs/notebooklm_outputs/project_summary.md
docs/notebooklm_outputs/faq.md
docs/notebooklm_outputs/limitations.md
```

These files will summarize the report, model limitations, and stakeholder FAQ
for use in the web demo and project documentation.

## Limitations

- The dataset is small and limited to bank-quarter observations.
- The Risk class is less frequent than NoRisk, so accuracy alone is not enough.
- The model should be interpreted as a screening aid, not an automated
  investment system.
- Predictions require analyst review and should be combined with financial
  context.
- Current results are from a Python migration of the original RapidMiner
  workflow, not a fully redesigned production model.

## Next Steps

```text
1. Create public sample data for the web demo.
2. Add model/ with model card, metrics, and prediction sample.
3. Generate NotebookLM outputs for report summary and FAQ.
4. Build the static Cloudflare Pages app.
5. Deploy with Wrangler and add the public demo link.
```
