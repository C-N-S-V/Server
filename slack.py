import requests
import time
import json

slack_url = "slack api"
sensor_url = "sensor url"

def send_slack_message(message):
    headers = {
        "Content-type": "application/json"
    }
    data = {
        "text": message
    }
    response = requests.post(slack_url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        return "Notification sent"
    else:
        return f"Error: {response.status_code}, {response.text}"

def get_sensor_data():
    try:
        response = requests.post(sensor_url, json={"sensor": "temperature", "value": 22.5})
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching sensor data: {response.status_code}, {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request exception: {e}")
        return None

while True:
    sensor_data = get_sensor_data()
    if sensor_data is not None:
        if isinstance(sensor_data, int):
            if sensor_data == 1:
                result = send_slack_message("척추를 똑바로 하세요")
                print(result)
            else:
                print(f"Sensor value: {sensor_data}")
        elif isinstance(sensor_data, dict) and "value" in sensor_data:
            if sensor_data["value"] == 1:
                result = send_slack_message("척추를 똑바로 하세요")
                print(result)
            else:
                print(f"Sensor value: {sensor_data['value']}")
        else:
            print(f"Unexpected sensor data format: {sensor_data}")
    time.sleep(1)
