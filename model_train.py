import os
import pickle
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder

# Both dataset and model saved in same root directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.join(BASE_DIR, "loan_dataset.csv")
MODEL_PATH = os.path.join(BASE_DIR, "loan_model.pkl")

def load_and_preprocess(path):
    df = pd.read_csv(path)
    print(f"Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")

    if "Loan_ID" in df.columns:
        df.drop("Loan_ID", axis=1, inplace=True)

    for col in df.select_dtypes(include="object").columns:
        df[col].fillna(df[col].mode()[0], inplace=True)
    for col in df.select_dtypes(include="number").columns:
        df[col].fillna(df[col].median(), inplace=True)

    le = LabelEncoder()
    cat_cols = df.select_dtypes(include="object").columns.tolist()
    if "Loan_Status" in cat_cols:
        cat_cols.remove("Loan_Status")
    for col in cat_cols:
        df[col] = le.fit_transform(df[col])

    df["Loan_Status"] = df["Loan_Status"].map({"Y": 1, "N": 0})

    df["Total_Income"] = df["ApplicantIncome"] + df["CoapplicantIncome"]
    df["Income_Loan_Ratio"] = df["Total_Income"] / (df["LoanAmount"] + 1)
    df["Loan_Term_Ratio"] = df["LoanAmount"] / (df["Loan_Amount_Term"] + 1)

    return df

def train():
    df = load_and_preprocess(DATASET_PATH)

    feature_cols = [
        "Gender", "Married", "Dependents", "Education", "Self_Employed",
        "ApplicantIncome", "CoapplicantIncome", "LoanAmount", "Loan_Amount_Term",
        "Credit_History", "Property_Area", "Total_Income", "Income_Loan_Ratio", "Loan_Term_Ratio"
    ]
    feature_cols = [c for c in feature_cols if c in df.columns]

    X = df[feature_cols]
    y = df["Loan_Status"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        min_samples_split=10,
        min_samples_leaf=4,
        random_state=42
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    cv_scores = cross_val_score(model, X, y, cv=5)

    print(f"\n✅ Training Accuracy: {model.score(X_train, y_train)*100:.2f}%")
    print(f"✅ Testing Accuracy:  {acc*100:.2f}%")
    print(f"✅ Cross-Val Mean:    {cv_scores.mean()*100:.2f}% ± {cv_scores.std()*100:.2f}%")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=["Rejected", "Approved"]))

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)
    print(f"\n✅ Model saved to: {MODEL_PATH}")

if __name__ == "__main__":
    train()
