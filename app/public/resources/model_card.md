# Model Card: NEW1 Earnings-Risk Screener

## Purpose

NEW1 is a binary screening model for flagging potential next-quarter earnings
risk among Vietnamese banking stocks.

## Prediction Target

```text
Risk / NoRisk
```

The current evaluation target is based on whether next-quarter net income shows
a material year-over-year decline.

## Model Summary

NEW1 is a two-member ensemble migrated from the original RapidMiner workflow:

```text
Member 1: 258-feature set
Member 2: 309-feature set
Ensemble probability = 0.5 * member_258 + 0.5 * member_309
Reference threshold = 0.437
```

The Python implementation uses XGBoost-style estimators to reproduce the
pipeline structure. It is not expected to be binary-identical to the original
RapidMiner/H2O workflow.

## How NEW1 Is Trained And Scored

NEW1 uses two feature views of the same bank-quarter data:

```text
Feature-set 258: narrower selected feature view
Feature-set 309: wider selected feature view
Union: 357 unique features
Overlap: 210 shared features
```

Both members are trained with the auxiliary Risk5 label so the model can see a
slightly broader set of earnings deterioration cases. The public evaluation and
web demo are still reported against the main Risk10 target.

Scoring flow:

```text
1. Score row with 258-feature member.
2. Score row with 309-feature member.
3. Average both Risk probabilities.
4. Predict Risk when ensemble probability >= 0.437.
```

The web app does not retrain the model. It only displays the saved NEW1 test
predictions from the Python baseline output.

## Public Baseline Metrics

```text
Accuracy:        80.77%
Risk precision: 43.90%
Risk recall:    45.00%
Macro-F1:       66.41%
Threshold:      0.437
```

Confusion matrix labels:

```text
[Risk, NoRisk]
```

Matrix:

```text
[[18, 22],
 [23, 171]]
```

## Limitations

- Dataset is small and based on bank-quarter observations.
- Risk class is less frequent than NoRisk.
- Accuracy should not be interpreted alone.
- This model is a screening aid, not a buy/sell recommendation.
- Predictions should be reviewed with analyst judgment and financial context.
