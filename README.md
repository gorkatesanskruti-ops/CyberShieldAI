# 🛡️ CyberShield AI
### AI-Powered Cybersecurity Monitoring and Threat Detection System

CyberShield AI is a Python-based cybersecurity application designed to identify potential cyber threats, detect phishing and fraudulent messages, analyze suspicious URLs, and monitor security risks through an interactive dashboard.

## 🚀 Features

- **Phishing Detection:** Identifies suspicious and potentially malicious messages.
- **Fraud Detection:** Analyzes messages for possible fraud indicators.
- **URL Security Scanner:** Checks URLs for suspicious characteristics.
- **AI Risk Assessment:** Calculates risk scores and classifies threats as Low, Medium, or High.
- **Email Alerts:** Sends email notifications when a HIGH-risk incident is detected.
- **Security Dashboard:** Displays security incidents, statistics, and visual charts.
- **Security Posture Score:** Calculates an overall security score out of 100.
- **Incident History:** Stores security incidents using SQLite.
- **PDF Reports:** Generates downloadable security reports.
- **Security Recommendations:** Provides suggestions to improve security.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Interactive dashboard |
| Pandas | Data processing |
| Plotly | Data visualization |
| SQLite | Incident database |
| Python-dotenv | Environment variable management |
| ReportLab | PDF report generation |
| SMTP | Email security alerts |

## 📁 Project Structure

```text
CyberShieldAI/
│
├── app.py
├── requirements.txt
├── .gitignore
│
├── agents/
│   ├── phishing_agent.py
│   ├── fraud_agent.py
│   └── risk_agent.py
│
├── core/
│   ├── database.py
│   ├── email_alert.py
│   ├── posture_score.py
│   ├── report_generator.py
│   └── security_analyzer.py
│
├── data/
└── models/
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/gorkatesanskruti-ops/CyberShieldAI.git
```

### 2. Open the project

```bash
cd CyberShieldAI
```

### 3. Create a virtual environment

```bash
python3 -m venv .venv
```

### 4. Activate the environment

Mac/Linux:

```bash
source .venv/bin/activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure email alerts

Create a `.env` file in the project directory:

```env
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_gmail_app_password
ALERT_EMAIL=recipient@gmail.com
```

Keep your `.env` file private. Never upload passwords or credentials to GitHub.

### 7. Run the application

```bash
python -m streamlit run app.py
```

Open the local URL displayed in your terminal.

## 📊 Risk Classification

| Risk Level | Description |
|---|---|
| 🟢 Low | Low-risk activity |
| 🟡 Medium | Suspicious activity requiring attention |
| 🔴 High | High-risk activity requiring immediate attention |

Email alerts are configured for HIGH-risk incidents.

## 🎯 Project Objective

The objective of CyberShield AI is to make cybersecurity monitoring easier through automated threat analysis, risk assessment, incident tracking, and security reporting.

## 👩‍💻 Developer

**Sanskruti Santosh Gorkate**

GitHub: [gorkatesanskruti-ops](https://github.com/gorkatesanskruti-ops)

## 📌 Repository

[CyberShield AI on GitHub](https://github.com/gorkatesanskruti-ops/CyberShieldAI)

---

*Built with Python and Streamlit.*
