# Fair Content Ranking System - Project Report

## Problem

Standard recommendation demos usually optimize for immediate engagement. That
creates a measurement problem. Popular items keep getting impressions, while
uncertain niche items do not receive enough traffic to prove whether they are
good.

This project models that platform-side decision. It does not replace a personal
recommender. It decides which underexposed items should get controlled
exploration traffic while keeping quality, uncertainty, and policy risk visible.

## Position In The Portfolio

This repository is System B.

- System A retrieves and ranks content for a reader.
- System B audits the candidate pool and allocates exploration traffic.
- System B can import System A artifacts through `scripts/import_system_a_artifacts.py`.

## Methods

### 1. Exposure Simulation

The project creates a logged exposure table with known propensities. Each row
contains an impression, click, completion, return signal, treatment flag,
reward, and logging propensity.

This matters because IPS-style evaluation is not valid without known logging
propensities.

### 2. Bayesian Shrinkage

Raw CTR or completion rate is noisy for low-impression items. The project uses
Beta-Binomial shrinkage so small-sample items move toward a genre prior while
mature items rely more on observed behavior.

This prevents a tiny-sample item from ranking highly only because of a few lucky
early outcomes.

### 3. Breakout Forecasting

A supervised model predicts which items may perform well after more exposure.
Feature generation separates early-window features from future-window labels to
avoid leakage.

This tests future upside instead of only explaining existing popularity.

### 4. Uplift Scoring

A T-learner estimates whether extra exposure is likely to increase reward. This
separates generally good items from items that specifically benefit from
promotion traffic.

### 5. Uncertainty-Aware Promotion

The final score combines shrunk quality, breakout probability, uplift, and
uncertainty while enforcing a relevance floor.

Exploration should be uncertain, but not random.

### 6. Bandit Policy Comparison

The project compares popularity, epsilon-greedy, UCB1, and Thompson Sampling on
cumulative reward, regret, and number of unique items exposed.

### 7. Concentration Metrics

The project computes creator exposure Gini, HHI, active creators, long-tail
viability, and a relevance-vs-concentration frontier.

Reward alone is not enough. The system also checks whether exposure collapses
into a small creator set.

### 8. Offline Policy Evaluation

The project reports IPS, clipped IPS, SNIPS, and doubly robust estimates under
policy-distance stress tests.

These estimates become unstable when the target policy moves too far from the
logging policy. The dashboard exposes that risk.

## Current Evidence

Artifacts are stored under:

```text
data/processed/system_b/
```

Generate the report with:

```powershell
python scripts/final_system_b_report.py
```

Launch the dashboard with:

```powershell
streamlit run dashboards/system_b_demo/app.py
```

Files worth checking:

- `promotion_scores.parquet`
- `ablation_comparison.parquet`
- `bandit_policy_metrics.parquet`
- `fairness_metrics.parquet`
- `ips_stress_test.parquet`

## What It Shows

The repo demonstrates a complete offline workflow:

1. build logged exposure data,
2. reduce small-sample noise,
3. predict breakout candidates,
4. estimate exposure uplift,
5. compare exploration policies,
6. audit exposure concentration,
7. stress-test off-policy estimates.

## What It Does Not Show

This is not production causal evidence. The exposure log is simulated. The
uplift model is a design test, not a randomized experiment. Any production claim
would need real logged propensities, randomized exploration, and A/B testing.

## Limits

- Exposure data is simulated.
- User outcomes come from controlled assumptions.
- IPS needs known propensities and enough policy overlap.
- Uplift estimates are not causal proof without randomized treatment assignment.
- A real system would need safety, spam, abuse, fatigue, and repeated-exposure guardrails.

## Next Work

The strongest next step is not adding more model types. It is replacing the
simulated exposure log with real impressions and known propensities. That is the
change that would make stronger causal claims possible.
