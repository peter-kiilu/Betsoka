"""
BETSOKA Services
================
Model training, evaluation, and prediction services.
Implements Logistic Regression, Random Forest, and a Keras ANN.
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_recall_fscore_support,
    confusion_matrix,
    roc_auc_score,
)

import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"        # suppress TF warnings

import tensorflow as tf
tf.get_logger().setLevel("ERROR")

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, BatchNormalization
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping

from core.config import (
    LOGISTIC_REGRESSION_PARAMS,
    RANDOM_FOREST_PARAMS,
    ANN_PARAMS,
    OUTCOME_LABELS,
)


# ═══════════════════════════════════════════════
# TRAINING
# ═══════════════════════════════════════════════

def train_logistic_regression(X_train, y_train):
    model = LogisticRegression(**LOGISTIC_REGRESSION_PARAMS)
    model.fit(X_train, y_train)
    return model


def train_random_forest(X_train, y_train):
    model = RandomForestClassifier(**RANDOM_FOREST_PARAMS)
    model.fit(X_train, y_train)
    return model


def train_ann(X_train, y_train):
    y_cat = to_categorical(y_train, num_classes=3)
    cfg = ANN_PARAMS

    model = Sequential()
    model.add(Dense(cfg["layers"][0], activation="relu", input_shape=(X_train.shape[1],)))
    model.add(BatchNormalization())
    model.add(Dropout(cfg["dropout"]))

    for units in cfg["layers"][1:]:
        model.add(Dense(units, activation="relu"))
        model.add(Dropout(cfg["dropout"] * 0.7))

    model.add(Dense(3, activation="softmax"))

    model.compile(
        optimizer=Adam(learning_rate=cfg["learning_rate"]),
        loss="categorical_crossentropy",
        metrics=["accuracy"],
    )

    early_stop = EarlyStopping(monitor="loss", patience=5, restore_best_weights=True)

    model.fit(
        X_train, y_cat,
        epochs=cfg["epochs"],
        batch_size=cfg["batch_size"],
        verbose=0,
        callbacks=[early_stop],
    )
    return model


def train_all(X_train, y_train):
    """Trains all three models and returns them as a dict."""
    return {
        "Logistic Regression": train_logistic_regression(X_train, y_train),
        "Random Forest": train_random_forest(X_train, y_train),
        "Neural Network (ANN)": train_ann(X_train, y_train),
    }


# ═══════════════════════════════════════════════
# EVALUATION
# ═══════════════════════════════════════════════

def evaluate_model(model, X_test, y_test, model_type="sklearn"):
    """Returns a dict of metrics + predictions for a single model."""
    if model_type == "keras":
        y_prob = model.predict(X_test, verbose=0)
        y_pred = np.argmax(y_prob, axis=1)
    else:
        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test)

    acc = accuracy_score(y_test, y_pred)
    prec, rec, f1, _ = precision_recall_fscore_support(y_test, y_pred, average="weighted")

    try:
        auc = roc_auc_score(y_test, y_prob, multi_class="ovr")
    except Exception:
        auc = 0.0

    cm = confusion_matrix(y_test, y_pred, labels=[0, 1, 2])

    return {
        "accuracy": round(acc, 4),
        "precision": round(prec, 4),
        "recall": round(rec, 4),
        "f1": round(f1, 4),
        "roc_auc": round(auc, 4),
        "confusion_matrix": cm,
        "y_pred": y_pred,
        "y_prob": y_prob,
    }


def evaluate_all(models, X_test, y_test):
    results = {}
    for name, model in models.items():
        mtype = "keras" if name == "Neural Network (ANN)" else "sklearn"
        results[name] = evaluate_model(model, X_test, y_test, model_type=mtype)
    return results


def build_comparison_table(results: dict) -> pd.DataFrame:
    rows = []
    for name, m in results.items():
        rows.append({
            "Model": name,
            "Accuracy": m["accuracy"],
            "Precision": m["precision"],
            "Recall": m["recall"],
            "F1-Score": m["f1"],
            "ROC-AUC": m["roc_auc"],
        })
    return pd.DataFrame(rows)


# ═══════════════════════════════════════════════
# PREDICTION
# ═══════════════════════════════════════════════

def predict(model, X_scaled, model_name: str):
    """Returns (predicted_class_label, probability_array)."""
    if model_name == "Neural Network (ANN)":
        probs = model.predict(X_scaled, verbose=0)[0]
    else:
        probs = model.predict_proba(X_scaled)[0]

    predicted_idx = int(np.argmax(probs))
    return OUTCOME_LABELS[predicted_idx], probs
