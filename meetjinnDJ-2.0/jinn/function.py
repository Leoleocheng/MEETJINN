from jinn.connect import *
from urllib import parse, request
import requests
import json, sys, ssl
from django.utils.safestring import mark_safe
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from qiniu import Auth, put_file, etag
from PIL import ImageFont,Image,ImageDraw
import urllib.request,wave,qiniu.config,redis, random, pymysql
from aip import AipNlp,AipImageCensor,AipSpeech

cursor, conn = open1()


def save_wave_file(filename, data):
    framerate = 8000
    NUM_SAMPLES = 2000
    channels = 1
    sampwidth = 1
    TIME = 2
    '''save the date to the wavfile'''
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(sampwidth)
    wf.setframerate(framerate)
    wf.writeframes(b"".join(data))
    wf.close()

def save_wave_file1(filename, data):
    framerate = 16000
    NUM_SAMPLES = 2000
    channels = 1
    sampwidth = 1
    TIME = 2
    '''save the date to the wavfile'''
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(sampwidth)
    wf.setframerate(framerate)
    wf.writeframes(b"".join(data))
    wf.close()

def yuyinshibie(audio,type):
    save_wave_file('01.pcm', audio)
    if type==1:
        APP_ID = '14711800'
        API_KEY = 'wyDhSG366cL1zy0GxDHZtHxk'
        SECRET_KEY = 'b2WprhYbk934KjegLaMk8WRrpw4zBEbW'
    else:
        APP_ID = '14731705'
        API_KEY = 'omZGAmrmqwR9tWOMiBLLKuWH'
        SECRET_KEY = 'POzePztxjWzVvqnykHGdEygu2QFETuQC'
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    # 读取文件
    def get_file_content(filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()
    # 识别本地文件
    result=client.asr(get_file_content('01.pcm'),'pcm',8000, {'dev_pid': 1536,})
    try:
        return result['result'][0]
    except:
        return 0


def yuyinshibie1(audio):#语音唤醒
    save_wave_file1('02.pcm', audio)
    APP_ID = '14747658'
    API_KEY = 'nfuf2vifhiHDZaPsRINxGYRu'
    SECRET_KEY = '6ya5gNi0WGvskyvAVsSv82klqOt0IfRz'
    client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
    # 读取文件
    def get_file_content(filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()
    # 识别本地文件
    result=client.asr(get_file_content('02.pcm'),'pcm',8000, {'dev_pid': 1536,})
    print (result)
    try:
        return result['result'][0].encode('utf8')
    except:
        return 0



def baiduimg(s):
    """ 你的 APPID AK SK """
    APP_ID = '14440883'
    API_KEY = 'kT8o0IxopsPwp8dswWCV54ww'
    SECRET_KEY = '8jPrgXlKj7c2mvDtkeqcTQe83RhdKLzV'
    client = AipImageCensor(APP_ID, API_KEY, SECRET_KEY)

    def get_file_content(filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()
    result = client.imageCensorUserDefined(
        get_file_content(r's1.' + s))
    print (result)
    if str(result['conclusionType']) == '1':
        return ('1')
    else:
        return (result['data'][0]['msg'])


def baidutext(text):
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=kT8o0IxopsPwp8dswWCV54ww&client_secret=8jPrgXlKj7c2mvDtkeqcTQe83RhdKLzV'
    formate = {"content": text}
    data = urllib.parse.urlencode(formate).encode('utf-8')
    request = urllib.request.Request(host)
    request.add_header('Content-Type', 'application/json; charset=UTF-8')
    response = urllib.request.urlopen(request)
    content = response.read()
    if (content):
        content = eval(content.decode("utf8"))["access_token"]
        host1 = 'https://aip.baidubce.com/rest/2.0/antispam/v2/spam?access_token=' + content
        request = urllib.request.Request(host1, data)
        request.add_header('Content-Type', 'application/json; charset=UTF-8')
        response = urllib.request.urlopen(request)
        content = response.read()
        content = eval(content.decode("utf8"))
        result = content['result']
        if (result['spam'] == 0):
            return ('1')
        else:
            for i in result['review']:
                if (i['label'] == 1):
                    return ([i['hit'][0], '暴恐违禁'])
                elif (i['label'] == 2):
                    return ([i['hit'][0], '文本色情'])
                elif (i['label'] == 3):
                    return ([i['hit'][0], '政治敏感'])
                elif (i['label'] == 4):
                    return ([i['hit'][0], '恶意推广'])
                elif (i['label'] == 5):
                    return ([i['hit'][0], '低俗辱骂'])
                else:
                    return ([i['hit'][0], '低质灌水'])


def functionsql(str1):  # 数据库读
    try:
        cursor.execute(str1)
        list = cursor.fetchall()
    except:
        cursor, conn = open1()
        cursor.execute(str1)
        list = cursor.fetchall()
    return list


def functionsql1(str1):  # 数据库写
    try:
        cursor.execute(str1)
        conn.commit()
    except:
        cursor, conn = open1()
        cursor.execute(str1)
        conn.commit()
    return 1


def functioncity(str1, str2):  # 找城市名
    if (int(str1) == 1):
        list = functionsql(
            "select province_name as name1,province_img_url as img1 from t_province where province_id=" + str(str2))[0]
    elif (int(str1) == 2):
        list = functionsql(
            "select city_name as name1,city_img_url as img1,city_id as id1 from t_city where city_id=" + str(str2))[0]
    elif (int(str) == 3):
        list = functionsql(
            "select scenicspot_name as name1,scenicspot_img_url as img1 from t_scenicspot where scenicspot_id=" + str(
                str2))[0]
    return list


def obtainverificationcode(phone, ver):  # 发送验证码
    textmod = {"sid": "a24d38b947a9dab64cbfabfbd314333e", "token": "92f7634dbfc3d8efc188254a7c567a39",
               "appid": "1fdbe8c03fea4322b3a9eaa7218b5914", "templateid": "389809", "param": ver,
               "mobile": phone}
    textmod = json.dumps(textmod).encode(encoding='utf-8')
    header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
                   "Content-Type": "application/json"}
    url = 'http://192.168.199.10/api_jsonrpc.php'
    req = request.Request(url='https://open.ucpaas.com/ol/sms/sendsms', data=textmod, headers=header_dict)
    res = request.urlopen(req)
    res = res.read()
    return 1


def weather(name):  # 获取天气
    url = 'http://v.juhe.cn/weather/index?format=2&cityname=' + name + '&key=6793e3d7bdff920ec2ae5a75511ef80c'
    r = requests.get(url)
    w = [[1, 2], [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 19, 21, 22, 23, 24, 25], [13, 14, 15, 16, 17, 26, 27, 28]]
    fa = int(r.json()["result"]["today"]["weather_id"]["fa"])
    fb = int(r.json()["result"]["today"]["weather_id"]['fb'])
    if (fa in w[0] or fb in w[0]):
        return 1
    elif (fa in w[1] or fb in w[1]):
        return 2
    elif (fa in w[2] or fb in w[2]):
        return 3
    else:
        return 4


def qiniuyun(key, a, s,username):
    access_key = 'O4uhB24lIhk5B_VR1Tj6IQ1pF0kKA18aIpEzs3Kv'
    secret_key = 'aEEnRGPsAGIRZCobHxBuRmao0Z3wQfi7NyQxzZJV'
    q = Auth(access_key, secret_key)
    image = Image.open(a)
    image.save('s1.' + s)
    state = baiduimg(s)
    if (state == '1'):
        draw = ImageDraw.Draw(image)
        a = image.size
        draw.text((a[0] - 120, a[1] - 40), "@"+username, (255, 255, 255))
        draw = ImageDraw.Draw(image)
        image.save('s1.' + s)
        bucket_name = 'tupian'
        localfile = r"s1." + s
        token = q.upload_token(bucket_name, key)
        ret, info = put_file(token, key, localfile)
        return 'http://files.g4.xmgc360.com/' + key
    else:
        return state
