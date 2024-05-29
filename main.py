import requests
import json

slack_url = "https://hooks.slack.com/services/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"

def sendSlackhook(strText):
    headers={
        "Content-type" : "application/json"
    }

    data={
        "text" : strText
    }

    res = requests.post(slack_url, headers=headers, data=json.dumps(data))

    if res.status_code == 200:
        return "warning"
    else:
        return "error"


print(sendSlackhook("척추를 똑바로 하세요"))