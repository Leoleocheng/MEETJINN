import urllib, sys
import ssl, json
import base64


AK = "kT8o0IxopsPwp8dswWCV54ww"
SK = "8jPrgXlKj7c2mvDtkeqcTQe83RhdKLzV"

# token 请求 url 与图片不一样
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials'\
       '&client_id=%s'\
       '&client_secret=%s' % (AK, SK)

def GetToken():
    request = urllib.request.Request(host)
    request.add_header('Content-Type', 'application/json; charset=UTF-8')
    response = urllib.request.urlopen(request)
    content = response.read()
    if (content):
        js = json.loads(content)
        # return js['refresh_token']
        return js['access_token']
    return Non
'''
人脸对比
'''

url = "https://aip.baidubce.com/rest/2.0/antiporn/v1/detect"

def FaceRecg(face1, token):
    f = open(face1, 'rb')
    # 参数images：图像base64编码
    img1 = base64.b64encode(f.read())
    params = {"images":img1}
    params = urllib.parse.urlencode(params).encode(encoding='UTF8')
    request_url = url + "?access_token=" + token
    request = urllib.request.Request(url=request_url, data=params)
    request.add_header('Content-Type', 'application/x-www-form-urlencoded')
    response = urllib.request.urlopen(request)
    content = response.read()
    print (content)


if __name__ == "__main__":
    FaceRecg(r'C:\Users\Administrator\Desktop\cz\项目\觅景\MEETJINN\meetjinnDJ\s1.jpeg', GetToken())      #前面两个参数是图片路径
