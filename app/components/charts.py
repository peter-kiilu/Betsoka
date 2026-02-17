"""
BETSOKA — Chart Components
===========================
Reusable Plotly and Matplotlib chart helpers for the UI.
"""

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from core.config import OUTCOME_LABELS, OUTCOME_COLORS, THEME


# ═══════════════════════════════════════════════
# CONFUSION MATRIX
# ═══════════════════════════════════════════════

def confusion_matrix_chart(cm, model_name: str):
    labels = [OUTCOME_LABELS[i] for i in range(3)]
    fig = go.Figure(
        data=go.Heatmap(
            z=cm,
            x=labels,
            y=labels,
            colorscale=[[0, "#1A1A2E"], [1, THEME["primary"]]],
            text=cm,
            texttemplate="%{text}",
            textfont={"size": 16, "color": "white"},
            hovertemplate="Actual: %{y}<br>Predicted: %{x}<br>Count: %{z}<extra></extra>",
            showscale=False,
        )
    )
    fig.update_layout(
        title=dict(text=f"Confusion Matrix — {model_name}", font=dict(size=14)),
        xaxis_title="Predicted",
        yaxis_title="Actual",
        yaxis=dict(autorange="reversed"),
        height=380,
        margin=dict(l=60, r=20, t=50, b=50),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=THEME["text_light"]),
    )
    return fig


# ═══════════════════════════════════════════════
# MODEL COMPARISON
# ═══════════════════════════════════════════════

def model_comparison_chart(comparison_df: pd.DataFrame):
    metrics = ["Accuracy", "Precision", "Recall", "F1-Score", "ROC-AUC"]
    colors = [THEME["primary"], THEME["success"], THEME["warning"]]

    fig = go.Figure()
    for i, model in enumerate(comparison_df["Model"]):
        fig.add_trace(go.Bar(
            name=model,
            x=metrics,
            y=comparison_df[comparison_df["Model"] == model][metrics].values[0],
            marker_color=colors[i % len(colors)],
            text=[f"{v:.2f}" for v in comparison_df[comparison_df["Model"] == model][metrics].values[0]],
            textposition="outside",
        ))

    fig.update_layout(
        title=dict(text="Model Performance Comparison", font=dict(size=16)),
        barmode="group",
        yaxis=dict(range=[0, 1.12]),
        height=420,
        legend=dict(orientation="h", y=-0.15),
        margin=dict(l=40, r=20, t=50, b=60),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=THEME["text_light"]),
    )
    return fig


# ═══════════════════════════════════════════════
# FEATURE IMPORTANCE
# ═══════════════════════════════════════════════

def feature_importance_chart(model, feature_names: list):
    importances = model.feature_importances_
    idx = np.argsort(importances)

    fig = go.Figure(go.Bar(
        x=importances[idx],
        y=[feature_names[i] for i in idx],
        orientation="h",
        marker=dict(
            color=importances[idx],
            colorscale=[[0, THEME["secondary"]], [1, THEME["primary"]]],
        ),
        text=[f"{v:.3f}" for v in importances[idx]],
        textposition="outside",
    ))
    fig.update_layout(
        title=dict(text="Feature Importance (Random Forest)", font=dict(size=14)),
        height=420,
        margin=dict(l=160, r=40, t=50, b=30),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=THEME["text_light"]),
        xaxis=dict(title="Relative Importance"),
    )
    return fig


# ═══════════════════════════════════════════════
# PROBABILITY GAUGE
# ═══════════════════════════════════════════════

def probability_gauge(probs):
    """Returns a horizontal stacked bar showing probability breakdown."""
    labels = [OUTCOME_LABELS[i] for i in range(3)]
    colors = [OUTCOME_COLORS[l] for l in labels]

    fig = go.Figure()
    for i, (label, color) in enumerate(zip(labels, colors)):
        fig.add_trace(go.Bar(
            y=["Prediction"],
            x=[probs[i] * 100],
            name=f"{label} ({probs[i]*100:.1f}%)",
            orientation="h",
            marker_color=color,
            text=f"{probs[i]*100:.1f}%",
            textposition="inside",
            insidetextfont=dict(size=14, color="white"),
        ))

    fig.update_layout(
        barmode="stack",
        height=120,
        margin=dict(l=0, r=0, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=THEME["text_light"]),
        legend=dict(orientation="h", y=-0.6),
        xaxis=dict(range=[0, 100], showticklabels=False),
        yaxis=dict(showticklabels=False),
    )
    return fig


# ═══════════════════════════════════════════════
# DATA DISTRIBUTION
# ═══════════════════════════════════════════════

def outcome_distribution_chart(df):
    labels = [OUTCOME_LABELS[i] for i in range(3)]
    counts = df["outcome"].value_counts().sort_index()
    colors = [OUTCOME_COLORS[l] for l in labels]

    fig = go.Figure(go.Pie(
        labels=labels,
        values=counts.values,
        marker=dict(colors=colors),
        hole=0.5,
        textinfo="label+percent",
        textfont=dict(size=13),
    ))
    fig.update_layout(
        title=dict(text="Outcome Distribution", font=dict(size=14)),
        height=350,
        margin=dict(l=20, r=20, t=50, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color=THEME["text_light"]),
        showlegend=False,
    )
    return fig
