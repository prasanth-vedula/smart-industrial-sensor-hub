import sqlite3
import json
import paho.mqtt.client as mqtt
from datetime import datetime

DATABASE_NAME = "sensor_data.db"

connection = sqlite3.connect(
    DATABASE_NAME
)

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS sensor_readings(
id INTEGER PRIMARY KEY AUTOINCREMENT,
timestamp TEXT,
temperature REAL,
humidity REAL
)
""")

connection.commit()


def on_message(client, userdata, msg):

    data = json.loads(
        msg.payload.decode()
    )

    temperature = data["temperature"]
    humidity = data["humidity"]

    timestamp = str(
        datetime.now()
    )

    cursor.execute(
        """
        INSERT INTO sensor_readings
        (
        timestamp,
        temperature,
        humidity
        )
        VALUES
        (
        ?,
        ?,
        ?
        )
        """,
        (
            timestamp,
            temperature,
            humidity
        )
    )

    connection.commit()

    print(
        f"DB Stored -> Temp:{temperature} Hum:{humidity}"
    )


client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2
)

client.connect(
    "localhost",
    1883,
    60
)

client.subscribe(
    "factory/sensors"
)

client.on_message = on_message

print(
    "SQLite Database Logger Started"
)

client.loop_forever()