import requests
import json
import pandas as pd
import time

url = "Flask 서버의 주소와 포트"

# Slack 웹훅 URL
slack_url = "slack 웹 훅"

def send_slack_message(message):
    headers = {
        "Content-type": "application/json"
    }

    data = {
        "text": message
    }

    res = requests.post(slack_url, headers=headers, data=json.dumps(data))

    if res.status_code == 200:
        return "Message sent successfully"
    else:
        return f"Failed to send message, status code: {res.status_code}"

def get_gyro_data():
    try:
        # POST 요청 보내기
        response = requests.post(url)

        # 응답이 성공적이면 JSON 데이터를 가져옴
        if response.status_code == 200:
            data = response.json()
            avg_x = data['AvgX']
            avg_y = data['AvgY']
            avg_z = data['AvgZ']
            return (avg_x + avg_y + avg_z) / 3  # XYZ 평균값 계산
        else:
            print(f"Error: Received status code {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

# 실시간 데이터를 저장할 DataFrame 초기화
df = pd.DataFrame(columns=['Value'])

# 데이터를 실시간으로 추가하는 함수
def update_data():
    avg_value = get_gyro_data()
    if avg_value is not None:
        if avg_value > 0.5:
            new_value = 1
            send_slack_message("척추를 똑바로 하세요!")  # 알림 전송
        else:
            new_value = 0
        new_row = pd.DataFrame({'Value': [new_value]})
        return new_row
    else:
        return pd.DataFrame({'Value': []})  # 데이터가 없으면 빈 DataFrame 반환

# 1분 동안 1의 개수를 세는 함수
def count_ones_and_notify():
    global df
    while True:
        start_time = time.time()
        while time.time() - start_time < 600:  # 10분 동안 데이터를 수집
            new_data = update_data()
            if not new_data.empty:
                df = pd.concat([df, new_data], ignore_index=True)  # 새로운 데이터를 DataFrame에 추가
            time.sleep(0.5)  # 500ms마다 데이터를 수집

        # 10분 동안 1의 개수를 세기
        ones_count = df['Value'].sum()  # 10의 개수 합계
        message = f"지난 10분 동안 자세가 {ones_count}번 흐트러졌습니다."
        print(message)

        # 슬랙으로 메시지 보내기
        slack_response = send_slack_message(message)
        print(slack_response)

        # 다음 1분을 위해 데이터 초기화 (선택 사항)
        df = pd.DataFrame(columns=['Value'])

# 1의 개수를 세는 함수 실행
count_ones_and_notify()

