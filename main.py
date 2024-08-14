import requests
import json
import pandas as pd
import random
import time

# Slack 웹훅 URL (예시 URL, 실제로 사용 시 본인의 URL로 교체하세요)
slack_url = "slack api"

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

# 실시간 데이터를 저장할 DataFrame 초기화
df = pd.DataFrame(columns=['Value'])

# 데이터를 실시간으로 추가하는 함수
def update_data():
    new_value = random.choice([0, 1])  # 0 또는 1을 랜덤으로 생성
    new_row = pd.DataFrame({'Value': [new_value]})
    return new_row

# 1분 동안 1의 개수를 세는 함수
def count_ones_and_notify():
    global df
    while True:
        start_time = time.time()
        while time.time() - start_time < 60:  # 1분 동안 데이터를 수집
            new_data = update_data()
            df = pd.concat([df, new_data], ignore_index=True)  # 새로운 데이터를 DataFrame에 추가
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
