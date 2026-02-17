"""
BETSOKA — Sidebar Component
============================
Renders the sidebar with navigation, data generation, and model training controls.
"""

import streamlit as st
from core.config import DEFAULT_N_MATCHES, THEME


def render_sidebar():
    """Renders the sidebar and returns the selected page name."""

    # ── Logo / Brand ──────────────────────────
    st.sidebar.markdown(
        f"""
        <div style="text-align:center; padding: 1.2rem 0 0.6rem 0;">
            <span style="font-size:2.6rem;">⚽</span>
            <h1 style="margin:0; font-size:1.8rem;
                background: linear-gradient(135deg, {THEME['gradient_start']}, {THEME['gradient_end']});
                -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                BETSOKA
            </h1>
            <p style="margin:0; font-size:0.75rem; color:{THEME['text_light']}; letter-spacing:2px;">
                AI  FOOTBALL  PREDICTOR
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.divider()

    # ── Navigation ────────────────────────────
    page = st.sidebar.radio(
        "Navigate",
        ["🎯 Dashboard", "📊 Analytics", "⚙️ Settings"],
        label_visibility="collapsed",
    )

    st.sidebar.divider()

    # ── Data Controls ─────────────────────────
    st.sidebar.markdown(
        f"<p style='color:{THEME['accent']}; font-weight:600; font-size:0.85rem;'>DATA CONTROLS</p>",
        unsafe_allow_html=True,
    )
    n_matches = st.sidebar.slider(
        "Simulated Matches",
        min_value=500,
        max_value=5000,
        value=DEFAULT_N_MATCHES,
        step=250,
    )
    generate_btn = st.sidebar.button("⚡ Generate Dataset", use_container_width=True)

    st.sidebar.divider()

    # ── Training Controls ─────────────────────
    st.sidebar.markdown(
        f"<p style='color:{THEME['accent']}; font-weight:600; font-size:0.85rem;'>MODEL TRAINING</p>",
        unsafe_allow_html=True,
    )
    train_btn = st.sidebar.button("🧠 Train All Models", use_container_width=True)

    # ── Status indicator ──────────────────────
    if st.session_state.get("trained"):
        st.sidebar.success("Models trained ✓", icon="✅")
    elif st.session_state.get("data") is not None:
        st.sidebar.info("Dataset ready — train models next", icon="📦")
    else:
        st.sidebar.warning("Generate data to begin", icon="🔄")

    return page, n_matches, generate_btn, train_btn
