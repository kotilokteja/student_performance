"""
Data / model access layer.

Every computation here is a literal move of the logic that already existed in
app.py, train_model.py and evaluate_model.py. Nothing about the target
definition, the feature list, the split, the model or the metrics changed.
"""

import pandas as pd
import streamlit as st
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    confusion_matrix, accuracy_score, precision_score, recall_score, f1_score,
)

from .config import (
    MODEL_PATH, DATA_PATH, FEATURES, TARGET, RISK_THRESHOLD_G3,
    TEST_SIZE, RANDOM_STATE, NUMERICAL_FEATURES, CATEGORICAL_FEATURES,
    CODE_TO_STUDY_TIME,
)


# ---------------------------------------------------------------------------
# Loading (cached exactly as before)
# ---------------------------------------------------------------------------
@st.cache_resource(show_spinner=False)
def load_model():
    """Load the trained pipeline once per server process."""
    return joblib.load(MODEL_PATH)


@st.cache_data(show_spinner=False)
def load_data():
    """Load the dataset and derive the risk target: G3 <= 11 -> At Risk."""
    df = pd.read_csv(DATA_PATH)
    df[TARGET] = (df["G3"] <= RISK_THRESHOLD_G3).astype(int)
    return df


def _split(df):
    X = df[FEATURES]
    y = df[TARGET]
    return train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
    )


# ---------------------------------------------------------------------------
# Evaluation of the deployed model (identical maths to evaluate_model.py)
# ---------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def get_model_evaluation(df_cached):
    model_cached = load_model()
    _, X_test, _, y_test = _split(df_cached)
    pred = model_cached.predict(X_test)

    return {
        "accuracy": accuracy_score(y_test, pred),
        "precision": precision_score(y_test, pred),
        "recall": recall_score(y_test, pred),
        "f1": f1_score(y_test, pred),
        "cm": confusion_matrix(y_test, pred),
        "test_size": int(len(y_test)),
    }


# ---------------------------------------------------------------------------
# Algorithm comparison — replays train_model.py so the numbers are real
# instead of typed into the UI by hand. Cached: runs once per session.
# ---------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def get_model_comparison(df_cached):
    preprocessor = ColumnTransformer(
        transformers=[
            ("numerical", StandardScaler(), NUMERICAL_FEATURES),
            ("categorical", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_FEATURES),
        ]
    )

    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000),
        "Decision Tree": DecisionTreeClassifier(max_depth=5, random_state=RANDOM_STATE),
        "Random Forest": RandomForestClassifier(n_estimators=200, random_state=RANDOM_STATE),
    }

    X_train, X_test, y_train, y_test = _split(df_cached)

    rows = []
    for name, estimator in models.items():
        pipeline = Pipeline(
            steps=[("preprocessing", preprocessor), ("model", estimator)]
        )
        pipeline.fit(X_train, y_train)
        predictions = pipeline.predict(X_test)
        rows.append({
            "Model": name,
            "Accuracy": accuracy_score(y_test, predictions),
            "Precision": precision_score(y_test, predictions, zero_division=0),
            "Recall": recall_score(y_test, predictions, zero_division=0),
            "F1 Score": f1_score(y_test, predictions, zero_division=0),
        })

    return pd.DataFrame(rows)


@st.cache_resource(show_spinner=False)
def get_deployed_model_name():
    """Human name of the estimator inside the saved pipeline."""
    model = load_model()
    try:
        estimator = model.named_steps["model"]
    except Exception:
        estimator = model
    pretty = {
        "LogisticRegression": "Logistic Regression",
        "DecisionTreeClassifier": "Decision Tree",
        "RandomForestClassifier": "Random Forest",
    }
    return pretty.get(type(estimator).__name__, type(estimator).__name__)


# ---------------------------------------------------------------------------
# Dataset aggregates (same computations as the original get_dataset_insights)
# ---------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def get_dataset_insights(df_cached):
    total = len(df_cached)
    at_risk = int(df_cached[TARGET].sum())
    not_at_risk = total - at_risk

    avg = (
        df_cached.groupby(TARGET)[["absences", "studytime", "failures", "G1", "G2"]]
        .mean()
        .reset_index()
    )
    avg["Risk Status"] = avg[TARGET].map({0: "Not At Risk", 1: "At Risk"})
    avg_melt = avg.melt(
        id_vars=["Risk Status"],
        value_vars=["absences", "studytime", "failures", "G1", "G2"],
    )

    grade_counts = df_cached["G3"].value_counts().sort_index().reset_index()
    grade_counts.columns = ["Grade", "Count"]
    grade_counts["Percent"] = grade_counts["Count"] / total * 100
    grade_counts["Status"] = grade_counts["Grade"].apply(
        lambda x: "At Risk" if x <= RISK_THRESHOLD_G3 else "Not At Risk"
    )

    comparison = (
        df_cached.groupby(TARGET)[["absences", "studytime", "failures", "G1", "G2"]]
        .mean()
        .T
    )
    comparison.columns = ["Not At Risk", "At Risk"]

    overall_avg = {
        col: float(df_cached[col].mean())
        for col in ["absences", "studytime", "failures", "G1", "G2"]
    }

    return {
        "total": total,
        "at_risk": at_risk,
        "not_at_risk": not_at_risk,
        "avg_melt": avg_melt,
        "grade_counts": grade_counts,
        "comparison": comparison,
        "overall_avg": overall_avg,
        "n_columns": int(df_cached.shape[1] - 1),  # exclude the derived target
        "n_features_used": len(FEATURES),
    }


# ---------------------------------------------------------------------------
# Key insights — every sentence is derived from the dataset, none hardcoded
# ---------------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def get_key_insights(df_cached):
    total = len(df_cached)
    risk_rate = df_cached[TARGET].mean() * 100

    grouped = df_cached.groupby(TARGET)[["absences", "G2", "failures"]].mean()
    abs_risk, abs_safe = grouped.loc[1, "absences"], grouped.loc[0, "absences"]
    g2_risk, g2_safe = grouped.loc[1, "G2"], grouped.loc[0, "G2"]

    has_failures = df_cached[df_cached["failures"] > 0]
    no_failures = df_cached[df_cached["failures"] == 0]
    fail_rate = has_failures[TARGET].mean() * 100 if len(has_failures) else 0.0
    nofail_rate = no_failures[TARGET].mean() * 100 if len(no_failures) else 0.0

    low_study = df_cached[df_cached["studytime"] <= 1]
    high_study = df_cached[df_cached["studytime"] >= 3]
    low_rate = low_study[TARGET].mean() * 100 if len(low_study) else 0.0
    high_rate = high_study[TARGET].mean() * 100 if len(high_study) else 0.0

    return [
        {
            "label": "Cohort exposure",
            "text": (
                f"{risk_rate:.1f}% of the {total} students in the cohort fall below the "
                f"risk threshold of G3 ≤ {RISK_THRESHOLD_G3}."
            ),
        },
        {
            "label": "Attendance signal",
            "text": (
                f"At-risk students miss {abs_risk:.1f} classes on average versus "
                f"{abs_safe:.1f} for the rest of the cohort."
            ),
        },
        {
            "label": "Second-period grades",
            "text": (
                f"Mean G2 is {g2_risk:.1f} for at-risk students against {g2_safe:.1f} for "
                f"the rest — a gap of {g2_safe - g2_risk:.1f} points before finals."
            ),
        },
        {
            "label": "Prior failures",
            "text": (
                f"{fail_rate:.1f}% of students with at least one previous failure end up "
                f"at risk, compared with {nofail_rate:.1f}% of students with none."
            ),
        },
        {
            "label": "Study time",
            "text": (
                f"{low_rate:.1f}% of students studying less than 2 hours per week are at "
                f"risk, versus {high_rate:.1f}% of those studying 5 hours or more."
            ),
        },
    ]


def study_time_band(mean_code: float) -> str:
    """Nearest human-readable band for an average studytime code."""
    return CODE_TO_STUDY_TIME.get(int(round(mean_code)), "—")


def bootstrap():
    """Load everything the app needs, all cached."""
    df = load_data()
    return {
        "model": load_model(),
        "df": df,
        "eval": get_model_evaluation(df),
        "ds": get_dataset_insights(df),
        "insights": get_key_insights(df),
    }
