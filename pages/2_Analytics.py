import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from style import load_css

# ---------------------------
# CONFIG
# ---------------------------
st.set_page_config(page_title="Risk Analytics", layout="wide")
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
    <h1>📊 Credit Risk Analytics Dashboard</h1>
    <p>Default Probability Breakdown & Early Warning Intelligence</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------
# DATA CHECK
# ---------------------------
if not st.session_state.get("loan_result"):
    st.warning("⚠ Run Risk Assessment first on the Risk Assessment page.")
    st.stop()

data = st.session_state["loan_result"]

# ---------------------------
# COLORS
# ---------------------------
GREEN  = "#2ecc71"
RED    = "#e74c3c"
BLUE   = "#3498db"
ORANGE = "#f39c12"

# ---------------------------
# KPI ROW
# ---------------------------
st.subheader("📌 Borrower Profile Overview")

c1, c2, c3 = st.columns(3)
c1.metric("Annual Income",  format_inr(data["income"]))
c2.metric("Loan Amount",    format_inr(data["loan"]))
c3.metric("Credit Score",   data["credit_score"])

c4, c5, c6 = st.columns(3)
c4.metric("DTI Ratio",      f"{data['dti']:.2f}")
c5.metric("Monthly EMI",    format_inr(data["emi"]))
c6.metric("LTV Ratio",      f"{data.get('ltv', 0):.2f}")

# ---------------------------
# GAUGE SECTION — DTI | PD SCORE | LTV
# ---------------------------
colG1, colG2, colG3 = st.columns(3)

# --- DTI Gauge (unchanged logic) ---
with colG1:
    st.subheader("📉 DTI Gauge")

    fig, ax = plt.subplots(figsize=(3.5, 2))
    dti = data["dti"]
    color_map = {"green": GREEN, "orange": ORANGE, "red": RED}
    color = color_map[get_dti_color(dti)]

    ax.barh(["DTI"], [dti], color=color)
    ax.set_xlim(0, 2)
    ax.text(
        dti / 2, 0, f"{dti:.2f}",
        ha="center", va="center",
        color="black", fontsize=12, fontweight="bold"
    )
    fig.tight_layout()
    st.pyplot(fig, width="content")

# --- PD Score Gauge (replaces Approval Probability) ---
with colG2:
    st.subheader("🎯 Default Probability (PD)")

    pd_score = data.get("pd_score", data["prob"])
    pd_pct   = pd_score * 100

    # Colour: green=low risk, orange=watch, red=high risk (inverted from original)
    if pd_score < 0.10:
        gauge_color = GREEN
    elif pd_score < 0.30:
        gauge_color = ORANGE
    else:
        gauge_color = RED

    fig2, ax2 = plt.subplots(figsize=(3.5, 2))
    ax2.barh(["PD Score"], [pd_pct], color=gauge_color)
    ax2.set_xlim(0, 100)
    ax2.text(
        50, 0, f"{pd_pct:.1f}%",
        ha="center", va="center",
        color="black", fontsize=12, fontweight="bold"
    )
    fig2.tight_layout()
    st.pyplot(fig2, width="content")

# --- LTV Gauge (unchanged logic) ---
with colG3:
    st.subheader("🏠 LTV Gauge")

    ltv = data.get("ltv", 0)
    fig6, ax6 = plt.subplots(figsize=(3.5, 2))
    color = RED if ltv > 0.9 else ORANGE if ltv > 0.7 else GREEN

    ax6.barh(["LTV"], [ltv], color=color)
    ax6.set_xlim(0, 1)
    ax6.text(
        ltv / 3 if ltv > 0 else 0.1, 0, f"{ltv:.2f}",
        ha="center", va="center",
        color="black", fontsize=12, fontweight="bold"
    )
    fig6.tight_layout()
    st.pyplot(fig6, width="content")

# ---------------------------
# RISK BAND DISPLAY (replaces Final Decision block here)
# ---------------------------
st.markdown('<div class="glass">', unsafe_allow_html=True)
st.subheader("📊 Risk Band Summary")

risk_band  = data.get("risk_band", "UNKNOWN")
band_color = data.get("band_color", "grey")

col_rb1, col_rb2, col_rb3 = st.columns(3)
col_rb1.metric("PD Score",        f"{pd_pct:.1f}%")
col_rb2.metric("Risk Band",       risk_band)
col_rb3.metric("Early Warning Flags", len(data.get("early_warning_flags", [])))

if band_color == "green":
    st.success(f"🟢 Final Risk Band: {risk_band} — Low Default Probability")
elif band_color == "orange":
    st.warning(f"🟠 Final Risk Band: {risk_band} — Monitor Closely")
else:
    st.error(f"🔴 Final Risk Band: {risk_band} — Elevated Default Probability")

# Early warning flags summary
flags = data.get("early_warning_flags", [])
if flags:
    st.markdown("#### 🚨 Active Early Warning Signals")
    for flag in flags:
        st.warning(flag)
else:
    st.success("✅ No Early Warning Signals — All Policy Checks Passed")

st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------
# DTI RISK BLOCK (unchanged structure)
# ---------------------------
st.markdown('<div class="glass">', unsafe_allow_html=True)
st.subheader("📌 Debt Serviceability Risk Analysis")

col1, col2 = st.columns([2, 1])

with col1:
    dti_ratio = data["dti"]
    fig3, ax3 = plt.subplots(figsize=(5, 2.8))

    categories = ["Safe Limit", "Your DTI"]
    values     = [0.40, dti_ratio]
    colors     = [
        GREEN,
        GREEN if dti_ratio < 0.3 else ORANGE if dti_ratio < 0.6 else RED
    ]

    bars = ax3.bar(categories, values, color=colors)
    ax3.set_ylim(0, 2)
    ax3.set_title("DTI vs Safe Serviceability Threshold")

    for bar in bars:
        height = bar.get_height()
        ax3.text(
            bar.get_x() + bar.get_width() / 2,
            height + 0.03,
            f"{height:.2f}",
            ha="center", fontsize=11, fontweight="bold"
        )

    fig3.tight_layout()
    st.pyplot(fig3, width="content")

with col2:
    st.markdown("### 🧾 Serviceability Summary")

    if dti_ratio < 0.3:
        st.success("✅ Healthy Debt Serviceability")
        st.info("Low repayment stress — Low default signal")
    elif dti_ratio < 0.6:
        st.warning("⚠️ Moderate Debt Burden")
        st.info("Monitor closely — Watch category signal")
    else:
        st.error("❌ High Debt Burden")
        st.info("Repayment stress — Elevated default risk")

    safe_loan = st.session_state["form_data"].get("safe_loan", 0)
    loan      = st.session_state["form_data"].get("loan", 0)

    st.metric(label="💰 Applied Loan Amount",       value=f"₹{loan / 100000:.2f} Lakh")
    st.metric(label="✅ Max Safe Loan (40% DTI)",    value=f"₹{safe_loan / 100000:.2f} Lakh")

st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------
# EMI VS INCOME + LOAN BURDEN PIE
# ---------------------------
st.markdown('<div class="glass">', unsafe_allow_html=True)

colL, colR = st.columns(2)

monthly_income   = data["income"] / 12 if data["income"] else 0
remaining_income = max(monthly_income - data["emi"], 0)

with colL:
    st.subheader("⚖️ EMI vs Monthly Income")

    fig4, ax4 = plt.subplots(figsize=(4.2, 3.2))
    bars = ax4.bar(
        ["Monthly Income", "Monthly EMI"],
        [monthly_income, data["emi"]],
        color=[GREEN, RED],
        width=0.55
    )

    for bar in bars:
        height = bar.get_height()
        ax4.text(
            bar.get_x() + bar.get_width() / 2,
            height + 800,
            f"₹{height:,.0f}",
            ha="center", fontsize=10, fontweight="bold"
        )

    ax4.spines["top"].set_visible(False)
    ax4.spines["right"].set_visible(False)
    fig4.tight_layout()
    st.pyplot(fig4, width="content")
    plt.savefig("emi_vs_income.png", bbox_inches="tight")

with colR:
    st.subheader("📉 Income Burden Distribution")

    fig5, ax5 = plt.subplots(figsize=(4.2, 3.2))
    ax5.pie(
        [data["emi"], remaining_income],
        labels=["EMI Obligation", "Remaining Income"],
        autopct="%1.1f%%",
        startangle=90,
        radius=0.88,
        colors=[RED, GREEN],
        textprops={"fontsize": 10, "fontweight": "bold"}
    )
    ax5.set_aspect("equal")
    fig5.tight_layout()
    st.pyplot(fig5, width="content")

st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------
# AI DECISION TRANSPARENCY (reframed for PD)
# ---------------------------
st.markdown('<div class="glass">', unsafe_allow_html=True)
st.subheader("🔍 AI Risk Factor Transparency")

# Credit Score signal
if data["credit_score"] > 750:
    st.success("✅ Prime credit tier — Strong default resistance signal")
elif data["credit_score"] >= 650:
    st.info("ℹ Standard credit profile — Moderate default risk contribution")
else:
    st.warning("⚠ Sub-standard credit score — Elevated default probability signal")

plt.savefig("loan_burden.png", bbox_inches="tight")

# DTI signal
if data["dti"] > 0.60:
    st.warning("⚠ High DTI — Debt serviceability breach increases default vulnerability")
elif data["dti"] < 0.30:
    st.success("✅ Low debt burden — Strong repayment capacity, reduces PD")
else:
    st.info("ℹ Moderate debt obligations — Watch for further stress")

# LTV / Collateral signal
if data.get("ltv", 0) > 0:
    if data["ltv"] <= 0.70:
        st.success("🏠 Strong collateral coverage — Reduces Loss-Given-Default (LGD)")
    elif data["ltv"] <= 0.90:
        st.info("ℹ Collateral coverage is acceptable — Moderate LGD exposure")
    else:
        st.warning("⚠ High LTV — Weak collateral buffer amplifies default loss severity")

# Income signal
if data["income"] == 0:
    st.info("📘 Student profile — PD evaluated on co-applicant / guarantor basis")
elif data["income"] < 500000:
    st.warning("⚠ Lower income profile may reduce repayment capacity under stress")
else:
    st.success("💰 Stable income profile — Positive serviceability signal")

# PD Confidence Summary (replaces Approval Confidence)
st.markdown("### 📊 PD Confidence Summary")

if pd_score < 0.10:
    st.success("🟢 Low Default Probability — High confidence in repayment capacity")
elif pd_score < 0.30:
    st.info("🟡 Moderate Default Probability — Enhanced monitoring recommended")
else:
    st.warning("🔴 Elevated Default Probability — Proactive intervention required")

st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------
# STRATEGIC RISK MITIGATION RECOMMENDATIONS
# ---------------------------
st.markdown('<div class="glass">', unsafe_allow_html=True)
st.subheader("🤖 Strategic Risk Mitigation Recommendations")

risk_band = data.get("risk_band", "")

if risk_band == "LOW RISK":
    st.success("✅ Borrower is in LOW RISK band. Standard monitoring applies.")
    st.info("Recommended: Annual review of credit score and DTI. No immediate intervention needed.")

elif risk_band == "WATCH CATEGORY":
    st.warning("🟠 Borrower is in WATCH CATEGORY. Proactive measures recommended.")
    st.markdown("""
- 📉 Encourage partial prepayment to reduce outstanding loan principal
- 💳 Improve credit score through timely repayment of existing obligations
- 📊 Consider restructuring tenure to reduce monthly EMI burden
- 🏠 Obtain additional collateral to strengthen LGD position
- 🔄 Quarterly review cadence recommended
""")

else:
    st.error("🔴 HIGH DEFAULT RISK — Immediate intervention required.")
    st.markdown("""
- 🚨 Initiate Early Warning System (EWS) protocol
- 📋 Request updated income documentation and bank statements
- 🏦 Refer to Credit Risk Committee for enhanced scrutiny
- 🔁 Consider loan restructuring or moratorium options
- 💼 Evaluate personal guarantee or additional co-applicant
- 📞 Assign dedicated relationship manager for monitoring
""")

st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------
# PDF EXPORT
# ---------------------------
st.markdown('<div class="glass">', unsafe_allow_html=True)
st.subheader("📄 Export Default Risk Assessment Report")

st.info(
    "Download an enterprise-grade AI-generated Default Risk Assessment Report "
    "with PD scoring, early warning signals, governance analysis, and risk transparency."
)

from pages.pdf_generator import generate_pdf

if st.button("📥 Generate PDF Risk Report"):
    pdf_data = {
        **st.session_state.get("form_data", {}),
        **data
    }
    pdf_data["applicant_name"] = st.session_state.get("applicant_name", "Unknown Borrower")

    pdf = generate_pdf(pdf_data)

    st.download_button(
        label="⬇ Download Default Risk Report (PDF)",
        data=pdf,
        file_name="FinWithDip_Default_Risk_Assessment.pdf",
        mime="application/pdf"
    )

st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------
# FOOTER
# ---------------------------
st.markdown("---")
st.caption("© 2026 FinWithDip | Enterprise Credit Risk & Early Warning Platform | Developed by Subhadip | IDBI Innovate 2026 — Track 4")
