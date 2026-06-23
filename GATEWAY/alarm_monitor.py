import json
import paho.mqtt.client as mqtt

TEMP_WARNING = 35
TEMP_CRITICAL = 38
HUM_WARNING = 65


def on_message(client, userdata, msg):

    data = json.loads(
        msg.payload.decode()
    )

    temp = data["temperature"]
    hum = data["humidity"]

    print(
        f"Temperature={temp}°C  Humidity={hum}%"
    )

    if temp >= TEMP_CRITICAL:
        print(
            "CRITICAL ALERT -> HIGH TEMPERATURE"
        )

    elif temp >= TEMP_WARNING:
        print(
            "WARNING -> TEMPERATURE HIGH"
        )

    if hum >= HUM_WARNING:
        print(
            "WARNING -> HUMIDITY HIGH"
        )

    print("-" * 50)


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

print("Alarm Monitor Started")

client.loop_forever()