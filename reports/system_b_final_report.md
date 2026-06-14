# System B Final Report

## Scope
System B ranks underexposed items for measured exploration traffic. It keeps quality, uncertainty, policy risk, and creator concentration visible.

## Data
- Items scored: 3000
- Logged exposures: 135000
- Logging policy: popularity ranking with epsilon exploration and known propensities.
- Data source: simulated exposure log.

## Breakout Forecasting
- Model: lightgbm
- ROC-AUC: 0.6814
- Average precision: 0.2422

## Score Ablation
This table compares ranking variants on the same candidate pool. It is the fastest way to see whether the full policy changes the ranking beyond popularity.

| Variant | Mean Quality | Tail Share | Novelty | Unique Creators | Creator Gini |
|---|---:|---:|---:|---:|---:|
| breakout_only | 0.3811 | 0.240 | 0.424 | 221 | 0.102 |
| full_promotion_score | 0.3781 | 0.240 | 0.421 | 218 | 0.110 |
| quality_shrinkage_only | 0.3518 | 0.220 | 0.462 | 228 | 0.080 |
| uplift_only | 0.3429 | 0.284 | 0.516 | 220 | 0.109 |
| popularity_only | 0.3315 | 0.000 | 0.040 | 222 | 0.099 |

## Top Opportunity Items
- item_01938: promotion=0.3907, shrinkage=0.1716, breakout=0.9079, uplift=0.2908
- item_04596: promotion=0.3805, shrinkage=0.1568, breakout=0.9368, uplift=0.2619
- item_00072: promotion=0.3754, shrinkage=0.1938, breakout=0.9341, uplift=0.1978
- item_03620: promotion=0.3710, shrinkage=0.1567, breakout=0.9455, uplift=0.2223
- item_00453: promotion=0.3693, shrinkage=0.1842, breakout=0.8733, uplift=0.2139
- item_04140: promotion=0.3690, shrinkage=0.1448, breakout=0.8751, uplift=0.2581
- item_00356: promotion=0.3660, shrinkage=0.2225, breakout=0.9359, uplift=0.1254
- item_01636: promotion=0.3656, shrinkage=0.1552, breakout=0.9359, uplift=0.2047
- item_04904: promotion=0.3541, shrinkage=0.1678, breakout=0.8220, uplift=0.2240
- item_02566: promotion=0.3534, shrinkage=0.1596, breakout=0.8922, uplift=0.1609

## Bandit Policy Comparison
- epsilon_greedy: reward=7655.0, regret=1250.54, unique_items=446
- popularity: reward=4842.0, regret=4137.34, unique_items=1
- ucb1: reward=4973.0, regret=4023.82, unique_items=500
- thompson: reward=5580.0, regret=3295.73, unique_items=500

## Fairness Snapshot
- popularity_epsilon_explore: Gini=0.3382, HHI=0.0016, active_creators=860

## Pareto Frontier Knee
- lambda_novelty=0.35, lambda_fairness=0.05, relevance=0.3675, Gini=0.0858, novelty=0.7415

## IPS Stress Test
- close_policy: IPS=0.0871, SNIPS=0.0871, DR=0.0839, p95_weight=1.50, ESS=130542.7
- moderate_policy: IPS=0.0923, SNIPS=0.0923, DR=0.0839, p95_weight=2.32, ESS=110873.6
- far_policy: IPS=0.0969, SNIPS=0.0968, DR=0.0839, p95_weight=3.03, ESS=89249.2

## Interpretation
- Bayesian shrinkage controls tiny-sample quality noise.
- Breakout prediction estimates future upside after early exposure.
- Uplift scoring asks whether extra exposure is expected to help, not only whether an item is already good.
- The full promotion score matters only if it improves tail and creator exposure without dropping quality.
- IPS estimates are most trustworthy when target policies remain close to the logging policy and effective sample size stays high.

## Limitations
- Exposure logs are simulated.
- Uplift estimates are not causal proof.
- IPS requires known logging propensities and sufficient overlap between logging and target policies.
- Real deployment would need randomized exploration buckets, content-quality guardrails, and A/B tests.
