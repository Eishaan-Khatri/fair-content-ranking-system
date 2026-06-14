# Fair Content Ranking System

Offline ranking lab for giving underexposed content measured exploration traffic.

This is System B from the Narrative Intelligence work. It is separate from the
personalized recommender. System A asks what a reader should see. System B asks
which underexposed items are worth testing, how risky that test is, and whether
the policy can be evaluated from logged data.

## What Is Built

- Exposure-log simulator with known logging propensities.
- Bayesian quality shrinkage for low-sample items.
- Breakout prediction from early exposure signals.
- Uplift scoring for items that may benefit from more exposure.
- Promotion score with uncertainty and relevance checks.
- Bandit comparison for reward, regret, and exploration breadth.
- Creator exposure concentration metrics.
- IPS, SNIPS, clipped IPS, and doubly robust stress tests.
- Streamlit dashboard for reviewing the artifacts.

## Run

```powershell
pip install -r requirements.txt
python scripts/run_system_b_pipeline.py
python scripts/final_system_b_report.py
streamlit run dashboards/system_b_demo/app.py
```

Generated artifacts are written to:

```text
data/processed/system_b/
```

## Use With System A

System B can run alone from its sample artifacts. To import System A outputs:

```powershell
python scripts/import_system_a_artifacts.py --system-a-path D:\Projects\narrative-intelligence-platform
python scripts/run_system_b_pipeline.py
python scripts/final_system_b_report.py
```

Required System A files:

- `data/processed/item_fingerprints.parquet`
- `data/processed/quality_scores.parquet`
- `data/processed/session_features.parquet`

Optional files:

- `data/processed/item_embeddings.parquet`
- `data/synthetic/catalog.parquet`

## Dashboard

Streamlit entrypoint:

```text
dashboards/system_b_demo/app.py
```

The app reads the processed artifacts and shows:

- top underexposed candidates,
- policy comparison,
- creator exposure concentration,
- off-policy estimate stability,
- current limitations.

## Reports

```powershell
python scripts/final_system_b_report.py
```

Main report files:

- `PROJECT_REPORT.md`: project explanation.
- `reports/system_b_final_report.md`: generated report from current artifacts.

## Limit

The exposure data is simulated. This project shows the offline ranking and
evaluation workflow, but it does not prove production lift. A real deployment
would need logged propensities from traffic, randomized exploration buckets, and
an A/B test.
