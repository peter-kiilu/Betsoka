"""
BETSOKA Configuration
=====================
Central configuration for the entire BETSOKA system.
Defines feature schemas, model parameters, theme colors, and constants.
"""

# ─────────────────────────────────────────────
# Feature Definitions
# ─────────────────────────────────────────────
FEATURE_COLUMNS = [
    "home_strength",
    "away_strength",
    "home_form",
    "away_form",
    "home_avg_goals",
    "away_avg_goals",
    "home_shots_on_target",
    "away_shots_on_target",
    "possession_diff",
    "home_advantage",
    "h2h_advantage",
    "goal_diff_trend",
]

FEATURE_LABELS = {
    "home_strength": "Home Team Strength (1–100)",
    "away_strength": "Away Team Strength (1–100)",
    "home_form": "Home Recent Form (0–10)",
    "away_form": "Away Recent Form (0–10)",
    "home_avg_goals": "Avg Goals Scored (Home)",
    "away_avg_goals": "Avg Goals Scored (Away)",
    "home_shots_on_target": "Shots on Target (Home)",
    "away_shots_on_target": "Shots on Target (Away)",
    "possession_diff": "Possession % Difference",
    "home_advantage": "Home Advantage Factor",
    "h2h_advantage": "Head-to-Head Advantage",
    "goal_diff_trend": "Goal Difference Trend",
}

TARGET_COLUMN = "outcome"

OUTCOME_LABELS = {0: "Away Win", 1: "Draw", 2: "Home Win"}
OUTCOME_COLORS = {"Away Win": "#e74c3c", "Draw": "#f39c12", "Home Win": "#2ecc71"}

# ─────────────────────────────────────────────
# Model Parameters
# ─────────────────────────────────────────────
DEFAULT_N_MATCHES = 2000
TEST_SIZE = 0.2
RANDOM_STATE = 42

LOGISTIC_REGRESSION_PARAMS = {
    "solver": "lbfgs",
    "max_iter": 1000,
    "random_state": RANDOM_STATE,
}

RANDOM_FOREST_PARAMS = {
    "n_estimators": 150,
    "max_depth": 12,
    "random_state": RANDOM_STATE,
}

ANN_PARAMS = {
    "layers": [64, 32, 16],
    "dropout": 0.3,
    "epochs": 60,
    "batch_size": 32,
    "learning_rate": 0.001,
}

# ─────────────────────────────────────────────
# UI Theme
# ─────────────────────────────────────────────
THEME = {
    "primary": "#6C63FF",
    "secondary": "#2D2B55",
    "accent": "#A29BFE",
    "success": "#00D2FF",
    "warning": "#F7B731",
    "danger": "#FF6B6B",
    "bg_dark": "#0E1117",
    "bg_card": "#1A1A2E",
    "text_light": "#E0E0E0",
    "gradient_start": "#6C63FF",
    "gradient_end": "#00D2FF",
}

MODEL_NAMES = ["Logistic Regression", "Random Forest", "Neural Network (ANN)"]
