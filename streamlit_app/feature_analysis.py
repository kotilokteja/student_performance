import pandas as pd

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

print("\n===== FEATURE INFORMATION =====")
print(df[features].dtypes)

print("\n===== AVERAGE VALUES BY RISK GROUP =====")
print(df.groupby("academic_risk")[[
    "absences",
    "studytime",
    "failures",
    "G1",
    "G2"
]].mean())

print("\n===== CATEGORICAL FEATURES BY RISK GROUP =====")

for feature in [
    "schoolsup",
    "famsup",
    "higher",
    "internet",
    "activities",
    "paid"
]:
    print(f"\n{feature}")
    print(pd.crosstab(df[feature], df["academic_risk"], normalize="index"))