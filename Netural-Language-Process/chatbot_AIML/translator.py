# /usr/bin/env python
# coding = utf8

import http.client as httplib
import hashlib
import urllib.request
import urllib.error
import random


def translator(q, fromLang="en", toLang="zh"):

    appid = ''
    secretKey = ''

    httpClient = None
    myurl = '/api/trans/vip/translate'
    salt = random.randint(32768, 65536)

    sign = appid + q + str(salt) + secretKey
    sign = sign.encode('utf-8')
    m1 = hashlib.md5(sign)
    # m1.update(sign)
    sign = m1.hexdigest()
    myurl = myurl + '?appid=' + appid + '&q=' + \
        urllib.request.quote(q) + '&from=' + fromLang + '&to=' + toLang + \
        '&salt=' + str(salt) + '&sign=' + sign

    httpClient = httplib.HTTPConnection('api.fanyi.baidu.com')
    httpClient.request('GET', myurl)

    # response是HTTPResponse对象
    response = httpClient.getresponse()

    get = response.read()
    # print(type(get))
    get = get.decode("utf-8")
    get = eval(get)
    # print(get)

    if httpClient:
        httpClient.close()
    
    # print(get.keys())
    if "trans_result" not in get.keys():
        if toLang == "en":
            return "ERROR!"
        else:
            return "错误！"
    else:
        return get['trans_result'][0]['dst']


if __name__ == "__main__":

    get_1 = translator("你是谁", fromLang="zh", toLang="en")
    print(get_1)
    get_2 = translator("Hi nice to see you!")
    print(get_2)
    # print(type(get))
