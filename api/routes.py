"""
BETSOKA — API Routes
=====================
REST endpoints for data generation, model training, evaluation, and prediction.
All state is held in module-level variables for this demo.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import numpy as np
import pandas as pd

from core.data_processing import generate_synthetic_matches, preprocess, scale_single_input
from core.services import train_all, evaluate_all, build_comparison_table, predict
from core.config import FEATURE_COLUMNS, OUTCOME_LABELS, FEATURE_LABELS

router = APIRouter()

# ─────────────────────────────────────────────
# In-memory state (demo only)
# ─────────────────────────────────────────────
_state = {
    "data": None,
    "models": None,
    "results": None,
    "scaler": None,
    "comparison": None,
    "feature_names": FEATURE_COLUMNS,
}


# ─────────────────────────────────────────────
# Pydantic Schemas
# ─────────────────────────────────────────────
class GenerateRequest(BaseModel):
    n_matches: int = 2000


class PredictRequest(BaseModel):
    model_name: str
    home_strength: float
    away_strength: float
    home_form: float
    away_form: float
    home_avg_goals: float
    away_avg_goals: float
    home_shots_on_target: float
    away_shots_on_target: float
    possession_diff: float
    home_advantage: float
    h2h_advantage: float
    goal_diff_trend: float


# ─────────────────────────────────────────────
# Endpoints
# ─────────────────────────────────────────────

@router.get("/status")
def get_status():
    """Returns current system state."""
    return {
        "data_loaded": _state["data"] is not None,
        "data_rows": len(_state["data"]) if _state["data"] is not None else 0,
        "models_trained": _state["models"] is not None,
        "model_names": list(_state["models"].keys()) if _state["models"] else [],
    }


@router.post("/generate")
def generate_data(req: GenerateRequest):
    """Generate synthetic match dataset."""
    df = generate_synthetic_matches(req.n_matches)
    _state["data"] = df
    _state["models"] = None
    _state["results"] = None
    _state["comparison"] = None

    # Outcome distribution
    dist = df["outcome"].value_counts().sort_index().to_dict()
    dist_labeled = {OUTCOME_LABELS[k]: int(v) for k, v in dist.items()}

    return {
        "message": f"Generated {req.n_matches} matches",
        "rows": len(df),
        "columns": list(df.columns),
        "outcome_distribution": dist_labeled,
        "sample": df.head(5).to_dict(orient="records"),
        "stats": df.describe().round(2).to_dict(),
    }


@router.post("/train")
def train_models():
    """Train all 3 models on current dataset."""
    if _state["data"] is None:
        raise HTTPException(status_code=400, detail="No data generated yet. Call /api/generate first.")

    X_tr, X_te, y_tr, y_te, scaler = preprocess(_state["data"])
    models = train_all(X_tr, y_tr)
    results = evaluate_all(models, X_te, y_te)
    comparison = build_comparison_table(results)

    _state["models"] = models
    _state["results"] = results
    _state["scaler"] = scaler
    _state["comparison"] = comparison

    # Serialize results for JSON
    results_json = {}
    for name, m in results.items():
        results_json[name] = {
            "accuracy": m["accuracy"],
            "precision": m["precision"],
            "recall": m["recall"],
            "f1": m["f1"],
            "roc_auc": m["roc_auc"],
            "confusion_matrix": m["confusion_matrix"].tolist(),
        }

    # Feature importance (Random Forest)
    rf = models.get("Random Forest")
    feature_importance = None
    if rf is not None:
        imp = rf.feature_importances_
        feature_importance = [
            {"feature": FEATURE_LABELS[FEATURE_COLUMNS[i]], "key": FEATURE_COLUMNS[i], "importance": round(float(imp[i]), 4)}
            for i in range(len(FEATURE_COLUMNS))
        ]
        feature_importance.sort(key=lambda x: x["importance"], reverse=True)

    return {
        "message": "All models trained successfully",
        "results": results_json,
        "comparison": comparison.to_dict(orient="records"),
        "feature_importance": feature_importance,
    }


@router.post("/predict")
def predict_outcome(req: PredictRequest):
    """Predict match outcome using a trained model."""
    if _state["models"] is None:
        raise HTTPException(status_code=400, detail="Models not trained yet. Call /api/train first.")

    if req.model_name not in _state["models"]:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown model: {req.model_name}. Available: {list(_state['models'].keys())}",
        )

    input_values = {
        "home_strength": req.home_strength,
        "away_strength": req.away_strength,
        "home_form": req.home_form,
        "away_form": req.away_form,
        "home_avg_goals": req.home_avg_goals,
        "away_avg_goals": req.away_avg_goals,
        "home_shots_on_target": req.home_shots_on_target,
        "away_shots_on_target": req.away_shots_on_target,
        "possession_diff": req.possession_diff,
        "home_advantage": req.home_advantage,
        "h2h_advantage": req.h2h_advantage,
        "goal_diff_trend": req.goal_diff_trend,
    }

    X_scaled = scale_single_input(input_values, _state["scaler"])
    label, probs = predict(_state["models"][req.model_name], X_scaled, req.model_name)

    return {
        "predicted_outcome": label,
        "confidence": round(float(np.max(probs)) * 100, 1),
        "probabilities": {
            OUTCOME_LABELS[i]: round(float(probs[i]) * 100, 1) for i in range(3)
        },
        "model_used": req.model_name,
    }


@router.get("/features")
def get_features():
    """Returns feature definitions for building the input form."""
    features = []
    defaults = {
        "home_strength": {"min": 1, "max": 100, "default": 75, "step": 1},
        "away_strength": {"min": 1, "max": 100, "default": 65, "step": 1},
        "home_form": {"min": 0, "max": 10, "default": 7.0, "step": 0.5},
        "away_form": {"min": 0, "max": 10, "default": 5.5, "step": 0.5},
        "home_avg_goals": {"min": 0, "max": 5, "default": 1.8, "step": 0.1},
        "away_avg_goals": {"min": 0, "max": 5, "default": 1.1, "step": 0.1},
        "home_shots_on_target": {"min": 0, "max": 20, "default": 6.0, "step": 0.5},
        "away_shots_on_target": {"min": 0, "max": 20, "default": 4.0, "step": 0.5},
        "possession_diff": {"min": -25, "max": 25, "default": 5, "step": 1},
        "home_advantage": {"min": 1, "max": 10, "default": 4.5, "step": 0.5},
        "h2h_advantage": {"min": -5, "max": 5, "default": 1.0, "step": 0.5},
        "goal_diff_trend": {"min": -3, "max": 3, "default": 0.5, "step": 0.1},
    }
    for key in FEATURE_COLUMNS:
        features.append({
            "key": key,
            "label": FEATURE_LABELS[key],
            **defaults[key],
        })
    return {"features": features}
