# Fair Content Ranking System

This project is System B: a ranking lab for underexposed content.

Think of a content platform with thousands of stories. Popular stories keep
getting shown because the platform already has data for them. New or niche
stories may be good, but they never get enough impressions to prove it.

This repo tests a simple question:

```text
Which underexposed items deserve measured exploration traffic?
```

Related project: System A is kept in a separate repository.

## What This Project Does

- Builds a logged exposure table with known propensities.
- Shrinks noisy item-quality rates with a Beta-Binomial model.
- Predicts breakout candidates from early exposure features.
- Estimates uplift from extra exposure.
- Builds a promotion score with quality, uplift, uncertainty, and relevance.
- Compares bandit policies such as epsilon-greedy, UCB1, and Thompson sampling.
- Measures creator exposure concentration with Gini and HHI.
- Runs IPS, SNIPS, clipped IPS, and doubly robust checks.
- Shows the outputs in a Streamlit dashboard.

## The Main Idea

Raw popularity is a bad guide for discovery.

Imagine two stories:

- Story A has 50,000 impressions and a stable completion rate.
- Story B has 20 impressions and 8 completions.

Story B may be promising, but the sample is tiny. Ranking it too high would be
risky. Ignoring it forever would also be wrong. This project gives that kind of
item a measured test instead of guessing.

## How The Pipeline Works

```text
1. Exposure log
   Creates impressions, rewards, treatment flags, and logging propensities.

2. Quality shrinkage
   Pulls tiny-sample rates toward a prior so lucky early results do not dominate.

3. Breakout model
   Predicts whether an item may perform better after more exposure.

4. Uplift model
   Estimates whether extra exposure is likely to improve reward.

5. Promotion policy
   Combines quality, uplift, uncertainty, and a relevance floor.

6. Policy checks
   Compares reward, regret, exploration breadth, exposure concentration, and
   off-policy estimate stability.
```

## Run

```powershell
pip install -r requirements.txt
python scripts/run_system_b_pipeline.py
python scripts/final_system_b_report.py
streamlit run dashboards/system_b_demo/app.py
```

Generated files are written to:

```text
data/processed/system_b/
reports/system_b_final_report.md
```

## Dashboard

```powershell
streamlit run dashboards/system_b_demo/app.py
```

The dashboard shows:

- top promotion candidates,
- score ablation,
- policy reward and regret,
- exploration breadth,
- creator concentration,
- IPS stress-test results,
- current limits.

## Important Files

```text
system_b_opportunity_lab/exposure_simulation/
  Builds exposure logs with propensities.

system_b_opportunity_lab/bayesian_shrinkage/
  Reduces noise in low-sample item quality.

system_b_opportunity_lab/breakout_forecasting/
  Predicts future upside from early item signals.

system_b_opportunity_lab/uplift_scoring/
  Estimates incremental reward from exposure.

system_b_opportunity_lab/uncertainty_promotion/
  Builds the final promotion score.

system_b_opportunity_lab/bandit_exploration/
  Compares exploration policies.

system_b_opportunity_lab/fairness/
  Measures exposure concentration.

system_b_opportunity_lab/offline_eval/
  Runs IPS, SNIPS, clipped IPS, and doubly robust checks.
```

## Limits

- The exposure log is simulated.
- The uplift score is not causal proof.
- IPS needs known propensities and enough overlap between policies.
- The project does not model spam, safety, fatigue, or creator gaming.
- A real launch would need randomized exploration traffic and an A/B test.
