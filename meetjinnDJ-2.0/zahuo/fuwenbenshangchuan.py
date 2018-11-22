from django.utils.safestring import mark_safe
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import redis, random, pymysql
from qiniu import Auth, put_file, etag
import qiniu.config
from PIL import Image

access_key = 'O4uhB24lIhk5B_VR1Tj6IQ1pF0kKA18aIpEzs3Kv'
secret_key = 'aEEnRGPsAGIRZCobHxBuRmao0Z3wQfi7NyQxzZJV'
q = Auth(access_key, secret_key)
bucket_name = 'tupian'
localfile = r"s1.jpg"




def ceshi(request):
    if request.method == 'GET':
        return render(request, 'index.html')
    else:
        a = request.FILES.get('imageData')
        image = Image.open(a)
        image.save('s1.jpg')
        key='ceshi5431.jpg'
        token = q.upload_token(bucket_name, key)
        ret, info = put_file(token, key, localfile)
        print(a,123)
        return HttpResponse('http://files.g4.xmgc360.com/'+key)