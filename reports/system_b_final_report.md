# System B Final Report

## Scope
System B is a simulation-backed fair content ranking system. It tests whether underexposed items can be promoted with uncertainty, relevance, policy-risk, and creator concentration visible.

## Data
- Items scored: 3000
- Logged exposures: 135000
- Logging policy: popularity ranking with epsilon exploration and known propensities.
- Evidence type: simulated exposure log, not production traffic.

## Breakout Forecasting
- Model: lightgbm
- ROC-AUC: 0.7931
- Average precision: 0.2715

## Score Ablation
This table compares ranking variants on the same candidate pool. It is the fastest way to see whether the full policy changes the ranking beyond popularity.

| Variant | Mean Quality | Tail Share | Novelty | Unique Creators | Creator Gini |
|---|---:|---:|---:|---:|---:|
| breakout_only | 0.7460 | 0.188 | 0.456 | 211 | 0.131 |
| full_promotion_score | 0.7425 | 0.176 | 0.442 | 211 | 0.131 |
| quality_shrinkage_only | 0.6978 | 0.220 | 0.415 | 207 | 0.141 |
| uplift_only | 0.5956 | 0.308 | 0.524 | 216 | 0.119 |
| popularity_only | 0.5825 | 0.000 | 0.042 | 214 | 0.122 |

## Top Opportunity Items
- item_02821: promotion=0.4225, shrinkage=0.3829, breakout=0.9556, uplift=0.1596
- item_02949: promotion=0.4178, shrinkage=0.3214, breakout=0.8616, uplift=0.2642
- item_02527: promotion=0.4129, shrinkage=0.3230, breakout=0.8987, uplift=0.2055
- item_02216: promotion=0.4112, shrinkage=0.3230, breakout=0.8371, uplift=0.2605
- item_00282: promotion=0.4106, shrinkage=0.3081, breakout=0.9135, uplift=0.2102
- item_01350: promotion=0.4094, shrinkage=0.3230, breakout=0.9242, uplift=0.1854
- item_01469: promotion=0.4094, shrinkage=0.3230, breakout=0.8966, uplift=0.1934
- item_01244: promotion=0.4088, shrinkage=0.3148, breakout=0.9040, uplift=0.1969
- item_02169: promotion=0.4080, shrinkage=0.3342, breakout=0.9473, uplift=0.1617
- item_02348: promotion=0.4048, shrinkage=0.2965, breakout=0.9284, uplift=0.1977

## Bandit Policy Comparison
- epsilon_greedy: reward=10900.0, regret=836.87, unique_items=446
- popularity: reward=8661.0, regret=3098.64, unique_items=1
- ucb1: reward=9130.0, regret=2589.42, unique_items=500
- thompson: reward=10482.0, regret=1212.25, unique_items=500

## Fairness Snapshot
- popularity_epsilon_explore: Gini=0.3405, HHI=0.0020, active_creators=686

## Pareto Frontier Knee
- lambda_novelty=0.20, lambda_fairness=0.00, relevance=0.7452, Gini=0.1287, novelty=0.5168

## IPS Stress Test
- close_policy: IPS=0.1430, SNIPS=0.1427, DR=0.1388, p95_weight=1.66, ESS=121834.6
- moderate_policy: IPS=0.1504, SNIPS=0.1499, DR=0.1388, p95_weight=1.98, ESS=111778.9
- far_policy: IPS=0.1568, SNIPS=0.1562, DR=0.1388, p95_weight=2.38, ESS=97822.2

## Interpretation
- Bayesian shrinkage controls tiny-sample quality noise.
- Breakout prediction estimates future upside after early exposure.
- Uplift scoring asks whether extra exposure is expected to help, not only whether an item is already good.
- The full promotion score is useful only if it improves tail/creator exposure without collapsing quality.
- IPS estimates are most trustworthy when target policies remain close to the logging policy and effective sample size stays high.

## Limitations
- Exposure logs are simulated, not real production logs.
- Uplift estimates are simulation-backed and should not be treated as causal proof.
- IPS requires known logging propensities and sufficient overlap between logging and target policies.
- Real deployment would need randomized exploration buckets, content-quality guardrails, and A/B tests.
