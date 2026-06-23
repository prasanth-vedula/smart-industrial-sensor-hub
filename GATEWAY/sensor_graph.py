import json
import paho.mqtt.client as mqtt
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

temperature_data = []
humidity_data = []

MAX_POINTS = 20


def on_message(client, userdata, msg):
    global temperature_data
    global humidity_data

    try:
        data = json.loads(msg.payload.decode())

        temperature = data["temperature"]
        humidity = data["humidity"]

        temperature_data.append(temperature)
        humidity_data.append(humidity)

        if len(temperature_data) > MAX_POINTS:
            temperature_data.pop(0)

        if len(humidity_data) > MAX_POINTS:
            humidity_data.pop(0)

        print(
            f"Temp={temperature}  Humidity={humidity}"
        )

    except Exception as e:
        print("Error:", e)


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

client.loop_start()


fig, ax = plt.subplots()


def update(frame):

    ax.clear()

    ax.plot(
        temperature_data,
        label="Temperature"
    )

    ax.plot(
        humidity_data,
        label="Humidity"
    )

    ax.set_title(
        "Industrial Sensor Trends"
    )

    ax.set_ylabel(
        "Value"
    )

    ax.legend()

    ax.grid(True)


ani = FuncAnimation(
    fig,
    update,
    interval=1000,
    cache_frame_data=False
)

plt.show()