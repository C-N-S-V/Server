import requests
import json

slack_url = "api여기다가 쓰기"

def sendSlackhook(strText):
    headers={
        "Content-type" : "application/json"
    }

    data={
        "text" : strText
    }

    res = requests.post(slack_url, headers=headers, data=json.dumps(data))

    if res.status_code == 200:
        return "ok"
    else:
        return "error"


print(sendSlackhook("테스트용 메세지"))