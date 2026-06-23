import tkinter as tk
import json
import csv
import os
from datetime import datetime
import paho.mqtt.client as mqtt

# ----------------------------------
# CSV FILE PATH
# ----------------------------------

CSV_FILE = r"D:\EMBDDED SYSTEMS & IOT\embeded systems projects\smart-sensor-hub(project-1)\DATA\sensor_data.csv"

# ----------------------------------
# CREATE CSV HEADER IF EMPTY
# ----------------------------------

if not os.path.exists(CSV_FILE) or os.path.getsize(CSV_FILE) == 0:
    with open(CSV_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "Timestamp",
                "Temperature",
                "Humidity"
            ]
        )

# ----------------------------------
# DASHBOARD WINDOW
# ----------------------------------

root = tk.Tk()
root.title("Smart Industrial Sensor Hub")
root.geometry("700x500")

temp_var = tk.StringVar()
hum_var = tk.StringVar()
status_var = tk.StringVar()

temp_var.set("Temperature: -- °C")
hum_var.set("Humidity: -- %")
status_var.set("Waiting for Sensor Data...")

title = tk.Label(
    root,
    text="Industrial Sensor Dashboard",
    font=("Arial", 24, "bold")
)
title.pack(pady=20)

temp_label = tk.Label(
    root,
    textvariable=temp_var,
    font=("Arial", 20)
)
temp_label.pack(pady=20)

hum_label = tk.Label(
    root,
    textvariable=hum_var,
    font=("Arial", 20)
)
hum_label.pack(pady=20)

status_label = tk.Label(
    root,
    textvariable=status_var,
    fg="blue",
    font=("Arial", 14)
)
status_label.pack(pady=20)

# ----------------------------------
# UPDATE GUI
# ----------------------------------

def update_gui(temp, hum):

    temp_var.set(f"Temperature: {temp} °C")
    hum_var.set(f"Humidity: {hum} %")

    status_var.set("Live Sensor Data Receiving")

# ----------------------------------
# SAVE TO CSV
# ----------------------------------

def save_to_csv(temp, hum):

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    with open(
        CSV_FILE,
        "a",
        newline=""
    ) as file:

        writer = csv.writer(file)

        writer.writerow(
            [
                timestamp,
                temp,
                hum
            ]
        )

# ----------------------------------
# MQTT CALLBACKS
# ----------------------------------

def on_connect(
        client,
        userdata,
        flags,
        reason_code,
        properties=None):

    print("CONNECTED TO BROKER")

    client.subscribe(
        "factory/sensors"
    )

def on_message(
        client,
        userdata,
        msg):

    try:

        payload = msg.payload.decode()

        print(
            "RECEIVED:",
            payload
        )

        data = json.loads(payload)

        temperature = data["temperature"]
        humidity = data["humidity"]

        save_to_csv(
            temperature,
            humidity
        )

        root.after(
            0,
            lambda: update_gui(
                temperature,
                humidity
            )
        )

    except Exception as e:

        print(
            "ERROR:",
            e
        )

# ----------------------------------
# MQTT CLIENT
# ----------------------------------

client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2
)

client.on_connect = on_connect
client.on_message = on_message

client.connect(
    "127.0.0.1",
    1883,
    60
)

client.loop_start()

# ----------------------------------
# RUN APP
# ----------------------------------

root.mainloop()