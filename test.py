import requests
import json
import pandas as pd
import random
import time

# Slack 웹훅 URL 및 센서 데이터 URL (실제 URL로 교체하세요)
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

# 실시간 데이터를 저장할 DataFrame 초기화
df = pd.DataFrame(columns=['Value'])

# 1분 동안 1의 개수를 세고 알림을 보내는 함수
def count_ones_and_notify():
    global df
    while True:
        start_time = time.time()
        while time.time() - start_time < 60:  # 1분 동안 데이터를 수집
            sensor_data = get_sensor_data()
            if sensor_data is not None:
                if isinstance(sensor_data, int):
                    new_value = sensor_data
                elif isinstance(sensor_data, dict) and "value" in sensor_data:
                    new_value = sensor_data["value"]
                else:
                    print(f"Unexpected sensor data format: {sensor_data}")
                    continue

                # 데이터 추가 및 슬랙 알림
                new_row = pd.DataFrame({'Value': [new_value]})
                df = pd.concat([df, new_row], ignore_index=True)

                if new_value == 1:
                    result = send_slack_message("척추를 똑바로 하세요")
                    print(result)

                time.sleep(0.5)  # 500ms마다 데이터를 수집

        # 1분 동안 1의 개수를 세기
        ones_count = df['Value'].sum()  # 1의 개수 합계
        message = f"지난 1분 동안 자세가 {ones_count}번 흐트러졌습니다."
        print(message)

        # 슬랙으로 메시지 보내기
        slack_response = send_slack_message(message)
        print(slack_response)

        # 다음 1분을 위해 데이터 초기화 (선택 사항)
        df = pd.DataFrame(columns=['Value'])

# 1의 개수를 세는 함수 실행
count_ones_and_notify()
