from jinn.connect import *
import random
from jinn.function import *
cursor,conn = open()


for i in range(2,20000):
    # a='abcdefghijklmnopqrstuvwxyz'
    # phone='138'
    # password='123456'
    # name=str(i)
    # for j in range(7-len(str(i))):
    #     b=random.randint(0,25)
    #     name=name+a[b]
    # for k in range(8):
    #     b=random.randint(0,9)
    #     phone=phone+str(b)
    # img='http://files.g4.xmgc360.com/user.png'
    # sex=random.randint(0,1)
    year=str(random.randint(2016,2018))
    m=str(random.randint(1,12))
    day=str(random.randint(1,28))
    date=year+'-'+m+'-'+day
    print (date)
    user_id=random.randint(1,1000)
    s=random.randint(1,45)
    if(i%2==0):
        type=random.randint(1,3)
    else:
        type=1
    functionsql1('insert into t_behavior(user_id,item_id,active_type,active_date) value (%s,%s,%s,"%s")'%(user_id,s,type,date))

