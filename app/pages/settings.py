"""
BETSOKA — Settings / About Page
=================================
Academic information, system architecture, and presentation notes.
"""

import streamlit as st
from core.config import THEME, ANN_PARAMS, RANDOM_FOREST_PARAMS


def render():
    st.markdown(
        f"""
        <div style="padding: 1.5rem 0 0.8rem 0;">
            <h2 style="margin:0;
                background: linear-gradient(135deg, {THEME['gradient_start']}, {THEME['gradient_end']});
                -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                ⚙️ System Information
            </h2>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Synthetic Data Logic ──────────────────
    with st.expander("🧪 How Synthetic Data Is Generated", expanded=True):
        st.markdown("""
        The system generates **2 000+** simulated matches using a probabilistic framework:

        1. **Base Features** — Each team is assigned a random strength rating (35–95) and a recent‑form score.
        2. **Derived Statistics** — Goals, shots on target, and possession are computed from team strength plus Gaussian noise.
        3. **Latent Score Model** — The match outcome is determined by:

        ```
        Score = (HomeStr − AwayStr) × 0.35
              + (HomeForm − AwayForm) × 2.0
              + HomeAdvantage
              + H2H × 0.8
              + GoalDiffTrend × 1.2
              + 𝒩(0, 10)
        ```

        4. **Classification** —  Score > 7 → Home Win  |  Score < −7 → Away Win  |  else → Draw
        """)

    # ── Model Architectures ───────────────────
    with st.expander("🧠 Model Architectures"):
        st.markdown(f"""
        | Model | Architecture | Key Params |
        |---|---|---|
        | **Logistic Regression** | Linear baseline, multinomial | solver=lbfgs, max_iter=1000 |
        | **Random Forest** | Ensemble of decision trees | n_estimators={RANDOM_FOREST_PARAMS['n_estimators']}, max_depth={RANDOM_FOREST_PARAMS['max_depth']} |
        | **Neural Network (ANN)** | Multi‑layer perceptron | layers={ANN_PARAMS['layers']}, dropout={ANN_PARAMS['dropout']} |

        The **ANN** uses ReLU activation, BatchNormalization, and an Adam optimizer with early stopping.
        """)

    # ── Why Models Differ ─────────────────────
    with st.expander("📐 Why Models Differ in Performance"):
        st.markdown("""
        - **Logistic Regression** assumes linear separability; football features often interact non‑linearly
          (e.g., strength difference matters more when home advantage is high).
        - **Random Forest** captures those non‑linear interactions via ensemble decision trees.
        - **ANN** learns hierarchical feature representations but may overfit on smaller datasets.

        In practice, **Random Forest** and **ANN** typically outperform the linear baseline on this task.
        """)

    # ── Academic Conclusion ───────────────────
    with st.expander("🎓 Academic Conclusion"):
        st.markdown("""
        Football outcome prediction is inherently stochastic — even with "perfect" features,
        the random variance in sport limits maximum achievable accuracy to roughly 50–70 %.

        This demonstration system shows that a complete ML pipeline — from data generation
        through preprocessing, training, evaluation, to interactive deployment — provides
        a robust framework for decision support in sports analytics.

        **Key takeaways:**
        - Ensemble methods handle non‑linear feature interactions well.
        - Neural networks require careful regularization on tabular data.
        - Probabilistic outputs are always preferred over hard classifications.
        """)

    # ── Future Improvements ───────────────────
    with st.expander("🔮 Future Improvements"):
        st.markdown("""
        - **Player‑level data** — Incorporate injuries, suspensions, and individual form.
        - **Temporal models** — Use LSTMs or Transformers to capture time‑series form trends.
        - **Real‑world calibration** — Map synthetic distributions to historical EPL / La Liga data.
        - **Explainability** — Add SHAP values for per‑prediction feature attribution.
        - **Deployment** — Containerise with Docker and deploy to cloud (Streamlit Community Cloud, AWS).
        """)

    # ── System Architecture ───────────────────
    with st.expander("🏗️ System Architecture"):
        st.code("""
├── app/                     # Streamlit UI layer
│   ├── main.py              # Entry point
│   ├── pages/
│   │   ├── dashboard.py     # Prediction interface
│   │   ├── analytics.py     # Model evaluation
│   │   └── settings.py      # This page
│   └── components/
│       ├── sidebar.py       # Navigation & controls
│       └── charts.py        # Plotly visualizations
│
├── core/                    # Business logic
│   ├── config.py            # Central configuration
│   ├── data_processing.py   # Data gen & preprocessing
│   └── services.py          # Training, evaluation, prediction
│
├── data/
│   └── sample.csv           # Generated dataset snapshot
│
├── requirements.txt
├── .env
└── README.md
        """, language="text")

    st.divider()
    st.caption("BETSOKA © 2026 — AI Football Match Outcome Prediction Demo System — University Class Assignment")
