from jinn.connect import *
import random
from jinn.function import *
cursor,conn = open()


for i in range(1,46):
    str1=[]
    for j in range(8):
        str1.append(str(random.randint(1,10)))
    functionsql1('insert into t_scenicspot_label value(%s,%s,%s,%s,%s,%s,%s,%s,%s)'%(str1[0],str1[1],str1[2],str1[3],i,str1[4],str1[5],str1[6],str1[7]))

