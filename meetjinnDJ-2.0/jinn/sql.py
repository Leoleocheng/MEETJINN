from jinn.function import *
import markdown
import html2text as ht

homepage1 = 'select city_name,city_img_url,city_id from t_city ORDER BY city_degree DESC LIMIT 0,6'

companions1 = 'select city_name,city_img_url,city_companions,city_id from t_city ORDER BY city_companions DESC LIMIT 0,6'
companions2 = "SELECT a.*,b.user_name,b.user_img,b.user_id,c.* FROM t_companions  a,t_user  b,t_city c WHERE a.companions_user_id=b.user_id AND a.companions_city_id=c.city_id and c.city_name='稻城'"


def companions3(str1):
    companions3 = "SELECT a.*,b.user_name,b.user_img,b.user_id,c.* FROM t_companions  a,t_user  b,t_city c WHERE a.companions_user_id=b.user_id AND a.companions_city_id=c.city_id and c.city_name='%s'" % str1
    return (companions3)


def companionsotes1(a):
    b = "select a.user_img,a.user_name,b.*,DATE_FORMAT(b.companions_date,'%Y-%m-%d') as time1 from t_user a,t_companions b where a.user_id=b.companions_user_id and b.companions_id=" + a
    return b


qa1 = '''select a.*,b.*,c.user_name,c.user_id,c.user_img,(CASE WHEN LENGTH(a.answer_md)>80 THEN CONCAT(SUBSTRING(a.answer_md,1,80),'...') ELSE a.answer_md END)as md1,
DATE_FORMAT(a.answer_time,'%Y-%m-%d %h:%s') as time1 from t_answer a,t_problem b,t_user c,t_city d where b.problem_id=a.answer_problem_id and a.answer_user_id=c.user_id and b.problem_place_id=d.city_id GROUP BY a.answer_problem_id ORDER BY sum(a.answer_fabulous) DESC '''

qa2 = "select city_name,city_problem,city_id from t_city ORDER BY city_problem DESC LIMIT 0,6"


# 问题按热度排序
def qa3(a):
    b = '''select a.*,b.*,c.user_name,c.user_id,c.user_img,(CASE WHEN LENGTH(a.answer_md)>80 THEN CONCAT(SUBSTRING(a.answer_md,1,80),'...') ELSE a.answer_md END)as md1,DATE_FORMAT(a.answer_time,'%Y-%m-%d %h:%s') as time1 from t_answer a,t_problem b,t_user c,t_city d where b.problem_id=a.answer_problem_id and a.answer_user_id=c.user_id and b.problem_place_id=d.city_id and b.problem_title like "%''' + a + '''%"  GROUP BY a.answer_problem_id ORDER BY sum(a.answer_fabulous) desc'''
    return b


# 问题按时间排序
def qa4(a):
    b = '''select a.*,b.*,c.user_name,c.user_id,c.user_img,(CASE WHEN LENGTH(a.answer_md)>80 THEN CONCAT(SUBSTRING(a.answer_md,1,80),'...') ELSE a.answer_md END)as md1,
        DATE_FORMAT(a.answer_time,'%Y-%m-%d %h:%s') as time1 from t_answer a,t_problem b,t_user c,t_city d where b.problem_id=a.answer_problem_id and a.answer_user_id=c.user_id and b.problem_place_id=d.city_id and b.problem_title like "%''' + a + '''%"  GROUP BY a.answer_problem_id ORDER BY b.problem_time DESC'''
    return b


# 按照月份查询
# 默认一月
search1 = "SELECT scenicspot_name,scenicspot_img_url from t_scenicspot where scenicspot_id in (select comment_object_id from t_comment where date_format(comment_time,'%m')='01' and comment_type=3 GROUP BY  comment_object_id ORDER BY COUNT(comment_id) DESC)"


# 其他月份

def search2(str):
    str = "'" + str + "'" if len(str) > 1 else "'0" + str + "'"
    return "SELECT scenicspot_name,scenicspot_img_url,scenicspot_id from t_scenicspot where scenicspot_id in (select comment_object_id from t_comment where date_format(comment_time,'%m')=" + str + " and comment_type=3 GROUP BY  comment_object_id ORDER BY COUNT(comment_id) DESC) LIMIT 0,6"


def region1(a):
    b = "select city_name,city_describe,city_id from t_city where city_id=%d" % int(a)
    return b


def region2(a):
    b = "select scenicspot_name,scenicspot_img_url,(CONCAT(SUBSTRING(scenicspot_md,13,100),'...')) as md,scenicspot_id from t_scenicspot where scenicspot_city_id=%d ORDER BY scenicspot_comment DESC LIMIT 0,5" % int(
        a)
    return b


def region3(a):
    b = "select a.*,b.user_name,b.user_img,DATE_FORMAT(a.travels_time,'%Y-%m-%d %h:%s') as time1, (CONCAT(SUBSTRING(a.travels_md,1,80),'...')) as md from t_travels a,t_user b where a.travels_user_id=b.user_id and a.travels_region_id=" + a + " and a.travels_region_type=2;"
    return b


def region4(a):
    b = '''select  a.*,c.*,d.user_name,d.user_id,d.user_img, 
(CASE WHEN LENGTH(a.answer_md)>80 
THEN CONCAT(SUBSTRING(a.answer_md,1,80),'...') 
ELSE a.answer_md END)as md1,DATE_FORMAT(a.answer_time,'%Y-%m-%d %h:%s') as time1   
from (select * from t_answer as a   
where  answer_fabulous=(select max(b.answer_fabulous)  
from t_answer as b  
where a.answer_problem_id = b.answer_problem_id and a.answer_problem_id in (select problem_id from t_problem where problem_place_id=''' + a + ''' and problem_type=2 order by problem_browse desc))
) as a,t_problem  c,t_user d where a.answer_problem_id=c.problem_id and a.answer_user_id=d.user_id  
group by answer_problem_id'''
    return b


travels1 = "select a.user_img,a.user_name,b.*,DATE_FORMAT(b.travels_date,'%Y-%m-%d') as time1,(CASE WHEN LENGTH(b.travels_md)>100 THEN CONCAT(SUBSTRING(b.travels_md,1,100),'...') ELSE b.travels_md END)as md1 from t_user a,t_travels b where b.travels_user_id=a.user_id ORDER BY b.travels_collection DESC limit 0,6"


def travels2(city_id):
    b = "select a.user_img,a.user_name,b.*,DATE_FORMAT(b.travels_date,'%Y-%m-%d') as time1,(CASE WHEN LENGTH(b.travels_md)>80 THEN CONCAT(SUBSTRING(b.travels_md,1,80),'...') ELSE b.travels_md END)as md1 from t_user a,t_travels b where b.travels_user_id=a.user_id and b.travels_region_id=" + str(
        city_id) + " and b.travels_region_type=2 ORDER BY b.travels_collection DESC limit 0,6"
    return b


def travelnotes1(a):
    b = "select a.user_img,a.user_name,b.*,DATE_FORMAT(b.travels_date,'%Y-%m-%d %h:%m') as time1,DATE_FORMAT(b.travels_time,'%Y-%m-%d %h:%m') as time2 from t_user a,t_travels b where a.user_id=b.travels_user_id and b.travels_id=" + a
    return b


def listmain1(a):
    b = 'select b.city_name,b.city_img_url,a.list_order,b.city_id from t_list a,t_city b where a.list_city_id=b.city_id and a.list_type=' + a + ' ORDER BY a.list_order'
    return b


def listmain2(a):
    b = 'select public_type_name from t_public_type where public_type_type="榜单" and public_type_id=' + a
    return b


def scenicspot1(a):
    b = 'select * from t_scenicspot where scenicspot_id=' + a
    return b


def scenicspot2(a):
    b = "select a.*,b.user_name,b.user_img,DATE_FORMAT(a.comment_time,'%Y-%m-%d %h:%m') as time1 from t_comment a,t_user b where a.comment_user_id=b.user_id and a.comment_type=4 and a.comment_object_id=" + a
    return b


def verificationcode1(phone, ver):
    state = functionsql("select ver_id from t_verification where ver_phone=" + phone)
    if (state):
        b = 'UPDATE t_verification SET ver_verification = ' + str(
            ver) + ' , ver_expiry=(SELECT date_add(NOW(), interval 3 minute)) WHERE ver_id = ' + str(state[0]['ver_id'])
    else:
        b = 'INSERT INTO `meetjinn`.`t_verification` (ver_phone,ver_verification,ver_expiry) VALUES ("%s",%d,(SELECT date_add(NOW(), interval 3 minute)))' % (
        phone, int(ver))
    return b


def wtn1(html, img, title, place, userid, consumption, date):
    text_maker = ht.HTML2Text()
    text_maker.bypass_tables = False
    md = text_maker.handle(html)
    a = functionsql('select city_id from t_city where city_name="%s"' % place)[0]
    b = 'insert into t_travels(travels_title,travels_md,travels_user_id,travels_time,travels_collection,travels_region_type,travels_region_id,travels_img_url,travels_date,travels_cost) value ("%s","%s",%d,now(),0,2,%d,"%s","%s",%d)' % (
    str(title), str(md), int(userid), int(a['city_id']), str(img), date, int(consumption))
    return b


def releasecompanions1(html, img_url, title, place, userid, date, expect, time, phone):
    text_maker = ht.HTML2Text()
    text_maker.bypass_tables = False
    md = text_maker.handle(html)
    a = functionsql('select city_id from t_city where city_name="%s"' % place)[0]['city_id']
    b = 'insert into t_companions(companions_title,companions_md,companions_user_id,companions_time,companions_collection,companions_city_id,companions_img_url,companions_date,companions_people_expect,companions_people,companions_phone' \
        ',companions_inserttime) value ("%s","%s",%d,%d,0,%d,"%s","%s",%d,0,"%s",now())' % (
        str(title), str(md), int(userid), int(time), a, img_url, date, int(expect), phone)
    return b


def issues1(title, text, place, userid, label):
    a = functionsql('select city_id from t_city where city_name="%s"' % place)[0]
    b = 'insert into t_problem(problem_title,problem_text,problem_user_id,problem_time,problem_place_id,problem_type,problem_browse,problem_label) value("%s","%s",%d,now(),%d,2,0,%s)' % (
    title, text, userid, a["city_id"], label)
    return b


def answer(x, i, j):
    b = "select a.*,u.user_name,u.user_img from t_answer as a,t_user as u where a.answer_problem_id=%d  " \
        "and a.answer_user_id=u.user_id order by a.answer_fabulous desc limit %d,%d" % (int(x), int(i), int(j))
    return b


# 这个回答的总赞数
def answerfabulous(answerid):
    a = "SELECT count(*) FROM `t_answer_fabulous` where answer_fabulous_answer_id=%d" % int(answerid)
    return a


# 用户赞这个回答的次数（0或1）
def userfabulous(userid, answerid):
    a = "SELECT count(*) FROM `t_answer_fabulous` where answer_fabulous_user_id=%d  and answer_fabulous_answer_id=%d" \
        % (int(userid), int(answerid))
    return a


# 获取赞行为id
def fabulousid(userid, answerid):
    a = "select answer_fabulous_id from `t_answer_fabulous` where answer_fabulous_user_id=%d  and answer_fabulous_answer_id=%d" % (
        int(userid), int(answerid))
    return a


def writecomment(userid, newcomment, answerid):
    a = "insert into t_comment(comment_text,comment_user_id,comment_time,comment_fabulous,comment_object_id,comment_type) values('%s',%d,now(),0,%d,2)" % (
    newcomment, int(userid), int(answerid))
    return a

def writecomment1(userid,newcomment,answerid,type):
    a="insert into t_comment(comment_text,comment_user_id,comment_time,comment_fabulous,comment_object_id,comment_type) values('%s',%d,now(),0,%d,%d)"%(newcomment,int(userid),int(answerid),int(type))
    return a


def problem(x):
    b = "SELECT * FROM t_problem where problem_id=%d " % int(x)
    return b


def comment1(x, y):  # 评论类型 评论的对象
    a = "SELECT c.*,u.user_name,u.user_img FROM t_comment as c,t_user as u where c.comment_type = %d and c.comment_object_id = %d and u.user_id=c.comment_user_id order by c.comment_fabulous desc " % (
    x, int(y))
    return a


# 获取用户头像等信息
def user(userid):
    a = "select user_name,user_img FROM t_user where user_id=%d" % int(userid)
    return a


def house1(userid):
    a="select s.* from t_scenicspot as s,t_scenicspot_collection as c where c.scenicspot_collection_user_id=" + str(userid) + " and c.scenicspot_collection_scenicspot_id=s.scenicspot_id"
    return a