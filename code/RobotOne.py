import hashlib
import time
import requests
import json
import hmac
import base64
import urllib

prefixUrl = "https://oapi.dingtalk.com/robot/send?access_token="
token = "这里输入群机器人的token"
secret = "这里输入群机器人的secret"
zhHeaders = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/58.0.3029.110 Safari/537.36 '
}
ddHeaders = {'content-type': 'application/json'}
links = []
zhihuDailyUrl = "https://news-at.zhihu.com/api/4/news/latest"
requestData = {}
jsonData = {}


def read_story():
    global jsonData
    for obj in jsonData['stories']:
        temp = {"title": obj["title"], "messageURL": obj["url"], "picURL": obj["images"][0]}
        links.append(temp)


def read_top_story():
    global jsonData
    for obj in jsonData['top_stories']:
        temp = {"title": obj["title"], "messageURL": obj["url"], "picURL": obj["image"]}
        links.append(temp)


def post_message():
    timestamp = str(int(time.time() * 1000))
    string_to_sign = timestamp + '\n' + secret
    sign_data = hmac.new(secret.encode("UTF-8"), string_to_sign.encode("UTF-8"), digestmod=hashlib.sha256)
    sign_data = base64.b64encode(sign_data.digest())
    sign = urllib.parse.quote_plus(sign_data.decode('utf-8').encode('UTF-8'))
    url_params = '&timestamp=' + timestamp + '&sign=' + sign
    request = requests.post(prefixUrl + token + url_params, json=requestData, headers=ddHeaders)
    print(request.text)


def create_data():
    global requestData
    requestData = {
        "feedCard": {
            "links": links
        },
        "msgtype": "feedCard"
    }
    print(requestData)


def get_data():
    global jsonData
    data = requests.get(zhihuDailyUrl, headers=zhHeaders)
    jsonData = json.loads(data.text)


if __name__ == '__main__':
    get_data()
    read_story()
    # read_top_story()
    create_data()
    post_message()
