import requests
import json


def weChatRequest(url, encoding="urf-8"):
    try:
        response = requests.get(url)
        response.encoding = encoding
        if response.status_code == 200: return response.json()
    except json.JSONDecodeError:
        return {}
