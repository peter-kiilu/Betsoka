"""
BETSOKA — Analytics Page
=========================
Model evaluation metrics, confusion matrices, feature importance,
and side‑by‑side model comparison.
"""

import streamlit as st
import pandas as pd

from core.config import FEATURE_COLUMNS, THEME
from core.services import build_comparison_table
from app.components.charts import (
    confusion_matrix_chart,
    model_comparison_chart,
    feature_importance_chart,
    outcome_distribution_chart,
)


def render(models: dict, results: dict, data):
    """Renders the analytics page."""

    st.markdown(
        f"""
        <div style="padding: 1.5rem 0 0.8rem 0;">
            <h2 style="margin:0;
                background: linear-gradient(135deg, {THEME['gradient_start']}, {THEME['gradient_end']});
                -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                📊 Model Analytics
            </h2>
            <p style="color:{THEME['text_light']}; font-size:0.9rem; margin-top:0.3rem;">
                Evaluate and compare machine learning model performance.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not results:
        st.info("👈 Train models first to view analytics.", icon="📊")
        return

    # ── Comparison Table ──────────────────────
    comp_df = build_comparison_table(results)
    st.subheader("Performance Overview")
    st.dataframe(
        comp_df.style
            .format({c: "{:.4f}" for c in comp_df.columns if c != "Model"})
            .highlight_max(axis=0, subset=["Accuracy", "Precision", "Recall", "F1-Score", "ROC-AUC"],
                           props="background-color: #6C63FF33; color: white; font-weight: bold"),
        use_container_width=True,
        hide_index=True,
    )

    # ── Comparison Chart ──────────────────────
    st.plotly_chart(model_comparison_chart(comp_df), use_container_width=True, config={"displayModeBar": False})

    st.divider()

    # ── Per‑Model Deep Dive ───────────────────
    st.subheader("Confusion Matrices")
    cm_cols = st.columns(len(results))
    for i, (name, metrics) in enumerate(results.items()):
        with cm_cols[i]:
            st.plotly_chart(
                confusion_matrix_chart(metrics["confusion_matrix"], name),
                use_container_width=True,
                config={"displayModeBar": False},
            )

    st.divider()

    # ── Feature Importance ────────────────────
    if "Random Forest" in models:
        st.subheader("Feature Importance (Random Forest)")
        st.markdown(
            f"<p style='color:{THEME[\"text_light\"]}; font-size:0.85rem;'>"
            "Shows which input features have the most influence on predictions.</p>",
            unsafe_allow_html=True,
        )
        st.plotly_chart(
            feature_importance_chart(models["Random Forest"], FEATURE_COLUMNS),
            use_container_width=True,
            config={"displayModeBar": False},
        )

    st.divider()

    # ── Data Distribution ─────────────────────
    if data is not None:
        st.subheader("Dataset Overview")
        c1, c2 = st.columns([1, 2])
        with c1:
            st.plotly_chart(
                outcome_distribution_chart(data),
                use_container_width=True,
                config={"displayModeBar": False},
            )
        with c2:
            st.markdown(f"**Total matches:** {len(data):,}")
            st.markdown(f"**Features:** {len(FEATURE_COLUMNS)}")
            st.markdown(f"**Target classes:** Away Win, Draw, Home Win")
            st.dataframe(data.describe().round(2), use_container_width=True)
