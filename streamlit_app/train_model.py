import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.pipeline import Pipeline

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


# Load the dataset
df = pd.read_csv("dataset/student-por.csv")

# Create the academic risk target
# 1 = At Risk, 0 = Not At Risk
df["academic_risk"] = (df["G3"] <= 11).astype(int)


# Features used for early risk prediction
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


# Separate numerical and categorical columns
numerical_features = [
    "absences",
    "studytime",
    "failures",
    "G1",
    "G2"
]

categorical_features = [
    "schoolsup",
    "famsup",
    "higher",
    "internet",
    "activities",
    "paid"
]


# Preprocessing
preprocessor = ColumnTransformer(
    transformers=[
        (
            "numerical",
            StandardScaler(),
            numerical_features
        ),
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        )
    ]
)


# Split the dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# Models to compare
models = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Decision Tree": DecisionTreeClassifier(
        max_depth=5,
        random_state=42
    ),
    "Random Forest": RandomForestClassifier(
        n_estimators=200,
        random_state=42
    )
}


results = {}
trained_models = {}


# Train and evaluate each model
for name, model in models.items():

    pipeline = Pipeline(
        steps=[
            ("preprocessing", preprocessor),
            ("model", model)
        ]
    )

    pipeline.fit(X_train, y_train)

    predictions = pipeline.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(y_test, predictions, zero_division=0)
    recall = recall_score(y_test, predictions, zero_division=0)
    f1 = f1_score(y_test, predictions, zero_division=0)

    results[name] = {
        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1 Score": f1
    }

    trained_models[name] = pipeline


# Display results
print("\n===== MODEL RESULTS =====")

for name, metrics in results.items():

    print(f"\n{name}")

    for metric, value in metrics.items():
        print(f"{metric}: {value:.3f}")


# Select the model with the best F1 score
best_model_name = max(
    results,
    key=lambda model_name: results[model_name]["F1 Score"]
)

best_model = trained_models[best_model_name]


print("\n===== BEST MODEL =====")
print(best_model_name)


# Save the best model
joblib.dump(
    best_model,
    "academic_risk_model.pkl"
)

print("\nModel saved as academic_risk_model.pkl")