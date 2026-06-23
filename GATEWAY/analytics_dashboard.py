import sqlite3
import matplotlib.pyplot as plt

# Connect Database
conn = sqlite3.connect("sensor_data.db")

cursor = conn.cursor()

# Read Last 20 Records
cursor.execute("""
SELECT temperature, humidity
FROM sensor_readings
ORDER BY id DESC
LIMIT 20
""")

rows = cursor.fetchall()

conn.close()

# Reverse Order
rows.reverse()

temperatures = []
humidities = []

for row in rows:
    temperatures.append(row[0])
    humidities.append(row[1])

# Plot Graph
plt.figure(figsize=(10,5))

plt.plot(
    temperatures,
    marker="o",
    label="Temperature"
)

plt.plot(
    humidities,
    marker="s",
    label="Humidity"
)

plt.title("Industrial Sensor Analytics")
plt.xlabel("Samples")
plt.ylabel("Values")
plt.legend()
plt.grid()

plt.show()