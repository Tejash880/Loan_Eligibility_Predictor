import os
import pickle
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "loan_model.pkl")

model = None
if os.path.exists(MODEL_PATH):
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)

def preprocess_input(data):
    gender = 1 if data.get("Gender") == "Male" else 0
    married = 1 if data.get("Married") == "Yes" else 0
    dependents_map = {"0": 0, "1": 1, "2": 2, "3+": 3}
    dependents = dependents_map.get(str(data.get("Dependents", "0")), 0)
    education = 1 if data.get("Education") == "Graduate" else 0
    self_employed = 1 if data.get("Self_Employed") == "Yes" else 0
    applicant_income = float(data.get("ApplicantIncome", 0))
    coapplicant_income = float(data.get("CoapplicantIncome", 0))
    loan_amount = float(data.get("LoanAmount", 0))
    loan_term = float(data.get("Loan_Amount_Term", 360))
    credit_history = float(data.get("Credit_History", 1))
    property_area_map = {"Rural": 0, "Semiurban": 1, "Urban": 2}
    property_area = property_area_map.get(data.get("Property_Area", "Urban"), 2)

    total_income = applicant_income + coapplicant_income
    income_loan_ratio = total_income / loan_amount if loan_amount > 0 else 0
    loan_term_ratio = loan_amount / loan_term if loan_term > 0 else 0

    features = [
        gender, married, dependents, education, self_employed,
        applicant_income, coapplicant_income, loan_amount, loan_term,
        credit_history, property_area, total_income, income_loan_ratio, loan_term_ratio
    ]
    return np.array(features).reshape(1, -1)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "model_loaded": model is not None})


@app.route("/predict", methods=["POST"])
def predict():
    if model is None:
        return jsonify({"error": "Model not loaded. Please train the model first."}), 503

    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400

    try:
        features = preprocess_input(data)
        prediction = model.predict(features)[0]
        probabilities = model.predict_proba(features)[0]

        result = "Approved" if prediction == 1 else "Rejected"
        confidence = round(float(max(probabilities)) * 100, 2)
        approved_prob = round(float(probabilities[1]) * 100, 2)
        rejected_prob = round(float(probabilities[0]) * 100, 2)

        return jsonify({
            "prediction": result,
            "confidence": confidence,
            "probability": {
                "approved": approved_prob,
                "rejected": rejected_prob
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
