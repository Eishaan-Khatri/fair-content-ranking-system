# System B - Opportunity Lab

System B is the platform-side layer. System A chooses candidate content for a
reader. System B decides which underexposed items should receive measured
exploration traffic and whether that policy can be evaluated safely offline.

## Why It Exists

Pure engagement ranking concentrates exposure. Popular creators keep getting
data, while uncertain items remain untested. Promoting the highest early CTR is
also unsafe because tiny samples can look artificially strong.

System B handles this with:

- Bayesian shrinkage for low-data quality estimates.
- Uplift scoring for likely benefit from extra exposure.
- Uncertainty-aware promotion with a relevance floor.
- Offline policy evaluation using logged propensities.

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

## Components

### Exposure Simulation

`exposure_simulation/simulation_harness.py`

Builds a synthetic exposure log from available item artifacts. Each row includes
a logging propensity for IPS and doubly robust evaluation.

### Bayesian Shrinkage

`bayesian_shrinkage/beta_binomial_shrinkage.py`

Shrinks low-sample completion estimates toward a genre prior.

### Breakout Forecasting

`breakout_forecasting/`

Builds early-window features and trains a classifier for future upside. Uses
LightGBM when available and sklearn otherwise.

### Uplift Scoring

`uplift_scoring/uplift_model.py`

Uses a T-learner to estimate incremental reward from exploration exposure.

### Promotion Policy

`uncertainty_promotion/promotion_policy.py`

Combines quality, breakout, uplift, and uncertainty while enforcing a relevance
floor.

### Bandit Exploration

`bandit_exploration/`

Compares popularity, epsilon-greedy, UCB1, and Thompson Sampling.

### Concentration Metrics

`fairness/`

Computes Gini, HHI, active creators, long-tail viability, and a
relevance-vs-concentration frontier.

### Offline Policy Evaluation

`offline_eval/`

Runs IPS, clipped IPS, SNIPS, and doubly robust estimates. The stress test shows
when estimates become unreliable because the target policy is too far from the
logging policy.

## Current Limits

- Exposure logs are simulated.
- Amazon/Gutenberg metadata can enrich items, but does not create real exposure outcomes.
- IPS is only valid with known propensities and enough policy overlap.
- Uplift estimates should be read as design evidence, not live causal proof.
