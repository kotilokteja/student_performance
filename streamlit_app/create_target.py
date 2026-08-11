import pandas as pd

df = pd.read_csv("dataset/student-por.csv")

# Students with a final grade of 11 or below are considered at risk.
df["academic_risk"] = (df["G3"] <= 11).astype(int)

print("\n===== ACADEMIC RISK DISTRIBUTION =====")
print(df["academic_risk"].value_counts())

print("\n0 = Not At Risk")
print("1 = At Risk")