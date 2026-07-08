import streamlit as st
from style import load_css

# ---------------------------
# CONFIG + CSS
# ---------------------------
st.set_page_config(page_title="FinWithDip | Credit Risk Platform", layout="wide")
load_css(st)

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
    <h1>🛡️ FinWithDip | Enterprise Credit Risk Platform</h1>
    <p>AI-Powered Probability of Default & Early Warning Risk Intelligence System</p>
</div>
""", unsafe_allow_html=True)

# ---------------------------
# INTRO
# ---------------------------
st.markdown('<div class="glass">', unsafe_allow_html=True)

st.markdown("### 📘 What is this Platform?")

st.info("""
This platform operationalises **IDBI Innovate 2026 — Problem Statement 4: Default Prediction Model**
through a Hybrid AI Risk Intelligence Framework:

1. **PD Scoring** → Machine Learning estimates the Probability of Default for each borrower
2. **Early Warning Engine** → Banking risk policies flag elevated default signals (Credit Score, DTI, LTV)
3. **Risk Advisory** → 'What-If Engine' simulates risk reduction scenarios for proactive intervention

💡 Decisions are not just AI-driven — they are validated through institutional risk governance rules.
""")

st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------
# WHAT IS PD?
# ---------------------------
st.markdown('<div class="glass">', unsafe_allow_html=True)

st.markdown("### 🎯 What is Probability of Default (PD)?")

st.write("""
**Probability of Default (PD)** is a core metric in credit risk management that estimates
the likelihood that a borrower will fail to meet their loan repayment obligations
within a defined time horizon (typically 12 months).

PD is a foundational component of the **Basel III / RBI regulatory framework** used by
Indian banks including IDBI Bank to compute:
""")

col_pd1, col_pd2 = st.columns(2)

with col_pd1:
    st.success("""
✔ **Credit Risk Capital (CRAR)**
✔ **Expected Credit Loss (ECL)**
✔ **Loan Loss Provisioning**
✔ **Risk-Weighted Assets (RWA)**
""")

with col_pd2:
    st.info("""
📊 **PD Risk Bands:**

🟢 PD < 10% → Low Risk
🟠 PD 10–30% → Watch Category
🔴 PD > 30% → High Default Risk
""")

st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------
# PLATFORM CAPABILITIES
# ---------------------------
st.markdown('<div class="glass">', unsafe_allow_html=True)

st.markdown("### 🚀 Platform Capabilities")

colA, colB = st.columns(2)

with colA:
    st.markdown("#### 🛡️ Risk Intelligence")

    st.write("● **PD Scoring Engine:** AI-driven default probability estimation")
    st.write("● **Early Warning Triggers:** Credit Score, DTI & LTV breach detection")
    st.write("● **Compliance Logic:** Final risk band governed by RBI-aligned policy rules")
    st.write("● **Risk Governance Engine:** AI + institutional policy validation")
    st.write("● **Risk Classification:** Low / Watch / High Default Risk segmentation")

with colB:
    st.markdown("#### 📈 Credit Advisory")

    st.write("● **Scenario Analysis:** Dynamic 'What-If' PD reduction simulations")
    st.write("● **Actionable Insights:** Understand default risk drivers")
    st.write("● **Optimization Engine:** Strategies to improve borrower risk profile")
    st.write("● **AI Transparency Layer:** Decision explanation & top risk drivers")
    st.write("● **Executive PDF Reporting:** Enterprise-grade risk intelligence reports")

st.markdown("---")

st.markdown("#### 🧭 Core System Workflow")

st.markdown("""
1. **[PD Scoring Engine]** → Multi-factor default probability estimation
2. **[Early Warning Layer]** → Credit Score, DTI & LTV breach detection
3. **[Risk Intelligence]** → AI transparency & risk factor breakdown
4. **[Financial Advisory Engine]** → PD reduction simulations & recommendations
5. **[Analytics Dashboard]** → Risk visualisation & affordability analysis
6. **[Enterprise PDF Generator]** → Official default risk assessment report
""")

st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------
# CREDIT SCORE
# ---------------------------
st.markdown('<div class="glass">', unsafe_allow_html=True)

st.markdown("### 💳 Credit Score & Default Risk")

st.write("""
A Credit Score (300–900) is the primary predictor of default probability.

- Repayment history
- Credit card utilisation
- Existing loan obligations
- Credit enquiry frequency
""")

st.success("""
✔ 750+ → Low Default Risk
✔ 650–750 → Moderate Watch
✔ <650 → Elevated Default Risk
""")

st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------
# DTI
# ---------------------------
st.markdown('<div class="glass">', unsafe_allow_html=True)

st.markdown("### 📊 DTI Ratio — Debt Serviceability Indicator")

st.write("DTI measures the proportion of monthly income consumed by loan repayment — a core default signal.")

st.latex(r"DTI = \frac{Monthly\ EMI}{Monthly\ Income}")

st.info("""
✔ DTI < 0.30 → Healthy Serviceability
✔ DTI 0.30–0.50 → Moderate Stress
✔ DTI > 0.50 → High Default Vulnerability
""")

st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------
# EMI
# ---------------------------
st.markdown('<div class="glass">', unsafe_allow_html=True)

st.markdown("### 💰 EMI & Repayment Capacity")

st.write("""
EMI is the fixed monthly repayment obligation. Higher EMI relative to income
directly elevates DTI and therefore the Probability of Default.

Depends on:
- Loan amount
- Interest rate
- Loan tenure
""")

st.latex(r"EMI = \frac{P \cdot r \cdot (1+r)^n}{(1+r)^n - 1}")

st.info("""
✔ Higher tenure → Lower EMI → Lower default stress
✔ Higher interest → Higher EMI → Higher PD exposure
""")

st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------
# LTV
# ---------------------------
st.markdown('<div class="glass">', unsafe_allow_html=True)

st.markdown("### 🏠 LTV Ratio — Collateral Risk Indicator")

st.write("""
**LTV (Loan-to-Value Ratio)** measures collateral coverage against the loan.
High LTV signals insufficient security buffer — a key default risk amplifier.
""")

st.latex(r"LTV = \frac{Loan\ Amount}{Asset\ Value}")

st.info("""
✔ LTV ≤ 0.70 → Strong Collateral Coverage (Low Risk)
✔ LTV 0.70–0.90 → Moderate Collateral Stress
✔ LTV > 0.90 → Weak Security — High Default Exposure

💡 Low LTV reduces loss-given-default (LGD) even when PD is elevated
""")

st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------
# HOW BANKS ASSESS DEFAULT RISK
# ---------------------------
st.markdown('<div class="glass">', unsafe_allow_html=True)

st.markdown("### 🏦 How Banks Assess Default Risk")

st.info("""
Banks and NBFCs evaluate default probability using:

✔ Credit score trajectory
✔ Debt serviceability (DTI)
✔ Income stability & employment type
✔ Loan-to-income multiplier
✔ Collateral strength (LTV)
✔ Repayment history signals

👉 A single stressed variable can trigger Early Warning classification
""")

st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------
# AI TRANSPARENCY
# ---------------------------
st.markdown('<div class="glass">', unsafe_allow_html=True)

st.markdown("### 🔍 AI Transparency & Governance")

st.write("""
RBI and Basel III frameworks require AI credit decisions to be explainable,
auditable, and policy-compliant.

This platform includes:
""")

st.success("""
✔ AI Risk Factor Breakdown
✔ Top Default Drivers
✔ PD Band Classification Engine
✔ Early Warning Governance Layer
✔ Financial Stress Analysis
✔ RBI-Aligned Policy Compliance Logic
✔ Decision Confidence Scoring
""")

st.info("""
💡 The system ensures PD scores are not purely model-driven,
but validated using real-world banking risk governance principles.
""")

st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------
# USER JOURNEY
# ---------------------------
st.markdown('<div class="glass">', unsafe_allow_html=True)

st.markdown("### 🚀 What You Can Do")

st.write("""
👉 Go to **Risk Assessment Page** → Submit borrower profile & get PD score
👉 Go to **Analytics Page** → Understand risk breakdown & affordability

---

### 🧭 User Journey

#### 🧠 Step 1: PD Scoring Engine
✔ **Proprietary ML Model:** Probability of Default estimation
✔ PD Score with risk band classification

#### 🏦 Step 2: Early Warning Governance Layer
✔ Credit Score breach detection
✔ DTI (Debt-to-Income) stress signals
✔ LTV (Loan-to-Value) collateral risk flags
✔ Policy Override System (AI PD ≠ Final Risk Band)

#### 🔮 Step 3: Risk Advisory Engine
✔ What-If Simulation (Income vs Loan stress testing)
✔ Dynamic PD Recalculation
✔ Real-Time Risk Band Adjustment
✔ AI-Based Risk Mitigation Suggestions
✔ Smart Recommendations to reduce default probability
✔ Maximum Safe Loan Estimation

#### 📊 Step 4: Analytics Dashboard
✔ EMI vs Income Stress Analysis
✔ Loan Burden Distribution
✔ AI Risk Factor Contribution Analysis
✔ Risk Visualisation (DTI + LTV)
✔ Transparency & Confidence Insights
✔ Strategic Risk Mitigation Recommendations
✔ Early Warning Governance Summary

#### 📄 Step 5: Enterprise PDF Risk Report
✔ Official Default Risk Assessment Summary
✔ AI Governance Reports
✔ PD Score Documentation
✔ Financial Stress Snapshot
✔ Decision Transparency Summaries
✔ Loan Affordability Analysis

---

💡 This system replicates real-world **bank credit risk underwriting** by combining
Machine Learning + RBI-Aligned Policy + Borrower Advisory.
""")

st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------
# NAVIGATION
# ---------------------------
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.page_link(
        "pages/1_Decision.py",
        label="➡ Start Risk Assessment",
        help="Submit borrower profile for PD scoring"
    )

# ---------------------------
# FOOTER
# ---------------------------
st.markdown("---")
st.caption("© 2026 FinWithDip | Enterprise Credit Risk & Early Warning Platform | Developed by Subhadip | IDBI Innovate 2026 — Track 4")
