# Dataset Information

## Required File
Place your dataset here as `loan_data.csv` (or the root `loan_dataset.csv` will be used automatically).

## Required Columns
| Column              | Type        | Description                          |
|---------------------|-------------|--------------------------------------|
| Loan_ID             | string      | Unique identifier (will be dropped)  |
| Gender              | categorical | Male / Female                        |
| Married             | categorical | Yes / No                             |
| Dependents          | categorical | 0 / 1 / 2 / 3+                       |
| Education           | categorical | Graduate / Not Graduate              |
| Self_Employed       | categorical | Yes / No                             |
| ApplicantIncome     | numeric     | Monthly income of applicant          |
| CoapplicantIncome   | numeric     | Monthly income of co-applicant       |
| LoanAmount          | numeric     | Loan amount requested                |
| Loan_Amount_Term    | numeric     | Term of loan in months               |
| Credit_History      | numeric     | 1 = good history, 0 = bad            |
| Property_Area       | categorical | Urban / Semiurban / Rural            |
| Loan_Status         | categorical | Y (Approved) / N (Rejected)          |

## Where to Download
- Kaggle: https://www.kaggle.com/datasets/altruistdelhite04/loan-prediction-problem-dataset
- Or use the included `loan_dataset.csv` in the root of this repository.

## After Placing the Dataset
```bash
cd backend
python model_train.py
```
This will generate `backend/loan_model.pkl` which the Flask API uses.
