import sqlite3

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet

doc = SimpleDocTemplate("Industrial_Report.pdf")

styles = getSampleStyleSheet()

elements = []

title = Paragraph(
    "Industrial Sensor Monitoring Report",
    styles["Title"]
)

elements.append(title)

elements.append(Spacer(1, 20))

conn = sqlite3.connect("sensor_data.db")

cursor = conn.cursor()

cursor.execute("""
SELECT *
FROM sensor_readings
ORDER BY id DESC
LIMIT 20
""")

rows = cursor.fetchall()

conn.close()

for row in rows:

    text = Paragraph(
        f"ID: {row[0]} | Temp: {row[1]} °C | Humidity: {row[2]} %",
        styles["Normal"]
    )

    elements.append(text)

    elements.append(Spacer(1, 5))

doc.build(elements)

print("PDF Report Generated Successfully")