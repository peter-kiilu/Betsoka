"""
BETSOKA Data Processing
=======================
Handles synthetic data generation and preprocessing pipeline.
All data is generated programmatically — no external APIs or datasets.
"""

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from core.config import (
    FEATURE_COLUMNS,
    TARGET_COLUMN,
    DEFAULT_N_MATCHES,
    TEST_SIZE,
    RANDOM_STATE,
)


# ═══════════════════════════════════════════════
# SYNTHETIC DATA GENERATION
# ═══════════════════════════════════════════════

def generate_synthetic_matches(n_matches: int = DEFAULT_N_MATCHES) -> pd.DataFrame:
    """
    Generates a realistic synthetic football match dataset.

    The outcome is determined by a probabilistic latent‑score model
    that combines team strength, form, and situational factors with
    controlled stochastic noise so that resulting accuracy is in the
    60–80 % range — realistic for football prediction tasks.
    """
    rng = np.random.default_rng(RANDOM_STATE)

    # ── Base team attributes ──────────────────
    home_strength = rng.integers(35, 96, size=n_matches)
    away_strength = rng.integers(35, 96, size=n_matches)

    home_form = np.round(rng.uniform(1.5, 9.5, size=n_matches), 2)
    away_form = np.round(rng.uniform(1.5, 9.5, size=n_matches), 2)

    # ── Performance statistics ────────────────
    home_avg_goals = np.round((home_strength / 45) + rng.normal(0, 0.25, n_matches), 2)
    away_avg_goals = np.round((away_strength / 45) + rng.normal(0, 0.25, n_matches), 2)

    home_shots = np.round((home_strength / 10) + rng.integers(0, 5, size=n_matches), 1)
    away_shots = np.round((away_strength / 10) + rng.integers(0, 5, size=n_matches), 1)

    # ── Contextual features ───────────────────
    possession_diff = np.round(
        np.clip((home_strength - away_strength) / 5 + rng.normal(0, 2, n_matches), -25, 25), 2
    )
    home_advantage = np.round(rng.uniform(2, 6, size=n_matches), 2)
    h2h_advantage = np.round(rng.uniform(-5, 5, size=n_matches), 2)
    goal_diff_trend = np.round(
        (home_form - away_form) / 2 + rng.normal(0, 0.5, n_matches), 2
    )

    # ── Latent score → outcome ────────────────
    latent = (
        (home_strength - away_strength) * 0.35
        + (home_form - away_form) * 2.0
        + home_advantage
        + h2h_advantage * 0.8
        + goal_diff_trend * 1.2
        + rng.normal(0, 10, n_matches)      # stochastic noise
    )
    outcome = np.where(latent > 7, 2, np.where(latent < -7, 0, 1)).astype(int)

    df = pd.DataFrame(
        {
            FEATURE_COLUMNS[0]: home_strength,
            FEATURE_COLUMNS[1]: away_strength,
            FEATURE_COLUMNS[2]: home_form,
            FEATURE_COLUMNS[3]: away_form,
            FEATURE_COLUMNS[4]: home_avg_goals,
            FEATURE_COLUMNS[5]: away_avg_goals,
            FEATURE_COLUMNS[6]: home_shots,
            FEATURE_COLUMNS[7]: away_shots,
            FEATURE_COLUMNS[8]: possession_diff,
            FEATURE_COLUMNS[9]: home_advantage,
            FEATURE_COLUMNS[10]: h2h_advantage,
            FEATURE_COLUMNS[11]: goal_diff_trend,
            TARGET_COLUMN: outcome,
        }
    )
    return df


# ═══════════════════════════════════════════════
# PREPROCESSING PIPELINE
# ═══════════════════════════════════════════════

def preprocess(df: pd.DataFrame):
    """
    Splits and scales the dataset.
    Returns: X_train, X_test, y_train, y_test, fitted_scaler
    """
    X = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMN]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
    )

    scaler = StandardScaler()
    X_train_scaled = pd.DataFrame(scaler.fit_transform(X_train), columns=FEATURE_COLUMNS)
    X_test_scaled = pd.DataFrame(scaler.transform(X_test), columns=FEATURE_COLUMNS)

    return X_train_scaled, X_test_scaled, y_train.reset_index(drop=True), y_test.reset_index(drop=True), scaler


def scale_single_input(values: dict, scaler: StandardScaler) -> np.ndarray:
    """Scales a single user‑provided input row for prediction."""
    row = pd.DataFrame([values], columns=FEATURE_COLUMNS)
    return scaler.transform(row)
