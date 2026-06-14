# Fair Content Ranking System

A small platform-side ranking project for underexposed content discovery.

This repo is System B from the Narrative Intelligence portfolio. It is separate from the personalized recommender repo. System A answers: "what should this reader see?" System B answers: "which underexposed items deserve controlled exploration traffic, and can we evaluate that policy safely offline?"

## What It Builds

- Simulated exposure logs with known logging propensities.
- Bayesian quality shrinkage for low-sample items.
- Breakout prediction from early exposure signals.
- Uplift scoring for exploration value.
- Uncertainty-aware promotion ranking.
- Bandit policy comparison.
- Creator exposure fairness metrics.
- IPS/SNIPS/doubly robust policy stress tests.
- Streamlit dashboard for review/demo.

## Quick Start

```powershell
pip install -r requirements.txt
python scripts/run_system_b_pipeline.py
python scripts/final_system_b_report.py
streamlit run dashboards/system_b_demo/app.py
```

The dashboard uses the generated artifacts under:

```text
data/processed/system_b/
```

## Use With System A

Keep System A and System B as separate repositories. To import System A artifacts into this repo:

```powershell
python scripts/import_system_a_artifacts.py --system-a-path D:\Projects\narrative-intelligence-platform
python scripts/run_system_b_pipeline.py
python scripts/final_system_b_report.py
```

Required System A artifacts:

- `data/processed/item_fingerprints.parquet`
- `data/processed/quality_scores.parquet`
- `data/processed/session_features.parquet`

Optional:

- `data/processed/item_embeddings.parquet`
- `data/synthetic/catalog.parquet`

## Streamlit Cloud

Use this app entrypoint:

```text
dashboards/system_b_demo/app.py
```

The repo includes `.streamlit/config.toml` and sample processed artifacts, so the app can open without running training first.

## Reports

```powershell
python scripts/final_system_b_report.py
```

Main report files:

- `PROJECT_REPORT.md`: hand-written project explanation.
- `reports/system_b_final_report.md`: generated summary from current artifacts.

## Important Limitation

This project uses simulated exposure data. It demonstrates the offline ranking and policy-evaluation workflow, but it does not prove real production lift. Real deployment would need logged propensities from actual traffic, randomized exploration buckets, and A/B testing.
