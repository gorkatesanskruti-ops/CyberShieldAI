import sqlite3
from datetime import datetime

DB_NAME = "data/cybershield.db"


def create_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            incident_type TEXT,
            description TEXT,
            risk_level TEXT,
            risk_score INTEGER,
            timestamp TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_incident(incident_type, description, risk_level, risk_score):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO incidents
        (incident_type, description, risk_level, risk_score, timestamp)
        VALUES (?, ?, ?, ?, ?)
    """, (
        incident_type,
        description,
        risk_level,
        risk_score,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


def get_incidents():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM incidents ORDER BY id DESC")
    incidents = cursor.fetchall()

    conn.close()
    return incidents