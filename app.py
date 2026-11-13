
import streamlit as st
import pandas as pd
import plotly.express as px
import os
import re
from dotenv import load_dotenv

from agents.phishing_agent import PhishingAgent
from agents.fraud_agent import FraudAgent
from agents.risk_agent import RiskAgent

from core.security_analyzer import analyze_url
from core.database import create_database, save_incident, get_incidents
from core.email_alert import send_security_alert
from core.posture_score import calculate_posture_score
from core.report_generator import generate_security_report


# ---------------- CONFIGURATION ----------------

load_dotenv()
create_database()

st.set_page_config(
    page_title="CyberShield AI",
    page_icon="🛡️",
    layout="wide"
)


# ---------------- CUSTOM DESIGN ----------------

st.markdown("""
<style>
.stApp {
    background-color: #080d1a;
    color: white;
}

section[data-testid="stSidebar"] {
    background-color: #101a30;
}

h1, h2, h3 {
    color: #56c8ff;
}

div[data-testid="stMetric"] {
    background-color: #14213d;
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #25466d;
}

.stButton button {
    background-color: #d94355;
    color: white;
    border-radius: 8px;
    border: none;
}

.stButton button:hover {
    background-color: #a92e43;
    color: white;
}
</style>
""", unsafe_allow_html=True)


# ---------------- AI AGENTS ----------------

phishing_agent = PhishingAgent()
fraud_agent = FraudAgent()
risk_agent = RiskAgent()


# ---------------- HELPER FUNCTIONS ----------------

def display_result(result):

    score = int(result["risk_score"])
    level = result["risk_level"]

    st.subheader("Security Analysis Result")

    col1, col2 = st.columns(2)

    col1.metric("Risk Score", f"{score}/100")
    col2.metric("Risk Level", level.upper())

    st.progress(max(0, min(score, 100)) / 100)

    if level == "High":
        st.error("🚨 HIGH RISK DETECTED")

    elif level == "Medium":
        st.warning("⚠️ MEDIUM RISK DETECTED")

    else:
        st.success("✅ LOW RISK")

    reasons = result.get("reasons", [])

    st.write("### Detection Reasons")

    if reasons:
        for reason in reasons:
            st.write(f"- {reason}")
    else:
        st.info("No suspicious indicators detected.")


def process_incident(incident_type, description, result):

    risk_level = result["risk_level"]
    risk_score = int(result["risk_score"])

    # Save incident in SQLite
    save_incident(
        incident_type,
        description[:500],
        risk_level,
        risk_score
    )

    st.success("Incident recorded successfully!")

    # Send email only for HIGH risk
    if risk_level == "High":

        st.warning("High-risk threat detected. Sending email alert...")

        try:
            email_sent = send_security_alert(
                incident_type,
                description[:500],
                risk_score
            )

            if email_sent:
                st.success("📧 Security alert email sent successfully!")
            else:
                st.error(
                    "Email could not be sent. "
                    "Please check your .env settings."
                )

        except Exception as error:
            st.error(f"Email error: {error}")

    else:
        st.info(
            "Email notification is sent only for HIGH-risk incidents."
        )


def create_incident_dataframe(incidents):

    return pd.DataFrame(
        incidents,
        columns=[
            "ID",
            "Incident Type",
            "Description",
            "Risk Level",
            "Risk Score",
            "Timestamp"
        ]
    )


# ---------------- SIDEBAR ----------------

st.sidebar.title("🛡️ CyberShield AI")

st.sidebar.caption("AI-Powered Cybersecurity Platform")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Phishing Detector",
        "URL Scanner",
        "Fraud Detector",
        "Incident History",
        "Security Report",
        "Security Recommendations",
        "About Project"
    ]
)


# ---------------- DASHBOARD ----------------

if page == "Dashboard":

    st.title("🛡️ CyberShield AI Dashboard")

    st.write(
        "Monitor cybersecurity threats, incidents and organizational risk."
    )

    incidents = get_incidents()

    total = len(incidents)

    high = sum(1 for x in incidents if x[3] == "High")
    medium = sum(1 for x in incidents if x[3] == "Medium")
    low = sum(1 for x in incidents if x[3] == "Low")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Incidents", total)
    col2.metric("High Risk", high)
    col3.metric("Medium Risk", medium)
    col4.metric("Low Risk", low)

    st.divider()

    # SECURITY POSTURE

    st.subheader("🛡️ Security Posture")

    posture_score = calculate_posture_score(incidents)

    st.metric(
        "Security Posture Score",
        f"{posture_score}/100"
    )

    st.progress(posture_score / 100)

    if posture_score >= 80:
        st.success("Excellent security posture!")

    elif posture_score >= 50:
        st.warning("Moderate security risk. Review incidents.")

    else:
        st.error(
            "Critical security posture. Immediate attention required."
        )

    st.divider()

    # INCIDENT ANALYTICS

    if incidents:

        df = create_incident_dataframe(incidents)

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("Risk Distribution")

            risk_counts = (
                df["Risk Level"]
                .value_counts()
                .reset_index()
            )

            risk_counts.columns = ["Risk Level", "Count"]

            fig = px.pie(
                risk_counts,
                names="Risk Level",
                values="Count",
                hole=0.45
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        with col2:

            st.subheader("Incident Risk Scores")

            fig = px.bar(
                df,
                x="Incident Type",
                y="Risk Score",
                color="Risk Level"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

        st.subheader("Recent Incidents")

        st.dataframe(
            df.head(10),
            use_container_width=True
        )

    else:

        st.info(
            "No incidents recorded yet. Start by analyzing a message or URL."
        )

    # EMAIL CONFIGURATION

    st.divider()

    st.subheader("📧 Gmail Alert Configuration")

    if all([
        os.getenv("EMAIL_ADDRESS"),
        os.getenv("EMAIL_PASSWORD"),
        os.getenv("ALERT_EMAIL")
    ]):

        st.success("Gmail settings configured.")

    else:

        st.warning(
            "Gmail settings are missing. Check your .env file."
        )


# ---------------- PHISHING DETECTOR ----------------

elif page == "Phishing Detector":

    st.title("🎣 Phishing Detection Agent")

    message = st.text_area(
        "Enter an email or message to analyze:",
        height=180,
        placeholder="Paste a test email here..."
    )

    if st.button("Analyze Message", type="primary"):

        if message.strip():

            phishing_result = phishing_agent.detect(message)

            fraud_result = fraud_agent.detect(message)

            final_result = risk_agent.calculate_risk(
                phishing_result,
                fraud_result
            )

            display_result(final_result)

            process_incident(
                "Phishing Analysis",
                message,
                final_result
            )

        else:

            st.warning("Please enter a message.")


# ---------------- URL SCANNER ----------------

elif page == "URL Scanner":

    st.title("🔗 Malicious URL Scanner")

    url = st.text_input(
        "Enter a URL:",
        placeholder="https://example.com"
    )

    if st.button("Scan URL", type="primary"):

        if url.strip():

            if not re.match(
                r"^https?://",
                url.strip(),
                re.IGNORECASE
            ):
                url = "https://" + url.strip()

            result = analyze_url(url.strip())

            display_result(result)

            process_incident(
                "URL Security Scan",
                url.strip(),
                result
            )

        else:

            st.warning("Please enter a URL.")


# ---------------- FRAUD DETECTOR ----------------

elif page == "Fraud Detector":

    st.title("💳 Fraud Detection Agent")

    message = st.text_area(
        "Enter a message to check for fraud:",
        height=180,
        placeholder="Enter a test banking or payment message..."
    )

    if st.button("Detect Fraud", type="primary"):

        if message.strip():

            result = fraud_agent.detect(message)

            display_result(result)

            process_incident(
                "Fraud Detection",
                message,
                result
            )

        else:

            st.warning("Please enter a message.")


# ---------------- INCIDENT HISTORY ----------------

elif page == "Incident History":

    st.title("📋 Security Incident History")

    incidents = get_incidents()

    if incidents:

        df = create_incident_dataframe(incidents)

        selected_level = st.selectbox(
            "Filter by Risk Level",
            ["All", "High", "Medium", "Low"]
        )

        if selected_level != "All":

            df = df[
                df["Risk Level"] == selected_level
            ]

        st.dataframe(
            df,
            use_container_width=True
        )

        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "📥 Download CSV Report",
            data=csv,
            file_name="cybershield_incidents.csv",
            mime="text/csv"
        )

    else:

        st.info("No incidents recorded yet.")


# ---------------- SECURITY REPORT ----------------

elif page == "Security Report":

    st.title("📄 Security Risk Assessment Report")

    incidents = get_incidents()

    posture_score = calculate_posture_score(incidents)

    st.metric(
        "Current Security Posture",
        f"{posture_score}/100"
    )

    st.write(f"Total recorded incidents: {len(incidents)}")

    if st.button("Generate PDF Report", type="primary"):

        try:

            pdf_data = generate_security_report(
                incidents,
                posture_score
            )

            st.download_button(
                "📥 Download Security Report",
                data=pdf_data,
                file_name="CyberShield_AI_Security_Report.pdf",
                mime="application/pdf"
            )

        except Exception as error:

            st.error(f"Report generation failed: {error}")


# ---------------- SECURITY RECOMMENDATIONS ----------------

elif page == "Security Recommendations":

    st.title("🔐 Security Recommendations")

    recommendations = [
        "Enable multi-factor authentication.",
        "Use strong and unique passwords.",
        "Never share OTPs or banking details.",
        "Verify suspicious links before opening them.",
        "Keep operating systems and applications updated.",
        "Use antivirus and endpoint protection.",
        "Monitor unusual login activity.",
        "Train employees to identify phishing attacks.",
        "Maintain regular backups.",
        "Investigate all high-risk security incidents."
    ]

    for recommendation in recommendations:

        st.write(f"✅ {recommendation}")


# ---------------- ABOUT PROJECT ----------------

elif page == "About Project":

    st.title("About CyberShield AI")

    st.write("""
    CyberShield AI is a Python-based cybersecurity monitoring prototype.

    It uses multiple security agents to analyze suspicious messages,
    potentially malicious URLs and possible financial fraud.

    ### Main Features

    - Phishing Detection
    - Fraud Detection
    - Malicious URL Analysis
    - Combined Risk Analysis
    - Security Posture Score
    - Automatic Incident Logging
    - Gmail Security Alerts
    - Security Incident Analytics
    - PDF Security Reports

    ### Technology Stack

    - Python
    - Streamlit
    - SQLite
    - Pandas
    - Plotly
    - ReportLab
    - Gmail SMTP

    The current detection system uses predefined rules and indicators.
    It is a prototype and does not replace professional security software
    or live threat intelligence.
    """)


# ---------------- FOOTER ----------------

st.sidebar.divider()

st.sidebar.caption(
    "CyberShield AI | Python Cybersecurity Platform"
)
