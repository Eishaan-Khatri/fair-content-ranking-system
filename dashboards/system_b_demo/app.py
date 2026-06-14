"""Streamlit dashboard for the Fair Content Ranking System.

Run with:
    streamlit run dashboards/system_b_demo/app.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
SYSTEM_B_DIR = PROJECT_ROOT / "data" / "processed" / "system_b"
REPORT_PATH = PROJECT_ROOT / "reports" / "system_b_final_report.md"

try:
    import plotly.express as px
    import plotly.graph_objects as go
    import streamlit as st
except ImportError:
    print("Install dashboard dependencies: pip install streamlit plotly")
    sys.exit(1)


st.set_page_config(
    page_title="Fair Content Ranking System",
    page_icon="FCR",
    layout="wide",
    initial_sidebar_state="expanded",
)

COLORWAY = ["#2563eb", "#059669", "#d97706", "#7c3aed", "#dc2626", "#0891b2"]

st.markdown(
    """
<style>
    .stApp { background: #f8fafc; color: #111827; }
    .block-container { max-width: 1280px; padding-top: 1.4rem; padding-bottom: 2.5rem; }
    [data-testid="stSidebar"] { background: #ffffff; border-right: 1px solid #e5e7eb; }
    h1, h2, h3, h4, p, li, label, .stMarkdown, [data-testid="stMetricLabel"] { color: #111827; }
    .hero {
        background: #ffffff;
        border: 1px solid #dbe3ef;
        border-radius: 8px;
        padding: 18px 20px;
        margin-bottom: 16px;
    }
    .hero h1 { margin: 0 0 6px 0; font-size: 2rem; line-height: 1.15; }
    .hero p { margin: 0; color: #4b5563; max-width: 920px; }
    .section-note {
        background: #eef6ff;
        border-left: 4px solid #2563eb;
        padding: 12px 14px;
        border-radius: 6px;
        color: #1f2937;
        margin: 10px 0 16px 0;
    }
    .warning-note {
        background: #fff7ed;
        border-left: 4px solid #d97706;
        padding: 12px 14px;
        border-radius: 6px;
        color: #7c2d12;
        margin: 10px 0 16px 0;
    }
    .method-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
        gap: 10px;
        margin: 12px 0 18px 0;
    }
    .method-card {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 13px 14px;
    }
    .method-card b { display: block; margin-bottom: 4px; color: #111827; }
    .method-card span { color: #4b5563; font-size: 0.94rem; }
    .term {
        border-bottom: 1px dotted #2563eb;
        color: #1d4ed8;
        cursor: help;
        font-weight: 650;
    }
    div[data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 12px 14px;
    }
    div[data-testid="stMetricValue"] { color: #111827; }
    .small-muted { color: #6b7280; font-size: 0.9rem; }
    .footer-note {
        border-top: 1px solid #e5e7eb;
        padding-top: 14px;
        color: #4b5563;
        font-size: 0.92rem;
        margin-top: 24px;
    }
</style>
""",
    unsafe_allow_html=True,
)


@st.cache_data(show_spinner=False)
def load_parquet(name: str) -> pd.DataFrame:
    path = SYSTEM_B_DIR / name
    if not path.exists():
        return pd.DataFrame()
    return pd.read_parquet(path)


@st.cache_data(show_spinner=False)
def load_summary() -> dict:
    path = SYSTEM_B_DIR / "system_b_pipeline_summary.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def term(label: str, definition: str) -> str:
    safe_definition = definition.replace('"', "'")
    return f'<span class="term" title="{safe_definition}">{label}</span>'


def metric_value(df: pd.DataFrame, column: str, default: float = 0.0) -> float:
    if df.empty or column not in df.columns:
        return default
    return float(df[column].dropna().iloc[-1]) if not df[column].dropna().empty else default


def final_by_policy(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty or "policy" not in df.columns:
        return pd.DataFrame()
    sort_col = "round" if "round" in df.columns else "day"
    return df.sort_values(sort_col).groupby("policy", as_index=False).tail(1).reset_index(drop=True)


def configure_fig(fig: go.Figure) -> go.Figure:
    fig.update_layout(
        colorway=COLORWAY,
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        font={"color": "#111827"},
        margin={"l": 20, "r": 20, "t": 52, "b": 35},
        legend_title_text="",
    )
    fig.update_xaxes(gridcolor="#e5e7eb", zerolinecolor="#e5e7eb")
    fig.update_yaxes(gridcolor="#e5e7eb", zerolinecolor="#e5e7eb")
    return fig


summary = load_summary()
promotion = load_parquet("promotion_scores.parquet")
ablation = load_parquet("ablation_comparison.parquet")
bandit = load_parquet("bandit_policy_metrics.parquet")
fairness = load_parquet("fairness_metrics.parquet")
frontier = load_parquet("pareto_frontier.parquet")
ips = load_parquet("ips_stress_test.parquet")
exposure = load_parquet("exposure_log.parquet")
item_universe = load_parquet("item_universe.parquet")

with st.sidebar:
    st.title("Fair Ranking")
    section = st.radio(
        "View",
        [
            "Overview",
            "Methods",
            "Opportunity Explorer",
            "Policy Comparison",
            "Fairness",
            "IPS Stress Test",
            "Limitations",
        ],
    )
    st.caption("Standalone System B demo")
    st.divider()
    st.caption("Run pipeline")
    st.code("python scripts/run_system_b_pipeline.py", language="powershell")

st.markdown(
    """
<div class="hero">
  <h1>Fair Content Ranking System</h1>
  <p>A compact platform-side ranking demo for finding underexposed content, comparing exploration policies, and checking whether exposure becomes too concentrated.</p>
</div>
""",
    unsafe_allow_html=True,
)

if promotion.empty:
    st.error("System B artifacts not found. Run: python scripts/run_system_b_pipeline.py")
    st.stop()

if section == "Overview":
    st.markdown(
        f"""
<div class="section-note">
This project studies the ranking problem after a recommender has produced candidates: which items should receive controlled exploration traffic? It uses {term('Bayesian shrinkage', 'Pulls low-sample item rates toward a prior so noisy early results do not dominate.')}, {term('uplift scoring', 'Estimates whether extra exposure is expected to increase reward.')}, bandit comparisons, and offline policy checks.
</div>
""",
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Items scored", f"{len(promotion):,}")
    c2.metric("Exposure rows", f"{len(exposure):,}" if not exposure.empty else f"{summary.get('n_exposures', 0):,}")
    c3.metric("Creators", f"{promotion['creator_id'].nunique():,}" if "creator_id" in promotion else "0")
    c4.metric("Top promotion", f"{promotion['promotion_score'].max():.3f}")

    left, right = st.columns([1.15, 0.85])
    with left:
        top = promotion.sort_values("promotion_score", ascending=False).head(20)
        fig = px.bar(
            top.sort_values("promotion_score"),
            x="promotion_score",
            y="item_id",
            orientation="h",
            color="primary_genre" if "primary_genre" in top.columns else None,
            title="Top promotion candidates",
            hover_data=[c for c in ["title", "creator_id", "shrunk_mean", "breakout_score", "uplift_score"] if c in top.columns],
        )
        st.plotly_chart(configure_fig(fig), use_container_width=True)
    with right:
        metrics = summary.get("breakout_metrics", {})
        st.subheader("Model snapshot")
        st.metric("Breakout ROC-AUC", f"{metrics.get('roc_auc', 0):.3f}" if isinstance(metrics.get("roc_auc"), (int, float)) else "n/a")
        st.metric("Average precision", f"{metrics.get('average_precision', 0):.3f}" if isinstance(metrics.get("average_precision"), (int, float)) else "n/a")
        st.markdown(
            """
<div class="warning-note">
These are simulation-backed metrics. They show whether the offline workflow is coherent; they are not production impact numbers.
</div>
""",
            unsafe_allow_html=True,
        )

    st.subheader("Score ablation")
    if not ablation.empty:
        show = ablation[[
            "variant",
            "mean_true_quality",
            "tail_item_share",
            "mean_novelty",
            "unique_creators",
            "creator_gini",
        ]].copy()
        st.dataframe(show, use_container_width=True, hide_index=True)
    else:
        st.warning("Ablation artifact missing. Re-run the pipeline to generate ablation_comparison.parquet.")

elif section == "Methods":
    st.markdown(
        """
<div class="method-grid">
  <div class="method-card"><b>Exposure log</b><span>Creates impressions, rewards, treatment flags, and logging propensities for offline policy testing.</span></div>
  <div class="method-card"><b>Bayesian shrinkage</b><span>Reduces tiny-sample noise before quality is used for promotion.</span></div>
  <div class="method-card"><b>Breakout model</b><span>Predicts future upside from early-window item features.</span></div>
  <div class="method-card"><b>Uplift model</b><span>Estimates whether extra exposure is expected to help an item.</span></div>
  <div class="method-card"><b>Bandit policies</b><span>Compares reward, regret, and exploration breadth across policy choices.</span></div>
  <div class="method-card"><b>IPS stress test</b><span>Checks how unstable offline estimates become as target policy moves away from the logger.</span></div>
</div>
""",
        unsafe_allow_html=True,
    )
    st.subheader("How to read the system")
    st.markdown(
        """
1. Start with the ablation table. It shows whether the full scoring policy changes the candidate set compared with popularity.
2. Check policy comparison. A policy that gets reward by exposing one item is not a useful discovery system.
3. Check fairness. Lower concentration is useful only if quality does not collapse.
4. Check IPS. If effective sample size falls too much, offline estimates should not be trusted.
"""
    )

elif section == "Opportunity Explorer":
    st.markdown(
        f"""
<div class="section-note">
The scatter plot separates {term('shrunk quality', 'Observed quality after Beta-Binomial correction for sample size.')} from {term('uplift', 'Estimated incremental reward from extra exposure.')}. Larger points have more uncertainty, so they may need exploration rather than immediate heavy ranking.
</div>
""",
        unsafe_allow_html=True,
    )
    genres = sorted(promotion.get("primary_genre", pd.Series(["Unknown"])).dropna().astype(str).unique().tolist())
    col_a, col_b, col_c = st.columns([1, 1, 1])
    genre = col_a.selectbox("Genre", ["All"] + genres)
    min_quality = col_b.slider("Minimum shrunk quality", 0.0, 1.0, 0.0, 0.05)
    max_items = col_c.slider("Rows", 20, 200, 75, 5)

    view = promotion.copy()
    if genre != "All" and "primary_genre" in view.columns:
        view = view[view["primary_genre"].astype(str).eq(genre)]
    if "shrunk_mean" in view.columns:
        view = view[view["shrunk_mean"].astype(float) >= min_quality]
    view = view.sort_values("promotion_score", ascending=False).head(max_items)

    fig = px.scatter(
        view,
        x="shrunk_mean",
        y="uplift_score",
        size="posterior_uncertainty" if "posterior_uncertainty" in view.columns else None,
        color="primary_genre" if "primary_genre" in view.columns else None,
        hover_data=[c for c in ["item_id", "title", "creator_id", "promotion_score", "breakout_score"] if c in view.columns],
        title="Quality vs uplift, sized by uncertainty",
    )
    st.plotly_chart(configure_fig(fig), use_container_width=True)
    table_cols = [
        "item_id",
        "title",
        "creator_id",
        "primary_genre",
        "promotion_score",
        "shrunk_mean",
        "breakout_score",
        "uplift_score",
        "posterior_uncertainty",
        "popularity_percentile",
    ]
    st.dataframe(view[[c for c in table_cols if c in view.columns]], use_container_width=True, hide_index=True)

elif section == "Policy Comparison":
    st.markdown(
        f"""
<div class="section-note">
A useful policy needs more than reward. It should keep {term('regret', 'Reward lost compared with the best available arm in the simulation.')} controlled while exposing more than the same few items.
</div>
""",
        unsafe_allow_html=True,
    )
    if bandit.empty:
        st.warning("No bandit policy metrics found.")
    else:
        final = final_by_policy(bandit)
        c1, c2 = st.columns(2)
        with c1:
            fig = px.line(bandit, x="round", y="cumulative_reward", color="policy", title="Cumulative reward")
            st.plotly_chart(configure_fig(fig), use_container_width=True)
        with c2:
            fig = px.line(bandit, x="round", y="cumulative_regret", color="policy", title="Cumulative regret")
            st.plotly_chart(configure_fig(fig), use_container_width=True)
        fig = px.bar(final, x="policy", y="unique_items_exposed", color="policy", title="Exploration breadth at final round")
        st.plotly_chart(configure_fig(fig), use_container_width=True)
        st.dataframe(final, use_container_width=True, hide_index=True)

elif section == "Fairness":
    st.markdown(
        f"""
<div class="section-note">
{term('Gini', 'Exposure inequality across creators. Lower means exposure is less concentrated.')} and {term('HHI', 'Concentration index. Higher values mean exposure is controlled by fewer creators.')} help detect whether ranking collapses toward a small creator set.
</div>
""",
        unsafe_allow_html=True,
    )
    if fairness.empty or frontier.empty:
        st.warning("No fairness artifacts found.")
    else:
        c1, c2 = st.columns(2)
        with c1:
            fig = px.line(fairness, x="day", y="gini", color="policy", title="Creator exposure Gini over time")
            st.plotly_chart(configure_fig(fig), use_container_width=True)
        with c2:
            fig = px.line(fairness, x="day", y="active_creators", color="policy", title="Active creators over time")
            st.plotly_chart(configure_fig(fig), use_container_width=True)
        fig = px.scatter(
            frontier,
            x="gini",
            y="mean_relevance",
            size="long_tail_viability",
            color="mean_novelty",
            hover_data=["lambda_novelty", "lambda_fairness", "hhi"],
            title="Pareto frontier: relevance vs exposure concentration",
        )
        st.plotly_chart(configure_fig(fig), use_container_width=True)
        st.dataframe(frontier, use_container_width=True, hide_index=True)

elif section == "IPS Stress Test":
    st.markdown(
        f"""
<div class="section-note">
{term('IPS', 'Inverse propensity scoring reweights logged outcomes to estimate a target policy.')} becomes fragile when target policy probabilities are very different from logging policy probabilities. Watch p95 weight and effective sample size.
</div>
""",
        unsafe_allow_html=True,
    )
    if ips.empty:
        st.warning("No IPS stress-test artifact found.")
    else:
        c1, c2 = st.columns(2)
        with c1:
            fig = px.bar(
                ips,
                x="target_policy",
                y=["ips", "snips", "clipped_ips_10", "doubly_robust"],
                barmode="group",
                title="Off-policy value estimates",
            )
            st.plotly_chart(configure_fig(fig), use_container_width=True)
        with c2:
            fig = px.bar(ips, x="target_policy", y="effective_sample_size", color="target_policy", title="Effective sample size")
            st.plotly_chart(configure_fig(fig), use_container_width=True)
        fig = px.bar(ips, x="target_policy", y="p95_weight", color="target_policy", title="p95 importance weight")
        st.plotly_chart(configure_fig(fig), use_container_width=True)
        st.dataframe(ips, use_container_width=True, hide_index=True)

elif section == "Limitations":
    st.markdown(
        """
<div class="warning-note">
This project is useful as an offline ranking and evaluation design, but it does not prove production lift. The exposure data is simulated, and the uplift estimates are not causal proof without randomized treatment assignment.
</div>
""",
        unsafe_allow_html=True,
    )
    st.subheader("Known limitations")
    st.markdown(
        """
- Exposure logs are simulated, not real production impressions.
- IPS depends on known logging propensities and sufficient overlap.
- Uplift scoring needs randomized or quasi-random treatment for real causal interpretation.
- Content safety, spam resistance, fatigue, and creator gaming are not modeled.
- The dashboard is designed for explanation, not production monitoring.
"""
    )
    st.subheader("Project files")
    st.markdown(
        """
- `PROJECT_REPORT.md`: short technical explanation.
- `reports/system_b_final_report.md`: generated artifact summary.
- `scripts/import_system_a_artifacts.py`: bridge from separate System A checkout.
- `scripts/run_system_b_pipeline.py`: full artifact generator.
"""
    )
    if REPORT_PATH.exists():
        with st.expander("Generated report preview"):
            st.markdown(REPORT_PATH.read_text(encoding="utf-8"))

st.markdown(
    """
<div class="footer-note">
Review note: this demo should be evaluated as an offline policy-design system. Its strongest parts are shrinkage, explicit policy comparison, concentration metrics, and IPS stress testing. Its weakest assumption is simulated exposure data.
</div>
""",
    unsafe_allow_html=True,
)

