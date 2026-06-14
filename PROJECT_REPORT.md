# Fair Content Ranking System - Project Report

## Problem

Most recommender demos optimize for immediate engagement. That creates a second problem: popular items keep receiving impressions, while uncertain or niche items do not get enough exposure to prove whether they are useful. This project models that platform-side ranking problem.

The goal is not to replace a personalized recommender. The goal is to decide which underexposed content deserves controlled exploration traffic while keeping quality and measurement risk visible.

## System Position

This repository is System B. It is designed to sit after a recommender system such as System A.

- System A ranks content for a reader.
- System B audits the candidate pool and decides where exploration traffic should go.
- The systems stay in separate repositories. System B imports System A artifacts through `scripts/import_system_a_artifacts.py`.

## Methods

### 1. Exposure Simulation

The project builds a logged exposure table with known propensities. This is required for off-policy evaluation. Each row contains impression, click, completion, return, treatment, reward, and logging propensity.

Why it matters: without logged propensities, IPS-style evaluation is not valid.

### 2. Bayesian Shrinkage

Raw CTR or completion rate is unreliable for low-impression items. The project uses Beta-Binomial shrinkage so small-sample items move toward a genre-level prior while higher-sample items rely more on observed behavior.

Why it matters: it prevents a tiny-sample item from becoming top-ranked only because it had a few lucky early outcomes.

### 3. Breakout Forecasting

A supervised model predicts which items are likely to become high-performing after more exposure. The feature builder separates early-window features from future-window labels to avoid label leakage.

Why it matters: it tests whether the platform can find future upside, not only explain past popularity.

### 4. Uplift Scoring

A T-learner estimates whether extra exploration exposure is likely to improve reward. This separates generally good items from items that specifically benefit from more exposure.

Why it matters: promotion traffic is limited, so it should go to items with expected incremental value.

### 5. Uncertainty-Aware Promotion

The final promotion score combines shrunk quality, breakout probability, uplift, and uncertainty while enforcing a relevance floor.

Why it matters: exploration should not become random traffic allocation. It should be uncertain but still plausibly relevant.

### 6. Bandit Policy Comparison

The project compares popularity, epsilon-greedy, UCB1, and Thompson Sampling on cumulative reward, regret, and exploration breadth.

Why it matters: it shows the tradeoff between exploitation and discovery.

### 7. Fairness and Concentration Metrics

The project computes creator exposure Gini, HHI, active creators, long-tail viability, and a relevance-vs-fairness Pareto frontier.

Why it matters: a platform ranking system should be judged not only by reward, but also by whether exposure collapses into a small set of creators.

### 8. Offline Policy Evaluation

The project reports IPS, clipped IPS, SNIPS, and doubly robust estimates under policy-distance stress tests.

Why it matters: offline policy evaluation becomes unstable when the target policy is too far from the logging policy. The dashboard exposes this instead of hiding it.

## Current Evidence

Current generated artifacts are stored in `data/processed/system_b/`. The report is generated with:

```powershell
python scripts/final_system_b_report.py
```

The dashboard is launched with:

```powershell
streamlit run dashboards/system_b_demo/app.py
```

The most important evidence to inspect is:

- `promotion_scores.parquet`: final item-level ranking inputs and promotion score.
- `ablation_comparison.parquet`: comparison of popularity-only, shrinkage-only, breakout-only, uplift-only, and full promotion scoring.
- `bandit_policy_metrics.parquet`: cumulative reward, regret, and exploration breadth.
- `fairness_metrics.parquet`: exposure concentration over time.
- `ips_stress_test.parquet`: off-policy estimate stability.

## What This Project Proves

It shows a full offline workflow for opportunity-aware content ranking:

1. build logged exposure data,
2. reduce small-sample noise,
3. predict breakout candidates,
4. estimate exposure uplift,
5. compare exploration policies,
6. audit fairness and concentration,
7. stress-test off-policy estimates.

## What It Does Not Prove

This is not production causal evidence. The exposure log is simulated. The uplift model is a design demonstration, not a real randomized experiment. The final policy would need live A/B testing or a randomized exploration bucket before any production claim.

## Limitations

- Exposure data is simulated.
- User outcomes are generated from controlled assumptions.
- IPS is valid only when logging propensities are known and policy overlap is sufficient.
- Uplift estimates are not causal proof without randomized or quasi-random treatment assignment.
- Real-world deployment would need guardrails for creator spam, content safety, cold-start abuse, and repeated exposure fatigue.

## Next Improvements

The highest-value next step is not adding more models. It is replacing the simulated exposure log with real logged impressions and known propensities. After that, the project can support stronger causal claims.
