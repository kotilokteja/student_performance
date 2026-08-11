import pandas as pd

df = pd.read_csv("dataset/student-por.csv")

print("\n===== FINAL GRADE (G3) =====")
print(df["G3"].describe())

print("\n===== G3 VALUES =====")
print(df["G3"].value_counts().sort_index())

print("\n===== STUDENTS BY FINAL GRADE =====")
for grade, count in df["G3"].value_counts().sort_index().items():
    print(f"G3 = {grade}: {count} students")