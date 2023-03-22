#  import pprint
import requests
import time
import hashlib
import uuid

youdao_url = 'https://openapi.youdao.com/api'

global apikey
global apiid


def kies(stat):
    global apikey
    global apiid
    if stat % 3 == 0:  # smalltran1
        apikey = 'cM1VcDIx0QGiGhTyqwO8HzFjWhvcLbKA'
        apiid = '3244a5a0ea3e9905'
    elif stat % 3 == 1:  # bigtran1
        apikey = 'WC7tVr5YmM91LeJhWpQrhnlho3YpUfr2'
        apiid = '0f57f8a0ea32e2e4'
    else:  # bigtran2
        apikey = 'uSoaMzof3c0IxoLyq1vfQ2kD9cpykLZC'
        apiid = '646258019e11725a'


def translate(word, stat):
    kies(stat)
    time_curtime = int(time.time())  # 秒级时间戳获取
    app_id = apiid  # 应用id
    uu_id = uuid.uuid4()  # 随机生成的uuid数，为了每次都生成一个不重复的数。
    app_key = apikey  # 应用密钥
    sign = hashlib.sha256(
        (app_id + word + str(uu_id) + str(time_curtime) + app_key).encode('utf-8')).hexdigest()
    data = {
        'q': word,  # 翻译文本
        'from': "auto",  # 源语言
        'to': "auto",  # 翻译语言
        'appKey': app_id,  # 应用id
        'salt': uu_id,  # 随机生产的uuid码
        'sign': sign,  # 签名
        'signType': "v3",  # 签名类型，固定值
        'curtime': time_curtime,  # 秒级时间戳
    }
    #    r = requests.get(youdao_url, params=data).json()  # 获取返回的json()内容
    #    pprint.pprint(r)
    #    if r['errorCode'] == '411':
    #        time.sleep(1)
    #        print('{Translation api hit limits : sleep}')
    #        translate(word)
    try:
        r = requests.get(youdao_url, params=data).json()
        if r['isWord']:
            print(r['basic']['explains'])
            #            pprint.pprint(r)
            return r['basic']['explains'], stat
        else:
            print("None")
            return ' ', stat
    except KeyError:
        #        print('{Translation api hit limits : sleep}')
        stat = stat + 1
        # print('Tran '+str(stat % 3 + 1)+' online')
        time.sleep(0.5)
        temp = translate(word, stat)
        return temp[0], temp[1]

#  t = 4
#  while t > 0:
#      temp = translate('query', t)
#      print(temp)
#      time.sleep(0.5)
#      t = t+1
