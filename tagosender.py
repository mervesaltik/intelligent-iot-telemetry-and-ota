import requests
import json
import pandas as pd

from model import make_prediction


def send_to_tago(data_dict, prediction):
    url = "https://api.eu-w1.tago.io/data"
    device_token = "9d4dec69-7b72-4051-a643-ba05526a8296"  # your token

    headers = {
        "Content-Type": "application/json",
        "Device-Token": device_token
    }

    payload = [
        {
            "variable": "cpu",
            "value": data_dict["cpu"]
        },
        {
            "variable": "disk",
            "value": data_dict["disk"]
        },
        {
            "variable": "network_recv",
            "value": data_dict["network_recv"]
        },
        {
            "variable": "network_sent",
            "value": data_dict["network_sent"]
        },
        {
            "variable": "ram",
            "value": data_dict["ram"]
        },
        {
            "variable": "prediction",
            "value": prediction
        }
    ]

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code in [200, 201, 202]:
        print("Data sended successfully!")
    else:
        print(f"Data not sended: {response.status_code}")


def read_resource_data():
    df = pd.read_csv("output22.csv")
    return {
        "cpu": df["cpu"].iloc[-1],
        "disk": df["disk"].iloc[-1],
        "network_recv": df["network_recv"].iloc[-1],
        "network_sent": df["network_sent"].iloc[-1],
        "ram": df["ram"].iloc[-1]
    }


def process_new_data():
    data = read_resource_data()  # data read
    prediction = make_prediction(data["cpu"], data["disk"], data["network_recv"], data["network_sent"], data["ram"])  # Modeli çalıştır
    print(f"Model Prediction: {prediction}")

    # Send data to Tago (with prediction
    send_to_tago(data, prediction)

