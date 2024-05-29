import requests
import json
import time

# 슬랙 웹훅 URL을 여기에 입력하세요
slack_url = "https://hooks.slack.com/services/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"


def sendSlackhook(strText):
    headers = {
        "Content-type": "application/json"
    }

    data = {
        "text": strText
    }

    res = requests.post(slack_url, headers=headers, data=json.dumps(data))

    if res.status_code == 200:
        return "warning"
    else:
        return "error"


def get_data_from_sensor(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # HTTP 에러가 발생하면 예외를 일으킴
        return response.json()  # JSON 데이터를 반환
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None


# 센서 데이터를 가져올 URL
url = "http://192.168.185.24:5001/data"

while True:
    sensor_data = get_data_from_sensor(url)
    if sensor_data:
        # 데이터 값이 1인 경우 슬랙 알림 전송
        if sensor_data.get("value") == 1:
            message = "척추를 똑바로 하세요"
            print(sendSlackhook(message))
    time.sleep(1)