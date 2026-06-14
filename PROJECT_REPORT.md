# Fair Content Ranking System - Project Report

## Problem

Most recommendation systems learn fastest from items that already get traffic.
That creates a loop. Popular items get more impressions, so the platform gets
more data about them. New or niche items get fewer impressions, so the platform
stays unsure about them.

This project works on that second problem. It asks which underexposed items
should get a small, measured amount of traffic so the platform can learn more
about them.

## Where This Fits

This repo is System B. System A is a separate companion project.

## Method

### 1. Exposure Log

The pipeline creates a table of impressions, clicks, completions, returns,
treatments, rewards, and logging propensities.

The propensity column matters. It tells us how likely the old logging policy was
to show an item. Without that, IPS-style checks are not reliable.

### 2. Bayesian Shrinkage

Raw rates are noisy when an item has only a few impressions. A story with 2
completions from 3 impressions looks strong, but there is not enough data yet.

The Beta-Binomial shrinkage step pulls tiny-sample rates toward a genre prior.
Large-sample items stay closer to their observed rate.

### 3. Breakout Model

The breakout model looks at early item signals and predicts which items may do
well after more exposure. The features come from the early window. The label
comes from a later window, so the model is not allowed to peek at the answer.

### 4. Uplift Model

The uplift model estimates whether extra exposure is likely to improve reward.
That is different from asking whether an item is already good.

A good item may not need help. A promising underexposed item might.

### 5. Promotion Score

The final score combines:

- shrunk quality,
- breakout probability,
- uplift,
- uncertainty,
- a minimum relevance check.

The score is meant to pick candidates for measured exploration, not to replace
the whole recommender.

### 6. Bandit Policies

The project compares popularity, epsilon-greedy, UCB1, and Thompson Sampling.
It tracks reward, regret, and how many different items receive exposure.

### 7. Exposure Concentration

The project measures whether exposure collapses into a small set of creators.
It uses Gini, HHI, active creator count, long-tail viability, and a
relevance-vs-concentration frontier.

### 8. Off-Policy Checks

The project runs IPS, clipped IPS, SNIPS, and doubly robust checks. These checks
get weaker when the target policy is too different from the policy that created
the log.

## Files To Inspect

```text
data/processed/system_b/promotion_scores.parquet
data/processed/system_b/ablation_comparison.parquet
data/processed/system_b/bandit_policy_metrics.parquet
data/processed/system_b/fairness_metrics.parquet
data/processed/system_b/ips_stress_test.parquet
reports/system_b_final_report.md
```

## Run

```powershell
python scripts/run_system_b_pipeline.py
python scripts/final_system_b_report.py
streamlit run dashboards/system_b_demo/app.py
```

## What This Shows

The repo shows a complete offline workflow for exploration ranking:

1. create logged exposure data,
2. reduce tiny-sample noise,
3. find possible breakout items,
4. estimate exposure uplift,
5. compare exploration policies,
6. check exposure concentration,
7. test off-policy estimate stability.

## Limits

- The exposure log is simulated.
- Uplift is not causal proof.
- IPS needs known propensities and enough policy overlap.
- The project does not model spam, safety, repeated-exposure fatigue, or creator gaming.
- A real launch would need randomized exploration traffic and an A/B test.

The next serious step is to replace the simulated exposure log with real
impression logs that include propensities.
