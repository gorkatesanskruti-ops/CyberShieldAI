
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from datetime import datetime


def generate_security_report(incidents, posture_score):

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4
    )

    styles = getSampleStyleSheet()
    elements = []

    elements.append(
        Paragraph("CYBERSHIELD AI", styles["Title"])
    )

    elements.append(
        Paragraph(
            "Security Risk Assessment Report",
            styles["Heading2"]
        )
    )

    elements.append(Spacer(1, 20))

    elements.append(
        Paragraph(
            f"Generated: {datetime.now().strftime('%d-%m-%Y %H:%M')}",
            styles["Normal"]
        )
    )

    high = sum(1 for x in incidents if x[3] == "High")
    medium = sum(1 for x in incidents if x[3] == "Medium")
    low = sum(1 for x in incidents if x[3] == "Low")

    data = [
        ["Security Metric", "Result"],
        ["Total Incidents", str(len(incidents))],
        ["High Risk", str(high)],
        ["Medium Risk", str(medium)],
        ["Low Risk", str(low)],
        ["Security Posture", f"{posture_score}/100"]
    ]

    table = Table(data, colWidths=[250, 180])

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0),
         colors.HexColor("#176B9A")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 10)
    ]))

    elements.append(table)
    elements.append(Spacer(1, 25))

    elements.append(
        Paragraph("Security Recommendations", styles["Heading2"])
    )

    recommendations = [
        "Enable multi-factor authentication.",
        "Use strong and unique passwords.",
        "Avoid suspicious links.",
        "Never share OTPs or banking details.",
        "Investigate high-risk incidents.",
        "Keep software updated."
    ]

    for item in recommendations:
        elements.append(
            Paragraph(f"- {item}", styles["Normal"])
        )
        elements.append(Spacer(1, 8))

    doc.build(elements)

    buffer.seek(0)

    return buffer.getvalue()
