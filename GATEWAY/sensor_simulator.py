import random
import time
import json
import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
TOPIC = "factory/sensors"

client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2
)

client.connect(BROKER, PORT, 60)

print("Industrial Sensor Publisher Started...")
print("Publishing to topic:", TOPIC)

while True:

    temperature = round(random.uniform(25, 40), 2)
    humidity = round(random.uniform(40, 70), 2)

    sensor_data = {
        "temperature": temperature,
        "humidity": humidity
    }

    payload = json.dumps(sensor_data)

    client.publish(TOPIC, payload)

    print("Published:", payload)

    time.sleep(2)