import requests
import json
import hashlib
import time


def weChatRequest(url, encoding="urf-8"):
    try:
        response = requests.get(url)
        response.encoding = encoding
        if response.status_code == 200: return response.json()
    except json.JSONDecodeError:
        return {}


def getUTCtimesmap():
    """
    获取当前UTC时间的时间戳
    :return:
    """
    return str(int(round(time.time() * 1000)))


def getMd5EncodeData(string: str):
    """
    Md5加密字符串
    :param string:
    :return:
    """
    hash_md5 = hashlib.md5(string.encode('utf-8')).hexdigest()
    return hash_md5