// ⚠️ Change this to your deployed backend URL when live
const API_URL = "https://your-backend.onrender.com";

let lastResult = null;

async function predict() {
  const btn = document.getElementById("predictBtn");
  const btnText = document.getElementById("btnText");
  const btnLoader = document.getElementById("btnLoader");
  const errorBox = document.getElementById("errorBox");
  const resultCard = document.getElementById("resultCard");

  // Hide previous results
  resultCard.classList.add("hidden");
  errorBox.classList.add("hidden");

  // Validate inputs
  const applicantIncome = parseFloat(document.getElementById("ApplicantIncome").value);
  const loanAmount = parseFloat(document.getElementById("LoanAmount").value);

  if (!applicantIncome || applicantIncome <= 0) {
    showError("Please enter a valid Applicant Income.");
    return;
  }
  if (!loanAmount || loanAmount <= 0) {
    showError("Please enter a valid Loan Amount.");
    return;
  }

  // Loading state
  btn.disabled = true;
  btnText.classList.add("hidden");
  btnLoader.classList.remove("hidden");

  const payload = {
    Gender: document.getElementById("Gender").value,
    Married: document.getElementById("Married").value,
    Dependents: document.getElementById("Dependents").value,
    Education: document.getElementById("Education").value,
    Self_Employed: document.getElementById("Self_Employed").value,
    ApplicantIncome: applicantIncome,
    CoapplicantIncome: parseFloat(document.getElementById("CoapplicantIncome").value) || 0,
    LoanAmount: loanAmount,
    Loan_Amount_Term: parseFloat(document.getElementById("Loan_Amount_Term").value),
    Credit_History: parseFloat(document.getElementById("Credit_History").value),
    Property_Area: document.getElementById("Property_Area").value
  };

  try {
    const response = await fetch(`${API_URL}/predict`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      const err = await response.json();
      throw new Error(err.error || "Server error");
    }

    const data = await response.json();
    lastResult = { ...data, input: payload };
    showResult(data, payload);

  } catch (err) {
    showError(err.message || "Could not connect to the server. Make sure the backend is running.");
  } finally {
    btn.disabled = false;
    btnText.classList.remove("hidden");
    btnLoader.classList.add("hidden");
  }
}

function showResult(data, input) {
  const approved = data.prediction === "Approved";

  document.getElementById("resultIcon").textContent = approved ? "✅" : "❌";
  document.getElementById("resultTitle").textContent = `Loan ${data.prediction}`;
  document.getElementById("resultTitle").style.color = approved ? "#22c55e" : "#ef4444";
  document.getElementById("resultConfidence").textContent =
    `Model confidence: ${data.confidence}%`;

  document.getElementById("pctApproved").textContent = `${data.probability.approved}%`;
  document.getElementById("pctRejected").textContent = `${data.probability.rejected}%`;

  // Animate bars after render
  setTimeout(() => {
    document.getElementById("barApproved").style.width = `${data.probability.approved}%`;
    document.getElementById("barRejected").style.width = `${data.probability.rejected}%`;
  }, 100);

  // Summary
  const totalIncome = input.ApplicantIncome + input.CoapplicantIncome;
  const ratio = (totalIncome / input.LoanAmount).toFixed(2);
  document.getElementById("summary").innerHTML = `
    <strong>📊 Summary</strong><br/>
    Total Income: ₹${totalIncome.toLocaleString()}/month &nbsp;|&nbsp;
    Loan Amount: ₹${input.LoanAmount.toLocaleString()}<br/>
    Income-to-Loan Ratio: ${ratio} &nbsp;|&nbsp;
    Credit History: ${input.Credit_History == 1 ? "✅ Good" : "❌ Bad"}<br/>
    Property Area: ${input.Property_Area} &nbsp;|&nbsp;
    Education: ${input.Education}
  `;

  document.getElementById("resultCard").classList.remove("hidden");
  document.getElementById("resultCard").scrollIntoView({ behavior: "smooth" });
}

function showError(msg) {
  document.getElementById("errorMsg").textContent = msg;
  document.getElementById("errorBox").classList.remove("hidden");
}

function resetForm() {
  document.getElementById("resultCard").classList.add("hidden");
  document.getElementById("errorBox").classList.add("hidden");
  document.getElementById("ApplicantIncome").value = "";
  document.getElementById("CoapplicantIncome").value = "0";
  document.getElementById("LoanAmount").value = "";
  document.getElementById("barApproved").style.width = "0";
  document.getElementById("barRejected").style.width = "0";
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function downloadReport() {
  if (!lastResult) return;
  const d = lastResult;
  const i = d.input;
  const text = `
===========================
   LoanIQ - Prediction Report
===========================
Date     : ${new Date().toLocaleString()}
Result   : ${d.prediction}
Confidence: ${d.confidence}%

--- Applicant Details ---
Gender         : ${i.Gender}
Married        : ${i.Married}
Dependents     : ${i.Dependents}
Education      : ${i.Education}
Self Employed  : ${i.Self_Employed}
Property Area  : ${i.Property_Area}
Credit History : ${i.Credit_History == 1 ? "Good" : "Bad"}

--- Financials ---
Applicant Income  : ₹${i.ApplicantIncome.toLocaleString()}
Co-applicant Income: ₹${i.CoapplicantIncome.toLocaleString()}
Total Income      : ₹${(i.ApplicantIncome + i.CoapplicantIncome).toLocaleString()}
Loan Amount       : ₹${i.LoanAmount.toLocaleString()}
Loan Term         : ${i.Loan_Amount_Term} months

--- Probabilities ---
Approved : ${d.probability.approved}%
Rejected : ${d.probability.rejected}%

===========================
   Generated by LoanIQ
===========================
`.trim();

  const blob = new Blob([text], { type: "text/plain" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "LoanIQ_Report.txt";
  a.click();
  URL.revokeObjectURL(url);
}
