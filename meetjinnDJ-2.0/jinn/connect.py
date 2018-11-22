import redis,pymysql


# r = redis.Redis(host='112.74.171.152', port=6379, user='root', passwd='Cz292994')
def open1():
    conn=pymysql.connect(host='112.74.171.152', port=3306, user='root', passwd='Cz292994', db='meetjinn', charset='utf8')
    cursor=conn.cursor(pymysql.cursors.DictCursor)
    return cursor,conn