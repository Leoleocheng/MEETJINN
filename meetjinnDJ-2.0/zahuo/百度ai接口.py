import urllib, sys
import ssl
from urllib import parse, request
import base64



with open(r"C:\Users\Administrator\Desktop\cz\项目\觅景\MEETJINN\meetjinnDJ\s1.jpeg") as f:
    # b64encode是编码，b64decode是解码
    base64_data = base64.b64encode(f.read())
    print(base64_data)
# client_id 为官网获取的AK， client_secret 为官网获取的SK
textmod = {"img": base64_data}
textmod = json.dumps(textmod).encode(encoding='utf-8')
header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
               "Content-Type": "application/json"}


host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=kT8o0IxopsPwp8dswWCV54ww&client_secret=8jPrgXlKj7c2mvDtkeqcTQe83RhdKLzV'

req = request.Request(url=host, data=textmod, headers=header_dict)
res = request.urlopen(req)
res = res.read()



