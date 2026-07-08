import matplotlib.pyplot as plt
import os
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus.paragraph import Paragraph
from reportlab.lib.styles import ParagraphStyle

from io import BytesIO
from datetime import datetime
import uuid


# ---------------------------
# FORMAT INR
# ---------------------------
def format_inr(x):
    if x >= 100000:
        return f"Rs. {x / 100000:.2f} Lakh"
    return f"Rs. {x:,.0f}"


# ---------------------------
# PD BAND HELPER
# ---------------------------
def get_pd_band_label(pd_score):
    if pd_score < 0.10:
        return "LOW RISK"
    elif pd_score < 0.30:
        return "WATCH CATEGORY"
    else:
        return "HIGH DEFAULT RISK"


# ---------------------------
# GENERATE PDF
# ---------------------------
def generate_pdf(data):
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=30,
    )

    styles = getSampleStyleSheet()

    # ---------------------------
    # CUSTOM COLORS
    # ---------------------------
    brand_blue    = colors.HexColor("#2c3e50")
    light_blue    = colors.HexColor("#eaf2f8")
    success_green = colors.HexColor("#d4edda")
    warning_yellow = colors.HexColor("#fff3cd")
    danger_red    = colors.HexColor("#f8d7da")
    dark_text     = colors.HexColor("#212529")

    # ---------------------------
    # STYLES
    # ---------------------------
    title_style = ParagraphStyle(
        "title_style",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        alignment=TA_CENTER,
        textColor=brand_blue,
    )

    subtitle_style = ParagraphStyle(
        "subtitle_style",
        parent=styles["Normal"],
        fontSize=11,
        leading=14,
        alignment=TA_CENTER,
        textColor=colors.grey,
    )

    normal_style = styles["Normal"]

    elements = []

    # ---------------------------
    # HEADER — LOGO
    # ---------------------------
    try:
        logo = Image("financelogo.png", width=140, height=50)
        elements.append(logo)
        elements.append(Spacer(1, 25))
    except:
        pass

    report_id = f"IDBI-EWS-{str(uuid.uuid4())[:8].upper()}"
    timestamp = datetime.now().strftime("%d %b %Y | %I:%M %p")

    header_text = f"""
    <b>Report ID:</b> {report_id}<br/>
    <b>Generated On:</b> {timestamp}<br/>
    <b>Classification:</b> STRICTLY CONFIDENTIAL — FOR AUTHORIZED PERSONNEL ONLY
    """

    elements.append(Paragraph(header_text, normal_style))
    elements.append(Spacer(1, 18))

    # ---------------------------
    # TITLE
    # ---------------------------
    elements.append(
        Paragraph("DEFAULT RISK ASSESSMENT REPORT", title_style)
    )

    elements.append(
        Paragraph(
            "AI-Powered Probability of Default & Early Warning Risk Intelligence Report",
            subtitle_style,
        )
    )

    elements.append(Spacer(1, 20))

    # ---------------------------
    # BORROWER PROFILE
    # ---------------------------
    elements.append(
        Paragraph("<b>Borrower Profile</b>", styles["Heading2"])
    )

    profile_data = [
        ["Borrower Name",      data.get("applicant_name", "Unknown Borrower")],
        ["Loan Type",          data.get("loan_type", "-")],
        ["Employment Status",  data.get("employment", "-")],
        ["Annual Income",      format_inr(data.get("income", 0))],
        ["Loan Amount",        format_inr(data.get("loan", 0))],
        ["Asset Value",        format_inr(data.get("asset", 0))],
        ["Credit Score",       str(data.get("credit_score", 0))],
        ["Loan Tenure",        f"{data.get('years', 0)} Years"],
        ["Interest Rate",      f"{data.get('interest', 0):.2f}%"],
    ]

    profile_table = Table(profile_data, colWidths=[180, 280])

    profile_table.setStyle(
        TableStyle([
            ("BACKGROUND",    (0, 0), (-1, -1), light_blue),
            ("GRID",          (0, 0), (-1, -1), 1, colors.white),
            ("FONTNAME",      (0, 0), (-1, -1), "Helvetica"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ])
    )

    elements.append(profile_table)
    elements.append(Spacer(1, 20))

    # ---------------------------
    # FINANCIAL SNAPSHOT
    # ---------------------------
    elements.append(
        Paragraph("<b>Financial Risk Snapshot</b>", styles["Heading2"])
    )

    pd_score  = data.get("pd_score", data.get("prob", 0))
    risk_band = data.get("risk_band", get_pd_band_label(pd_score))

    snapshot_data = [
        ["EMI", "DTI Ratio", "LTV Ratio", "PD Score (%)"],
        [
            format_inr(data.get("emi", 0)),
            f"{data.get('dti', 0):.2f}",
            f"{data.get('ltv', 0):.2f}",
            f"{pd_score * 100:.2f}%"
        ]
    ]

    snapshot_table = Table(snapshot_data, colWidths=[120, 120, 120, 120])

    snapshot_table.setStyle(
        TableStyle([
            ("BACKGROUND",    (0, 0), (-1, 0), brand_blue),
            ("TEXTCOLOR",     (0, 0), (-1, 0), colors.white),
            ("BACKGROUND",    (0, 1), (-1, 1), success_green),
            ("ALIGN",         (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME",      (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ])
    )

    elements.append(snapshot_table)
    elements.append(Spacer(1, 20))

    # ---------------------------
    # EARLY WARNING GOVERNANCE CHECK
    # ---------------------------
    elements.append(
        Paragraph("<b>Early Warning Governance Check</b>", styles["Heading2"])
    )

    flags         = data.get("early_warning_flags", [])
    flag_count    = len(flags)
    gov_ai_label  = f"PD Score: {pd_score * 100:.1f}%"
    gov_pol_label = (
        f"{flag_count} Early Warning Flag(s) Triggered"
        if flag_count > 0
        else "All Policy Checks Passed"
    )

    governance_data = [
        ["AI PD Model",      "Policy Governance Layer"],
        [gov_ai_label,       gov_pol_label]
    ]

    governance_table = Table(governance_data, colWidths=[240, 240])

    governance_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), brand_blue),
            ("TEXTCOLOR",  (0, 0), (-1, 0), colors.white),
            ("BACKGROUND", (0, 1), (-1, 1),
             success_green if flag_count == 0 else warning_yellow),
            ("ALIGN",      (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME",   (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ])
    )

    elements.append(governance_table)
    elements.append(Spacer(1, 10))

    # Active early warning flags list
    if flags:
        elements.append(
            Paragraph("<b>Active Early Warning Signals:</b>", normal_style)
        )
        for flag in flags:
            # Strip emoji for PDF compatibility
            clean_flag = flag.replace("⚠", "!").strip()
            elements.append(
                Paragraph(f"• {clean_flag}", normal_style)
            )
        elements.append(Spacer(1, 8))

    # Governance status banner
    if flag_count == 0:
        gov_status_text  = "GOVERNANCE: ALL CHECKS PASSED"
        gov_status_color = success_green
    elif flag_count <= 1:
        gov_status_text  = "GOVERNANCE: WATCH — ELEVATED RISK SIGNALS"
        gov_status_color = warning_yellow
    else:
        gov_status_text  = "GOVERNANCE: ALERT — MULTIPLE RISK FLAGS"
        gov_status_color = danger_red

    status_table = Table([[gov_status_text]], colWidths=[480])

    status_table.setStyle(
        TableStyle([
            ("BACKGROUND",    (0, 0), (-1, -1), gov_status_color),
            ("ALIGN",         (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME",      (0, 0), (-1, -1), "Helvetica-Bold"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ])
    )

    elements.append(status_table)
    elements.append(Spacer(1, 20))

    # ---------------------------
    # AI RISK SUMMARY
    # ---------------------------
    elements.append(
        Paragraph("<b>AI Risk Intelligence Summary</b>", styles["Heading2"])
    )

    credit_score_val = data.get("credit_score", 0)
    dti_val          = data.get("dti", 0)
    ltv_val          = data.get("ltv", 0)
    income_val       = data.get("income", 0)

    credit_signal = (
        "Prime credit tier — Strong default resistance"
        if credit_score_val > 750
        else "Standard credit profile — Moderate default risk"
        if credit_score_val >= 650
        else "Sub-standard credit — Elevated default probability"
    )

    dti_signal = (
        "Low debt burden — Healthy repayment capacity"
        if dti_val < 0.30
        else "Moderate debt stress — Monitor closely"
        if dti_val < 0.60
        else "High DTI — Debt serviceability breach detected"
    )

    ltv_signal = (
        "Strong collateral coverage — Low LGD exposure"
        if ltv_val <= 0.70
        else "Adequate collateral — Moderate LGD risk"
        if ltv_val <= 0.90
        else "Weak collateral — High LGD exposure"
    ) if ltv_val > 0 else "No collateral data provided"

    income_signal = (
        "Student profile — Evaluated under education lending rules"
        if income_val == 0
        else "Lower income — Reduced stress buffer"
        if income_val < 500000
        else "Stable income — Positive serviceability signal"
    )

    ai_summary = f"""
    <b>Credit Score Signal:</b> {credit_signal}<br/>
    <b>DTI Signal:</b> {dti_signal}<br/>
    <b>Collateral Signal:</b> {ltv_signal}<br/>
    <b>Income Signal:</b> {income_signal}
    """

    elements.append(Paragraph(ai_summary, normal_style))
    elements.append(Spacer(1, 18))

    # ---------------------------
    # STRATEGIC RISK INSIGHTS
    # ---------------------------
    elements.append(
        Paragraph("<b>Strategic Risk Intelligence</b>", styles["Heading2"])
    )

    if risk_band == "LOW RISK":
        strategic_text = """
        • Borrower classified in LOW RISK band — Standard monitoring applies<br/>
        • No immediate intervention required<br/>
        • Annual credit review recommended<br/>
        • Borrower demonstrates healthy repayment capacity
        """
    elif risk_band == "WATCH CATEGORY":
        strategic_text = """
        • Borrower in WATCH CATEGORY — Proactive monitoring recommended<br/>
        • Partial prepayment advised to reduce outstanding principal<br/>
        • Credit score improvement through timely existing repayments<br/>
        • Tenure restructuring may reduce EMI burden and DTI stress<br/>
        • Quarterly review cadence recommended
        """
    else:
        strategic_text = """
        • HIGH DEFAULT RISK — Immediate intervention required<br/>
        • Initiate Early Warning System (EWS) protocol<br/>
        • Request updated income documentation and bank statements<br/>
        • Refer to Credit Risk Committee for enhanced scrutiny<br/>
        • Consider loan restructuring, moratorium, or co-applicant addition<br/>
        • Assign dedicated relationship manager for monitoring
        """

    elements.append(Paragraph(strategic_text, normal_style))
    elements.append(Spacer(1, 18))

    # ---------------------------
    # AI RISK BREAKDOWN CHART
    # ---------------------------
    elements.append(
        Paragraph("<b>AI Default Risk Factor Breakdown</b>", styles["Heading2"])
    )

    factors = ["Credit Risk", "Debt Burden", "Collateral Gap", "Income Stability"]

    # Risk contribution scores (higher = more default risk)
    credit_risk_score = int(((600 - min(credit_score_val, 600)) / 300) * 40)
    debt_burden_score = int(min(dti_val, 1) * 30)
    collateral_score  = int(min(ltv_val, 1) * 20)
    income_risk_score = (
        10 if data.get("employment", "") == "Unemployed" else 2
    )

    scores = [
        credit_risk_score,
        debt_burden_score,
        collateral_score,
        income_risk_score
    ]

    bar_colors = []
    for s in scores:
        if s >= 20:
            bar_colors.append("#e74c3c")   # red — high risk
        elif s >= 10:
            bar_colors.append("#f39c12")   # orange — moderate
        else:
            bar_colors.append("#2ecc71")   # green — low

    plt.figure(figsize=(5.8, 2.8))

    bars = plt.bar(
        factors,
        scores,
        color=bar_colors,
        edgecolor="black",
        linewidth=0.8
    )

    for bar in bars:
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height + 0.5,
            f"{height}",
            ha="center",
            fontsize=9,
            fontweight="bold"
        )

    plt.ylim(0, max(scores) + 8 if scores else 10)
    plt.ylabel("Risk Contribution Score")
    plt.title(
        "AI Default Risk Factor Contribution",
        fontsize=12,
        fontweight="bold",
        pad=8
    )
    plt.tight_layout()

    chart_path = "decision_chart.png"
    plt.savefig(chart_path, bbox_inches="tight")
    plt.close()

    chart = Image(chart_path, width=420, height=220)
    elements.append(chart)
    elements.append(Spacer(1, 20))

    # ---------------------------
    # FINANCIAL VISUALIZATION
    # ---------------------------
    elements.append(
        Paragraph("<b>Loan Affordability & Burden Analysis</b>", styles["Heading2"])
    )

    try:
        emi_chart    = Image("emi_vs_income.png",  width=230, height=170)
        burden_chart = Image("loan_burden.png",    width=230, height=170)

        emi_title    = Paragraph("<b>Income vs EMI Capacity</b>",            styles["BodyText"])
        burden_title = Paragraph("<b>Monthly Income Burden Distribution</b>", styles["BodyText"])

        charts_table = Table(
            [
                [emi_title,  burden_title],
                [emi_chart,  burden_chart]
            ],
            colWidths=[240, 240]
        )

        charts_table.setStyle(
            TableStyle([
                ("ALIGN",         (0, 0), (-1, -1), "CENTER"),
                ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
                ("BOTTOMPADDING", (0, 0), (-1, 0),  12),
                ("TOPPADDING",    (0, 1), (-1, 1),   8),
            ])
        )

        elements.append(charts_table)

    except:
        pass

    elements.append(Spacer(1, 20))

    # ---------------------------
    # FINAL RISK BAND DECISION
    # ---------------------------
    elements.append(
        Paragraph("<b>Final Risk Assessment</b>", styles["Heading2"])
    )

    if risk_band == "LOW RISK":
        decision_text  = f"RISK BAND: LOW RISK — PD {pd_score * 100:.1f}%"
        decision_color = success_green
    elif risk_band == "WATCH CATEGORY":
        decision_text  = f"RISK BAND: WATCH CATEGORY — PD {pd_score * 100:.1f}%"
        decision_color = warning_yellow
    else:
        decision_text  = f"RISK BAND: HIGH DEFAULT RISK — PD {pd_score * 100:.1f}%"
        decision_color = danger_red

    decision_table = Table([[decision_text]], colWidths=[480])

    decision_table.setStyle(
        TableStyle([
            ("BACKGROUND",    (0, 0), (-1, -1), decision_color),
            ("ALIGN",         (0, 0), (-1, -1), "CENTER"),
            ("FONTNAME",      (0, 0), (-1, -1), "Helvetica-Bold"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 15),
        ])
    )

    elements.append(decision_table)
    elements.append(Spacer(1, 12))

    elements.append(
        Paragraph(
            f"<b>Probability of Default (PD):</b> {pd_score * 100:.2f}% &nbsp;&nbsp; "
            f"<b>Early Warning Flags:</b> {flag_count}",
            normal_style
        )
    )

    elements.append(Spacer(1, 20))

    # ---------------------------
    # DISCLAIMER
    # ---------------------------
    disclaimer = """
    This report was generated using the FinWithDip Hybrid AI Credit Risk Governance Framework
    in compliance with IDBI Innovate 2026 — Problem Statement 4: Default Prediction Model.<br/><br/>

    The risk assessment is based on:<br/>
    <b>•</b> AI Probability of Default (PD) modelling<br/>
    <b>•</b> RBI-aligned credit risk governance policies<br/>
    <b>•</b> Basel III Early Warning System (EWS) principles<br/>
    <b>•</b> Borrower financial affordability analysis<br/>
    <b>•</b> Collateral strength and LGD assessment<br/><br/>

    This document is intended for simulation, educational, and analytical purposes only.
    It does not constitute a formal credit decision or regulatory filing.
    """

    elements.append(Paragraph(disclaimer, normal_style))
    elements.append(Spacer(1, 30))

    # ---------------------------
    # FOOTER
    # ---------------------------
    footer = """
    <b>FinWithDip — Enterprise Credit Risk & Early Warning Platform</b><br/>
    Generated Electronically — No Physical Signature Required<br/><br/>
    © 2026 FinWithDip | AI Default Risk Intelligence Platform | Developed by Subhadip | IDBI Innovate 2026 — Track 4
    """

    elements.append(Paragraph(footer, subtitle_style))

    # ---------------------------
    # BUILD PDF
    # ---------------------------
    doc.build(elements)

    pdf = buffer.getvalue()
    buffer.close()

    return pdf
