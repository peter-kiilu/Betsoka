"""
BETSOKA — Dashboard Page
=========================
Interactive match prediction interface.
Users input match features and receive predicted outcomes with probability breakdowns.
"""

import streamlit as st
import numpy as np

from core.config import FEATURE_LABELS, FEATURE_COLUMNS, OUTCOME_LABELS, OUTCOME_COLORS, THEME
from core.data_processing import scale_single_input
from core.services import predict
from app.components.charts import probability_gauge


def render(models: dict, scaler, results: dict):
    """Renders the prediction dashboard."""

    # ── Hero Header ───────────────────────────
    st.markdown(
        f"""
        <div style="padding: 1.5rem 0 0.8rem 0;">
            <h2 style="margin:0;
                background: linear-gradient(135deg, {THEME['gradient_start']}, {THEME['gradient_end']});
                -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                🎯 Match Outcome Predictor
            </h2>
            <p style="color:{THEME['text_light']}; font-size:0.9rem; margin-top:0.3rem;">
                Input simulated match statistics below and let the AI predict the result.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not models:
        st.info("👈 Generate data and train models using the sidebar to unlock predictions.", icon="🔒")
        return

    # ── Feature Input Form ────────────────────
    with st.container():
        cols = st.columns(3)

        sliders = {}
        feature_defaults = {
            "home_strength": (1, 100, 75),
            "away_strength": (1, 100, 65),
            "home_form": (0.0, 10.0, 7.0),
            "away_form": (0.0, 10.0, 5.5),
            "home_avg_goals": (0.0, 5.0, 1.8),
            "away_avg_goals": (0.0, 5.0, 1.1),
            "home_shots_on_target": (0.0, 20.0, 6.0),
            "away_shots_on_target": (0.0, 20.0, 4.0),
            "possession_diff": (-25.0, 25.0, 5.0),
            "home_advantage": (1.0, 10.0, 4.5),
            "h2h_advantage": (-5.0, 5.0, 1.0),
            "goal_diff_trend": (-3.0, 3.0, 0.5),
        }

        for i, feat in enumerate(FEATURE_COLUMNS):
            lo, hi, default = feature_defaults[feat]
            with cols[i % 3]:
                sliders[feat] = st.slider(
                    FEATURE_LABELS[feat], min_value=lo, max_value=hi, value=default
                )

    st.divider()

    # ── Model Selector & Predict ──────────────
    col_model, col_btn = st.columns([2, 1])
    with col_model:
        selected = st.selectbox("Select Model", list(models.keys()))
    with col_btn:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        predict_btn = st.button("🚀 Predict Outcome", use_container_width=True, type="primary")

    if predict_btn:
        X = scale_single_input(sliders, scaler)
        label, probs = predict(models[selected], X, selected)

        # ── Result Cards ──────────────────────
        st.markdown("---")
        c1, c2, c3 = st.columns([1, 1, 2])

        with c1:
            color = OUTCOME_COLORS[label]
            st.markdown(
                f"""
                <div style="background:{THEME['bg_card']}; border-left: 4px solid {color};
                    padding:1.2rem; border-radius:8px; text-align:center;">
                    <p style="margin:0; font-size:0.75rem; color:{THEME['text_light']};">PREDICTED OUTCOME</p>
                    <h2 style="margin:0.3rem 0; color:{color};">{label}</h2>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with c2:
            confidence = float(np.max(probs)) * 100
            st.markdown(
                f"""
                <div style="background:{THEME['bg_card']}; border-left: 4px solid {THEME['primary']};
                    padding:1.2rem; border-radius:8px; text-align:center;">
                    <p style="margin:0; font-size:0.75rem; color:{THEME['text_light']};">CONFIDENCE</p>
                    <h2 style="margin:0.3rem 0; color:{THEME['primary']};">{confidence:.1f}%</h2>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with c3:
            st.plotly_chart(probability_gauge(probs), use_container_width=True, config={"displayModeBar": False})

        st.caption(
            "⚠️ These are probabilistic estimates from a demo system trained on synthetic data. "
            "They are for educational purposes only and should not be used for any form of betting."
        )
