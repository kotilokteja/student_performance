"""
Central configuration for the Academic Risk Early-Warning System.

Nothing in this module changes ML behaviour. It only centralises paths,
the feature contract and human-readable label maps used by the UI.
"""

from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
FRONTEND_DIR = PROJECT_ROOT / "frontend"

# The original project kept the model at the project root and the dataset in
# ./dataset. Both locations are still checked first so the existing layout keeps
# working; ./model is only a fallback.
MODEL_CANDIDATES = [
    PROJECT_ROOT / "academic_risk_model.pkl",
    PROJECT_ROOT / "model" / "academic_risk_model.pkl",
]
DATA_CANDIDATES = [
    PROJECT_ROOT / "dataset" / "student-por.csv",
    PROJECT_ROOT / "student-por.csv",
]


def resolve(candidates):
    for path in candidates:
        if path.exists():
            return path
    return candidates[0]


MODEL_PATH = resolve(MODEL_CANDIDATES)
DATA_PATH = resolve(DATA_CANDIDATES)

# ---------------------------------------------------------------------------
# ML contract  (unchanged from the original project)
# ---------------------------------------------------------------------------
FEATURES = [
    "absences", "studytime", "failures", "G1", "G2",
    "schoolsup", "famsup", "higher", "internet", "activities", "paid",
]

NUMERICAL_FEATURES = ["absences", "studytime", "failures", "G1", "G2"]
CATEGORICAL_FEATURES = ["schoolsup", "famsup", "higher", "internet", "activities", "paid"]

TARGET = "academic_risk"
RISK_THRESHOLD_G3 = 11  # G3 <= 11  ->  At Risk (1)

TEST_SIZE = 0.2
RANDOM_STATE = 42

# ---------------------------------------------------------------------------
# UI label maps  (presentation only — the model always receives the raw values)
# ---------------------------------------------------------------------------
STUDY_TIME_OPTIONS = [
    "Less than 2 hours",
    "2–5 hours",
    "5–10 hours",
    "More than 10 hours",
]
STUDY_TIME_TO_CODE = {
    "Less than 2 hours": 1,
    "2–5 hours": 2,
    "5–10 hours": 3,
    "More than 10 hours": 4,
}
CODE_TO_STUDY_TIME = {v: k for k, v in STUDY_TIME_TO_CODE.items()}

YES_NO_OPTIONS = ["yes", "no"]          # stored / sent to the model
YES_NO_LABELS = {"yes": "Yes", "no": "No"}  # shown to the user

FEATURE_LABELS = {
    "absences": "Absences",
    "studytime": "Study Time",
    "failures": "Failures",
    "G1": "G1",
    "G2": "G2",
}

# ---------------------------------------------------------------------------
# Navigation
# ---------------------------------------------------------------------------
NAV_GROUPS = [
    ("Overview", ["Dashboard", "Risk Assessment"]),
    ("Analytics", ["Model Performance", "Dataset Insights"]),
    ("Project", ["About"]),
]
DEFAULT_PAGE = "Dashboard"

APP_NAME = "Aegis"
APP_TAGLINE = "Academic Early-Warning System"
APP_VERSION = "4.0"
