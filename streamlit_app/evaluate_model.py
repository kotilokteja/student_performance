import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report


df = pd.read_csv("dataset/student-por.csv")

df["academic_risk"] = (df["G3"] <= 11).astype(int)

features = [
    "absences",
    "studytime",
    "failures",
    "G1",
    "G2",
    "schoolsup",
    "famsup",
    "higher",
    "internet",
    "activities",
    "paid"
]

X = df[features]
y = df["academic_risk"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

model = joblib.load("academic_risk_model.pkl")

predictions = model.predict(X_test)

print("\n===== CONFUSION MATRIX =====")
print(confusion_matrix(y_test, predictions))

print("\n===== CLASSIFICATION REPORT =====")
print(
    classification_report(
        y_test,
        predictions,
        target_names=["Not At Risk", "At Risk"]
    )
)