from jinn.connect import *
import random
from jinn.function import *
import numpy as np


for i in range(1001,1002):
    list = functionsql('select * from t_behavior where user_id=%s'%i)
    user_score_total=np.zeros(8)
    for view in list:
        timedifference=functionsql('SELECT TIMESTAMPDIFF(DAY,"%s",now()) as time'%view['active_date'])[0]
        if(timedifference['time']>0 and timedifference['time']<365):
            score=functionsql('select * from t_scenicspot_label where scenicspot_id=%s'%view['item_id'])[0]
            user_score=np.array([score['food'],score['mountain'],score['sea'],score['modern.txt'],score['history'],score['explore'],score['price'],score['number']])
            print (timedifference['time'])
            y = (1.00000006283492 + 0.0962858586497722) / (1 + (int(timedifference['time']) / 189.129070243501) ** 3.55977034757135) - 0.0962858586497722  # 四参数方程时间影响因子函数
            print (y)
            user_score=user_score*np.array(int(view['active_type']))*np.array([y])
            user_score=user_score
            user_score_total=user_score_total+user_score
    print (user_score_total[0],user_score_total[1],user_score_total[2],user_score_total[3],user_score_total[4],user_score_total[5],user_score_total[6],user_score_total[7],i)
    a='UPDATE t_user_label SET food = food+%f , mountain = mountain+%f , sea = sea+%f , modern.txt = modern.txt+%f , history = history+%f , explore = explore+%f , price = price+%f , number=number+%f WHERE user_id = %d'%(user_score_total[0],user_score_total[1],user_score_total[2],user_score_total[3],user_score_total[4],user_score_total[5],user_score_total[6],user_score_total[7],int(i))
    print (a)
    functionsql1(a)