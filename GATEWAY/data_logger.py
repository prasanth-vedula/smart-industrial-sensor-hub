import paho.mqtt.client as mqtt
import json
import csv
import os
from datetime import datetime

FILE_NAME = "sensor_log.csv"

if not os.path.exists(FILE_NAME):
    with open(FILE_NAME, "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            "Timestamp",
            "Temperature",
            "Humidity"
        ])

def on_message(client, userdata, msg):

    data = json.loads(
        msg.payload.decode()
    )

    timestamp = datetime.now()

    temperature = data["temperature"]
    humidity = data["humidity"]

    with open(FILE_NAME, "a", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            timestamp,
            temperature,
            humidity
        ])

    print(
        f"Logged -> Temp:{temperature} Hum:{humidity}"
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

client.loop_forever()