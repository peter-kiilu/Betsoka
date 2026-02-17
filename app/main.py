"""
BETSOKA — Main Entry Point
============================
Streamlit application with page routing and session state management.

Run with:
    streamlit run app/main.py
"""

import sys, os

# Ensure project root is on sys.path so `core.*` and `app.*` imports work
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st

from core.config import THEME
from core.data_processing import generate_synthetic_matches, preprocess
from core.services import train_all, evaluate_all

from app.components.sidebar import render_sidebar
from app.pages import dashboard, analytics, settings


# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="BETSOKA — AI Football Predictor",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# GLOBAL CSS
# ─────────────────────────────────────────────
st.markdown(
    f"""
    <style>
        /* ── Import Google Font ────────────── */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        html, body, [class*="st-"] {{
            font-family: 'Inter', sans-serif;
        }}

        /* ── Sidebar ──────────────────────── */
        section[data-testid="stSidebar"] {{
            background: linear-gradient(180deg, {THEME['bg_dark']} 0%, {THEME['secondary']} 100%);
        }}

        /* ── Buttons ──────────────────────── */
        .stButton > button {{
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.3s ease;
        }}
        .stButton > button:hover {{
            transform: translateY(-1px);
            box-shadow: 0 4px 15px rgba(108,99,255,0.4);
        }}
        div[data-testid="stFormSubmitButton"] > button,
        button[kind="primary"] {{
            background: linear-gradient(135deg, {THEME['gradient_start']}, {THEME['gradient_end']}) !important;
            color: white !important;
            border: none !important;
        }}

        /* ── Metrics ──────────────────────── */
        [data-testid="stMetric"] {{
            background: {THEME['bg_card']};
            padding: 1rem;
            border-radius: 10px;
            border: 1px solid rgba(108,99,255,0.15);
        }}

        /* ── Remove Streamlit branding ───── */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}

        /* ── Dividers ─────────────────────── */
        hr {{
            border-color: rgba(108,99,255,0.15);
        }}

        /* ── Tabs ─────────────────────────── */
        .stTabs [data-baseweb="tab"] {{
            font-weight: 600;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)


# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
for key in ("data", "models", "results", "scaler", "trained"):
    if key not in st.session_state:
        st.session_state[key] = None if key != "trained" else False


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
page, n_matches, gen_btn, train_btn = render_sidebar()


# ─────────────────────────────────────────────
# ACTIONS
# ─────────────────────────────────────────────
if gen_btn:
    with st.spinner("⚡ Generating synthetic match data..."):
        df = generate_synthetic_matches(n_matches)
        st.session_state.data = df
        # Save a snapshot to data/sample.csv
        os.makedirs(os.path.join(os.path.dirname(__file__), "..", "data"), exist_ok=True)
        df.to_csv(os.path.join(os.path.dirname(__file__), "..", "data", "sample.csv"), index=False)
        st.session_state.trained = False
        st.session_state.models = None
        st.session_state.results = None
    st.toast(f"✅ Generated {n_matches:,} matches!", icon="⚽")
    st.rerun()

if train_btn:
    if st.session_state.data is None:
        st.sidebar.error("Generate data first!")
    else:
        with st.spinner("🧠 Preprocessing & training 3 models..."):
            X_tr, X_te, y_tr, y_te, scaler = preprocess(st.session_state.data)
            models = train_all(X_tr, y_tr)
            results = evaluate_all(models, X_te, y_te)

            st.session_state.models = models
            st.session_state.results = results
            st.session_state.scaler = scaler
            st.session_state.trained = True
        st.toast("✅ All models trained & evaluated!", icon="🧠")
        st.rerun()


# ─────────────────────────────────────────────
# PAGE ROUTING
# ─────────────────────────────────────────────
if page == "🎯 Dashboard":
    dashboard.render(
        models=st.session_state.models or {},
        scaler=st.session_state.scaler,
        results=st.session_state.results or {},
    )
elif page == "📊 Analytics":
    analytics.render(
        models=st.session_state.models or {},
        results=st.session_state.results or {},
        data=st.session_state.data,
    )
elif page == "⚙️ Settings":
    settings.render()
