import base64
import hashlib
import hmac
import json
import time
import urllib

import requests
from bs4 import BeautifulSoup

prefixUrl = "https://oapi.dingtalk.com/robot/send?access_token="
token = "这里输入群机器人的token"
secret = "这里输入群机器人的secret"

ddHeaders = {'content-type': 'application/json'}
url = "https://www.zhihu.com/billboard"
zhHeaders = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/58.0.3029.110 Safari/537.36 '
}
jsonData = {}
contentList = []
links = []
requestData = {}


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


if __name__ == '__main__':
    source_html = requests.get(url, headers=zhHeaders)
    source_html.encoding = source_html.apparent_encoding
    parsed_html = BeautifulSoup(source_html.text, "html.parser")
    html_text = parsed_html.prettify()
    for data in parsed_html.findAll("script"):
        if data.get('id') == 'js-initialData':
            jsonData = json.loads(data.text)
            contentList = jsonData['initialState']['topstory']['hotList']

    for content in contentList[:10]:
        temp = {"title": content['target']['titleArea']['text'], "messageURL": content['target']['link']['url'],
                "picURL": content['target']['imageArea']['url']}
        links.append(temp)

    create_data()
    post_message()
