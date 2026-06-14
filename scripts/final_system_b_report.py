"""Write a markdown summary report for System B."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SYSTEM_B_DIR = PROJECT_ROOT / "data" / "processed" / "system_b"
REPORT_DIR = PROJECT_ROOT / "reports"


def _read(path: Path) -> pd.DataFrame:
    return pd.read_parquet(path) if path.exists() else pd.DataFrame()


def _fmt(value: object, digits: int = 4) -> str:
    return f"{float(value):.{digits}f}" if isinstance(value, (float, int)) else "n/a"


def main() -> int:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    summary_path = SYSTEM_B_DIR / "system_b_pipeline_summary.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8")) if summary_path.exists() else {}
    predictions = _read(SYSTEM_B_DIR / "promotion_scores.parquet")
    bandit = _read(SYSTEM_B_DIR / "bandit_policy_metrics.parquet")
    fairness = _read(SYSTEM_B_DIR / "fairness_metrics.parquet")
    frontier = _read(SYSTEM_B_DIR / "pareto_frontier.parquet")
    ips = _read(SYSTEM_B_DIR / "ips_stress_test.parquet")
    ablation = _read(SYSTEM_B_DIR / "ablation_comparison.parquet")
    exposure = _read(SYSTEM_B_DIR / "exposure_log.parquet")

    top = predictions.sort_values("promotion_score", ascending=False).head(10) if not predictions.empty else pd.DataFrame()
    bandit_final = bandit.sort_values("round").groupby("policy").tail(1) if not bandit.empty else pd.DataFrame()
    fairness_last = fairness.sort_values("day").groupby("policy").tail(1) if not fairness.empty else pd.DataFrame()
    knee = frontier.head(1) if not frontier.empty else pd.DataFrame()

    lines = [
        "# System B Final Report",
        "",
        "## Scope",
        "System B is a simulation-backed fair content ranking system. It tests whether underexposed items can be promoted with uncertainty, relevance, policy-risk, and creator concentration visible.",
        "",
        "## Data",
        f"- Items scored: {summary.get('n_items', len(predictions) if not predictions.empty else 'n/a')}",
        f"- Logged exposures: {summary.get('n_exposures', len(exposure) if not exposure.empty else 'n/a')}",
        "- Logging policy: popularity ranking with epsilon exploration and known propensities.",
        "- Evidence type: simulated exposure log, not production traffic.",
        "",
        "## Breakout Forecasting",
    ]
    metrics = summary.get("breakout_metrics", {})
    lines.extend(
        [
            f"- Model: {metrics.get('model', 'n/a')}",
            f"- ROC-AUC: {_fmt(metrics.get('roc_auc'))}",
            f"- Average precision: {_fmt(metrics.get('average_precision'))}",
            "",
            "## Score Ablation",
            "This table compares ranking variants on the same candidate pool. It is the fastest way to see whether the full policy changes the ranking beyond popularity.",
        ]
    )
    if not ablation.empty:
        lines.append("")
        lines.append("| Variant | Mean Quality | Tail Share | Novelty | Unique Creators | Creator Gini |")
        lines.append("|---|---:|---:|---:|---:|---:|")
        for row in ablation.itertuples(index=False):
            lines.append(
                f"| {row.variant} | {row.mean_true_quality:.4f} | {row.tail_item_share:.3f} | {row.mean_novelty:.3f} | {row.unique_creators} | {row.creator_gini:.3f} |"
            )
    else:
        lines.append("- No ablation artifact found. Run `python scripts/run_system_b_pipeline.py`.")

    lines.extend(["", "## Top Opportunity Items"])
    if not top.empty:
        for row in top.itertuples(index=False):
            lines.append(
                f"- {row.item_id}: promotion={row.promotion_score:.4f}, shrinkage={row.shrunk_mean:.4f}, breakout={row.breakout_score:.4f}, uplift={row.uplift_score:.4f}"
            )
    else:
        lines.append("- No opportunity rows found.")

    lines.extend(["", "## Bandit Policy Comparison"])
    if not bandit_final.empty:
        for row in bandit_final.itertuples(index=False):
            lines.append(
                f"- {row.policy}: reward={row.cumulative_reward:.1f}, regret={row.cumulative_regret:.2f}, unique_items={row.unique_items_exposed}"
            )
    else:
        lines.append("- No bandit artifact found.")

    lines.extend(["", "## Fairness Snapshot"])
    if not fairness_last.empty:
        for row in fairness_last.itertuples(index=False):
            lines.append(f"- {row.policy}: Gini={row.gini:.4f}, HHI={row.hhi:.4f}, active_creators={row.active_creators}")
    else:
        lines.append("- No fairness artifact found.")

    lines.extend(["", "## Pareto Frontier Knee"])
    if not knee.empty:
        row = knee.iloc[0]
        lines.append(
            f"- lambda_novelty={row['lambda_novelty']:.2f}, lambda_fairness={row['lambda_fairness']:.2f}, relevance={row['mean_relevance']:.4f}, Gini={row['gini']:.4f}, novelty={row['mean_novelty']:.4f}"
        )
    else:
        lines.append("- No Pareto frontier artifact found.")

    lines.extend(["", "## IPS Stress Test"])
    if not ips.empty:
        for row in ips.itertuples(index=False):
            lines.append(
                f"- {row.target_policy}: IPS={row.ips:.4f}, SNIPS={row.snips:.4f}, DR={row.doubly_robust:.4f}, p95_weight={row.p95_weight:.2f}, ESS={row.effective_sample_size:.1f}"
            )
    else:
        lines.append("- No IPS stress-test artifact found.")

    lines.extend(
        [
            "",
            "## Interpretation",
            "- Bayesian shrinkage controls tiny-sample quality noise.",
            "- Breakout prediction estimates future upside after early exposure.",
            "- Uplift scoring asks whether extra exposure is expected to help, not only whether an item is already good.",
            "- The full promotion score is useful only if it improves tail/creator exposure without collapsing quality.",
            "- IPS estimates are most trustworthy when target policies remain close to the logging policy and effective sample size stays high.",
            "",
            "## Limitations",
            "- Exposure logs are simulated, not real production logs.",
            "- Uplift estimates are simulation-backed and should not be treated as causal proof.",
            "- IPS requires known logging propensities and sufficient overlap between logging and target policies.",
            "- Real deployment would need randomized exploration buckets, content-quality guardrails, and A/B tests.",
        ]
    )

    out_path = REPORT_DIR / "system_b_final_report.md"
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[OK] Wrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
