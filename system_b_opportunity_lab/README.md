# System B - Opportunity Lab

This module is the core of the fair content ranking project.

It handles a common platform problem: popular items keep getting data, while
newer or niche items stay untested. System B gives underexposed items a measured
test without sending random traffic to low-quality content.

## What It Does

- Builds simulated exposure logs with known propensities.
- Shrinks noisy item-quality rates.
- Predicts possible breakout items.
- Estimates uplift from extra exposure.
- Builds a promotion score with a relevance floor.
- Compares bandit policies.
- Measures creator exposure concentration.
- Runs IPS, SNIPS, clipped IPS, and doubly robust checks.

## Run

```powershell
python scripts/run_system_b_pipeline.py
python scripts/final_system_b_report.py
streamlit run dashboards/system_b_demo/app.py
```

Outputs:

```text
data/processed/system_b/
reports/system_b_final_report.md
```

## Main Folders

```text
exposure_simulation/
  Builds exposure logs.

bayesian_shrinkage/
  Reduces noise in small samples.

breakout_forecasting/
  Finds items with possible future upside.

uplift_scoring/
  Estimates benefit from extra exposure.

uncertainty_promotion/
  Builds the promotion score.

bandit_exploration/
  Compares exploration policies.

fairness/
  Measures exposure concentration.

offline_eval/
  Runs off-policy checks.
```

## Limits

- The exposure log is simulated.
- Uplift is not causal proof.
- IPS needs known propensities and enough policy overlap.
- A real rollout would need randomized exploration traffic.
