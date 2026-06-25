import pandas as pd
import mysql.connector

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# ==========================================
# MYSQL CONNECTION
# ==========================================

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="deepthi2245",   # Change to your password
    database="placement_db"
)

# ==========================================
# LOAD DATA
# ==========================================

query = "SELECT * FROM placementdata"

df = pd.read_sql(query, conn)

print("\nDataset Loaded Successfully\n")
print(df.head())

# ==========================================
# CHECK DATA
# ==========================================

print("\nDataset Shape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())

# ==========================================
# HANDLE NULL VALUES
# ==========================================

df.fillna(0, inplace=True)

# ==========================================
# CONVERT TEXT COLUMNS
# ==========================================

# PlacementTraining

if df["PlacementTraining"].dtype == "object":
    df["PlacementTraining"] = df["PlacementTraining"].replace({
        "Yes": 1,
        "No": 0
    })

# PlacementStatus

if df["PlacementStatus"].dtype == "object":
    df["PlacementStatus"] = df["PlacementStatus"].replace({
        "Placed": 1,
        "NotPlaced": 0
    })

# ==========================================
# FEATURES
# ==========================================

X = df[
    [
        "CGPA",
        "Internships",
        "Projects",
        "PlacementTraining",
        "SSC_Marks",
        "HSC_Marks"
    ]
]

# ==========================================
# TARGET
# ==========================================

y = df["PlacementStatus"]

# ==========================================
# TRAIN TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

# ==========================================
# MODEL
# ==========================================

model = LogisticRegression(max_iter=1000)

model.fit(X_train, y_train)

# ==========================================
# TEST PREDICTION
# ==========================================

y_pred = model.predict(X_test)

# ==========================================
# ACCURACY
# ==========================================

accuracy = accuracy_score(y_test, y_pred)

print("\nAccuracy:")
print(round(accuracy * 100, 2), "%")

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# ==========================================
# PREDICT WHOLE DATASET
# ==========================================

predictions = model.predict(X)

df["Prediction"] = predictions

df["Prediction"] = df["Prediction"].replace({
    1: "Placed",
    0: "NotPlaced"
})

# ==========================================
# COUNTS
# ==========================================

print("\nActual Placement Status Count")

actual_count = df["PlacementStatus"].replace({
    1: "Placed",
    0: "NotPlaced"
}).value_counts()

print(actual_count)

print("\nPredicted Placement Count")

print(df["Prediction"].value_counts())

# ==========================================
# NEW STUDENT PREDICTION
# ==========================================

print("\n--------------------------------")
print("NEW STUDENT PREDICTION")
print("--------------------------------")

new_student = pd.DataFrame(
    [[8.5, 2, 3, 1, 85, 88]],
    columns=[
        "CGPA",
        "Internships",
        "Projects",
        "PlacementTraining",
        "SSC_Marks",
        "HSC_Marks"
    ]
)

prediction = model.predict(new_student)

probability = model.predict_proba(new_student)

if prediction[0] == 1:
    print("\nPrediction : PLACED")
else:
    print("\nPrediction : NOT PLACED")

print(
    "Placement Probability:",
    round(probability[0][1] * 100, 2),
    "%"
)

# ==========================================
# SKILL GAP ANALYSIS
# ==========================================

print("\n--------------------------------")
print("SKILL GAP ANALYSIS")
print("--------------------------------")

cgpa = 6.2
internships = 0
projects = 1
training = 0

if cgpa < 7:
    print("Improve CGPA")

if internships < 1:
    print("Need Internship")

if projects < 2:
    print("Need More Projects")

if training == 0:
    print("Join Placement Training")

# ==========================================
# SAVE REPORT
# ==========================================

df["PlacementStatus"] = df["PlacementStatus"].replace({
    1: "Placed",
    0: "NotPlaced"
})

df.to_excel(
    "Placement_Report.xlsx",
    index=False
)

print("\nPlacement_Report.xlsx Saved Successfully")

# ==========================================
# CLOSE CONNECTION
# ==========================================

conn.close()