import streamlit as st
import pandas as pd
import pickle
import os
from style import load_css

# ---------------------------
# CONFIG + CSS
# ---------------------------
st.set_page_config(page_title="Risk Assessment", layout="wide")
load_css(st)

# ---------------------------
# HELPERS
# ---------------------------
def format_inr(x):
    if x >= 100000:
        return f"₹{x/100000:.2f} Lakh"
    return f"₹{x:,.0f}"

def get_dti_color(dti):
    if dti < 0.3:
        return "green"
    elif dti < 0.5:
        return "orange"
    else:
        return "red"

def get_pd_band(pd_score):
    """Classify PD score into risk band."""
    if pd_score < 0.10:
        return "LOW RISK", "green"
    elif pd_score < 0.30:
        return "WATCH CATEGORY", "orange"
    else:
        return "HIGH DEFAULT RISK", "red"

# ---------------------------
# SESSION STATE
# ---------------------------
if "form_data" not in st.session_state:
    st.session_state["form_data"] = {
        "age": 0,
        "employment": "",
        "loan_type": "",
        "income": 0.0,
        "loan": 0.0,
        "asset": 0.0,
        "credit": 0,
        "interest": None,
        "years": None
    }

# ---------------------------
# LOAD MODEL
# ---------------------------
base_path = os.path.dirname(__file__)
model_path = os.path.join(base_path, "..", "model", "model.pkl")

if os.path.exists(model_path):
    model = pickle.load(open(model_path, "rb"))
else:
    st.error("❌ Model file not found. Check /model folder.")
    st.stop()

# ---------------------------
# SIDEBAR LOGO
# ---------------------------
st.sidebar.image("financelogo.png", width=220)
st.sidebar.markdown("<br>", unsafe_allow_html=True)

# ---------------------------
# SIDEBAR NAV
# ---------------------------
st.sidebar.markdown("## 📍 System Menu")
st.sidebar.page_link("app.py", label="🏠 Home")
st.sidebar.page_link("pages/1_Decision.py", label="🔬 Risk Assessment")
st.sidebar.page_link("pages/2_Analytics.py", label="📊 Analytics")

# ---------------------------
# HEADER
# ---------------------------
st.markdown("""
<div class="glass header-glass">
    <h1>🔬 Credit Risk Assessment</h1>
    <p>AI-Powered Probability of Default & Early Warning System</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------
# INPUT SECTION
# ---------------------------
st.markdown('<div class="glass">', unsafe_allow_html=True)
error_box = st.empty()

col1, col2 = st.columns(2)

with col1:
    applicant_name = st.text_input(
        "Borrower Name (Optional — shown in PDF report)",
        value=st.session_state.get("applicant_name", ""),
        placeholder="Enter Borrower Name",
        key="applicant_name_input"
    )
    st.session_state["applicant_name"] = applicant_name

    age = st.number_input(
        "Age",
        min_value=18,
        max_value=75,
        value=(
            st.session_state["form_data"]["age"]
            if st.session_state["form_data"]["age"] != 0
            else None
        ),
        step=1,
        placeholder="Enter borrower age",
        key="age_input"
    )

    employment = st.selectbox(
        "Employment Status",
        ["Employed", "Self-employed", "Unemployed"]
    )

    loan_type = st.selectbox(
        "Loan Type",
        ["Personal", "Education"]
    )

    credit_score = st.number_input(
        "Credit Score (300–900)",
        min_value=300,
        max_value=900,
        value=(
            st.session_state["form_data"]["credit"]
            if st.session_state["form_data"]["credit"] != 0
            else None
        ),
        step=1,
        placeholder="Enter Credit Score",
        key="credit_input"
    )

with col2:
    annual_income = st.number_input(
        "Annual Income (₹)",
        min_value=0.0,
        value=(
            st.session_state["form_data"]["income"]
            if st.session_state["form_data"]["income"] != 0.0
            else None
        ),
        step=1000.0,
        placeholder="Enter Annual Income",
        key="income_input"
    )
    if annual_income:
        st.caption(f"💰 {format_inr(annual_income)}")

    loan_amount = st.number_input(
        "Loan Amount (₹)",
        min_value=0.0,
        value=(
            st.session_state["form_data"]["loan"]
            if st.session_state["form_data"]["loan"] != 0.0
            else None
        ),
        step=1000.0,
        placeholder="Enter Loan Amount",
        key="loan_input"
    )
    if loan_amount:
        st.caption(f"💰 {format_inr(loan_amount)}")

    asset_value = st.number_input(
        "Asset / Property Value (₹)",
        min_value=0.0,
        value=(
            st.session_state["form_data"]["asset"]
            if st.session_state["form_data"]["asset"] != 0.0
            else None
        ),
        step=10000.0,
        placeholder="Enter Asset / Property Value",
        key="asset_input"
    )
    if asset_value:
        st.caption(f"🏠 {format_inr(asset_value)}")

st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------
# LOAN CALCULATION
# ---------------------------
st.markdown('<div class="glass">', unsafe_allow_html=True)

st.subheader("📊 EMI & Debt Serviceability Calculation")

if "interest_input" not in st.session_state:
    st.session_state["interest_input"] = None

if "years_input" not in st.session_state:
    st.session_state["years_input"] = st.session_state["form_data"].get("years")

tenure_years = st.number_input(
    "Loan Tenure (Years)",
    min_value=1,
    max_value=30,
    step=1,
    placeholder="Enter Loan Tenure",
    key="years_input"
)
st.markdown(
    "<p style='margin-top:-10px; font-size:13px; color:gray;'>(Longer tenure reduces EMI and lowers DTI stress)</p>",
    unsafe_allow_html=True
)

interest_rate = st.number_input(
    "Interest Rate (%)",
    min_value=0.0,
    value=st.session_state["interest_input"],
    step=0.01,
    placeholder="Enter Interest Rate",
    key="interest_widget"
)

st.session_state["form_data"]["years"] = tenure_years
st.session_state["form_data"]["interest"] = interest_rate
st.session_state["form_data"]["employment"] = employment
st.session_state["interest_input"] = interest_rate

emi = None
dti = None
monthly_income = None
ltv = None
monthly_rate = None
months = None

if (
    loan_amount and loan_amount > 0
    and interest_rate and interest_rate > 0
    and tenure_years and tenure_years > 0
):
    interest_rate_dec = interest_rate / 100
    monthly_rate = interest_rate_dec / 12
    months = tenure_years * 12

    emi = (loan_amount * monthly_rate * (1 + monthly_rate) ** months) / (
        (1 + monthly_rate) ** months - 1
    )

    if annual_income and annual_income > 0:
        monthly_income = annual_income / 12
        dti = emi / monthly_income
        st.info(f"📊 EMI: {format_inr(emi)} | DTI Ratio: {dti:.2f}")
    else:
        st.info(f"📊 EMI: {format_inr(emi)} | Student Profile (No Income)")

    if asset_value and asset_value > 0:
        ltv = loan_amount / asset_value
        st.info(f"🏠 LTV Ratio: {ltv:.2f}")
else:
    st.warning("Enter loan amount, interest rate & tenure to calculate EMI")

st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------
# PREDICTION
# ---------------------------
st.markdown('<div class="glass">', unsafe_allow_html=True)
bottom_error_box = st.empty()

if st.button("🔬 Generate PD Score & Risk Assessment"):
    st.session_state["predicted"] = True

if st.session_state.get("predicted"):

    # ---------------------------
    # VALIDATION
    # ---------------------------
    errors = []

    if age is None or age <= 0:
        errors.append("Enter valid age")
    if annual_income is None or annual_income <= 0:
        errors.append("Enter valid annual income")
    if loan_amount is None or loan_amount <= 0:
        errors.append("Enter valid loan amount")
    if credit_score is None:
        errors.append("Enter credit score")
    if interest_rate is None:
        errors.append("Enter interest rate")
    if tenure_years is None:
        errors.append("Enter loan tenure")

    if errors:
        message = "⚠ " + " | ".join(errors)
        error_box.error(message)
        bottom_error_box.error(message)
        st.stop()

    # ---------------------------
    # SAVE FORM STATE
    # ---------------------------
    st.session_state["form_data"] = {
        "age": age,
        "income": annual_income,
        "loan": loan_amount,
        "asset": asset_value,
        "credit": credit_score,
        "interest": interest_rate,
        "years": tenure_years
    }

    # ---------------------------
    # MODEL INPUT
    # NOTE: model.predict_proba()[0][1] gives P(class=1).
    # Original model was trained on loan_paid_back (1=paid).
    # We invert: PD = 1 - P(paid back) to get default probability.
    # ---------------------------
    model_income = annual_income if annual_income and annual_income > 0 else 1

    data = pd.DataFrame(
        [[model_income, loan_amount, credit_score]],
        columns=["annual_income", "loan_amount", "credit_score"]
    )

    prob_paid = model.predict_proba(data)[0][1]
    pd_score = 1 - prob_paid  # Probability of Default

    # ---------------------------
    # PD BAND CLASSIFICATION
    # ---------------------------
    risk_band, band_color = get_pd_band(pd_score)

    # ---------------------------
    # EARLY WARNING GOVERNANCE
    # ---------------------------
    early_warning_flags = []

    if credit_score < 550:
        early_warning_flags.append("⚠ Critical Credit Score breach (<550) — High Default Signal")
    elif credit_score < 650:
        early_warning_flags.append("⚠ Weak Credit Score (<650) — Elevated Default Risk")

    if dti is not None and dti > 0.75:
        early_warning_flags.append("⚠ Severe DTI breach (>0.75) — Debt Serviceability Failure")
    elif dti is not None and dti > 0.50:
        early_warning_flags.append("⚠ High DTI (>0.50) — Repayment Stress Detected")

    if employment == "Unemployed" and dti is not None and dti > 0.60:
        early_warning_flags.append("⚠ Unemployed borrower with high DTI — Cash Flow Risk")

    if ltv is not None and ltv > 0.90:
        early_warning_flags.append("⚠ LTV >0.90 — Weak Collateral Coverage")

    # Governance override: escalate risk band if critical flags present
    critical_flags = [f for f in early_warning_flags if "Critical" in f or "Severe" in f or "Failure" in f]

    if critical_flags:
        if risk_band == "LOW RISK":
            risk_band = "WATCH CATEGORY"
            band_color = "orange"

    # Collateral override: strong collateral can moderate WATCH → LOW
    if ltv is not None and ltv <= 0.70 and credit_score >= 650 and not critical_flags:
        if risk_band == "WATCH CATEGORY":
            risk_band = "LOW RISK"
            band_color = "green"
            st.success("🏠 Strong collateral (LTV ≤ 0.70) moderated risk band to LOW RISK")

    # ---------------------------
    # SAVE RESULT TO SESSION
    # ---------------------------
    st.session_state["loan_result"] = {
        "income": annual_income,
        "loan": loan_amount,
        "credit_score": credit_score,
        "dti": dti if dti else 0,
        "emi": emi if emi else 0,
        "ltv": ltv if ltv else 0,
        "pd_score": pd_score,
        "prob": pd_score,
        "decision": 0 if risk_band == "HIGH DEFAULT RISK" else 1,
        "risk_band": risk_band,
        "band_color": band_color,
        "early_warning_flags": early_warning_flags,
        "loan_type": loan_type,
        "employment": employment
    }

    # ---------------------------
    # EARLY WARNING GOVERNANCE CHECK
    # ---------------------------
    st.markdown("## 🛡️ Early Warning Governance Check")

    gov1, gov2 = st.columns(2)

    with gov1:
        st.markdown("### 🤖 AI PD Model")
        pd_pct = pd_score * 100
        if pd_score < 0.10:
            st.success(f"PD Score: {pd_pct:.1f}% — Low Default Risk")
        elif pd_score < 0.30:
            st.warning(f"PD Score: {pd_pct:.1f}% — Watch Category")
        else:
            st.error(f"PD Score: {pd_pct:.1f}% — High Default Risk")

    with gov2:
        st.markdown("### 🏦 Policy Governance")
        if early_warning_flags:
            st.error(f"{len(early_warning_flags)} Early Warning Flag(s) Triggered")
        else:
            st.success("All Policy Checks Passed")

    if early_warning_flags:
        st.markdown("#### 🚨 Early Warning Signals Detected")
        for flag in early_warning_flags:
            st.warning(flag)

    # ---------------------------
    # FINAL RISK BAND
    # ---------------------------
    st.markdown("## 📊 Final Risk Assessment")

    if band_color == "green":
        st.success(f"🟢 Risk Band: {risk_band}")
    elif band_color == "orange":
        st.warning(f"🟠 Risk Band: {risk_band}")
    else:
        st.error(f"🔴 Risk Band: {risk_band}")

    col_pd_a, col_pd_b, col_pd_c = st.columns(3)
    col_pd_a.metric("PD Score", f"{pd_score * 100:.1f}%")
    col_pd_b.metric("Risk Band", risk_band)
    col_pd_c.metric("Early Warning Flags", len(early_warning_flags))

    # ---------------------------
    # AI RISK FACTOR BREAKDOWN
    # ---------------------------
    st.markdown("## 🔍 AI Risk Factor Breakdown")

    safe_credit = credit_score if credit_score is not None else 300
    safe_dti = dti if dti is not None else 1
    safe_ltv = ltv if ltv is not None else 1

    risk_impacts = {
        "Credit Risk":
            ((600 - min(safe_credit, 600)) / 300) * 40,
        "Debt Burden":
            min(safe_dti, 1) * 30,
        "Collateral Gap":
            min(safe_ltv, 1) * 20,
        "Income Instability":
            10 if employment == "Unemployed" else 2
    }

    impact_df = pd.DataFrame(
        list(risk_impacts.items()),
        columns=["Risk Factor", "Risk Contribution Score"]
    )

    col_exp1, col_exp2 = st.columns([1.7, 1])

    with col_exp1:
        st.bar_chart(
            impact_df.set_index("Risk Factor"),
            color="#e74c3c",
            height=250
        )

    with col_exp2:
        st.markdown("### 🧠 Top Default Driver")
        top_factor = max(risk_impacts, key=risk_impacts.get)
        st.error(
            f"**{top_factor}** is the strongest default risk contributor for this borrower profile."
        )

    # ---------------------------
    # WHAT-IF: PD REDUCTION SIMULATION
    # ---------------------------
    if risk_band != "LOW RISK" and dti is not None and monthly_rate and months:

        st.markdown("## 🔮 PD Reduction Simulation — What-If Engine")
        st.info("Adjust income or loan amount to simulate how the borrower can reduce default probability.")

        colA, colB = st.columns(2)

        with colA:
            new_income = st.slider(
                "Simulate Income Increase (₹)",
                int(annual_income or 0),
                int((annual_income or 100000) * 2),
                int(annual_income or 0)
            )

        with colB:
            new_loan = st.slider(
                "Simulate Loan Reduction (₹)",
                10000,
                int(loan_amount),
                int(loan_amount)
            )

        if new_income > 0:
            new_monthly_income = new_income / 12
            new_emi = (
                new_loan * monthly_rate * (1 + monthly_rate) ** months
            ) / (
                (1 + monthly_rate) ** months - 1
            )
            new_dti = new_emi / new_monthly_income
            dti_reduction_factor = max(0, (dti - new_dti) / dti) if dti > 0 else 0
            simulated_pd = max(0.01, pd_score * (1 - dti_reduction_factor * 0.6))
            sim_band, _ = get_pd_band(simulated_pd)

            st.markdown("#### 📉 Simulated Outcome")
            col_sim1, col_sim2, col_sim3 = st.columns(3)
            col_sim1.metric("New DTI", f"{new_dti:.2f}", delta=f"{new_dti - dti:.2f}")
            col_sim2.metric("Simulated PD", f"{simulated_pd * 100:.1f}%", delta=f"{(simulated_pd - pd_score) * 100:.1f}%")
            col_sim3.metric("Simulated Band", sim_band)

            if sim_band == "LOW RISK":
                st.success("✅ This scenario moves the borrower to LOW RISK band")
            elif sim_band == "WATCH CATEGORY":
                st.warning("🟠 Still in Watch Category — further reduction recommended")
            else:
                st.error("🔴 Still High Risk — significant financial restructuring needed")

    # ---------------------------
    # RISK ANALYSIS
    # ---------------------------
    st.markdown("## ⚠️ Borrower Risk Analysis")

    if dti is not None:
        risk_color = get_dti_color(dti)
        if risk_color == "green":
            st.success("🟢 Healthy Debt Serviceability — Low Repayment Stress")
        elif risk_color == "orange":
            st.warning("🟠 Moderate Debt Burden — Monitor Closely")
        else:
            st.error("🔴 High Debt Burden — Default Vulnerability Elevated")

    if credit_score > 750:
        st.success("💳 Prime Credit Tier — Strong Default Resistance")
    elif credit_score > 650:
        st.info("💳 Standard Credit Profile — Moderate Default Risk")
    else:
        st.warning("💳 Sub-Standard Credit — High Default Probability")

    # ---------------------------
    # EDUCATION LOAN INSIGHTS
    # ---------------------------
    if loan_type == "Education":
        st.markdown("## 🎓 Education Loan Risk Insights")
        if annual_income == 0:
            st.info("📘 Student profile — PD assessed on co-applicant/guarantor basis")
        if credit_score < 600:
            st.warning("Co-applicant with strong credit profile recommended")
        if loan_amount > 2000000:
            st.warning("High loan quantum — collateral requirement likely")
        st.success("Future earning potential factored into long-term PD assessment")

    # ---------------------------
    # STRATEGIC RISK INSIGHTS
    # ---------------------------
    st.markdown("## 🤖 Strategic Risk Intelligence")

    strengths = []
    mitigations = []

    if credit_score > 750:
        strengths.append("Prime Credit Tier: Strong historical repayment signal.")
    if dti is not None and dti < 0.3:
        strengths.append("Healthy Debt Serviceability: Low repayment stress detected.")
    if loan_type == "Education":
        strengths.append("Education loan: Future income potential reduces long-term PD.")
    if ltv is not None and ltv <= 0.7:
        strengths.append("Strong collateral coverage reduces Loss-Given-Default (LGD).")

    if annual_income and loan_amount > annual_income * 1.5:
        mitigations.append("Loan-to-Income overextension: Exceeds safe multiplier threshold.")
    if employment == "Unemployed" and loan_type != "Education":
        mitigations.append("No stable income source: Cash flow default risk elevated.")
    if dti is not None and dti > 0.5:
        mitigations.append("High DTI: Debt serviceability under stress — restructure recommended.")
    if pd_score > 0.30:
        mitigations.append("PD >30%: Consider enhanced monitoring or collateral enhancement.")

    pos_col, risk_col = st.columns(2)

    with pos_col:
        st.markdown("### ✅ Risk Mitigants")
        if strengths:
            for s in strengths:
                st.success(s)
        else:
            st.info("No significant risk mitigants detected.")

    with risk_col:
        st.markdown("### ⚠️ Default Risk Factors")
        if mitigations:
            for m in mitigations:
                st.warning(m)
        else:
            st.success("No critical default risk factors identified.")

    # ---------------------------
    # MAXIMUM SAFE LOAN ESTIMATION
    # ---------------------------
    if monthly_income and monthly_rate and months:
        max_emi = monthly_income * 0.4
        estimated_safe_loan = (
            max_emi * ((1 + monthly_rate) ** months - 1)
        ) / (
            monthly_rate * (1 + monthly_rate) ** months
        )
        st.session_state["form_data"]["safe_loan"] = estimated_safe_loan
        st.success(
            f"💰 Maximum Safe Loan (40% DTI Ceiling): {format_inr(estimated_safe_loan)}"
        )

    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.page_link("pages/2_Analytics.py", label="➡ View Risk Analytics")

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------
# FOOTER
# ---------------------------
st.markdown("---")
st.caption("© 2026 FinWithDip | Enterprise Credit Risk & Early Warning Platform | Developed by Subhadip | IDBI Innovate 2026 — Track 4")
