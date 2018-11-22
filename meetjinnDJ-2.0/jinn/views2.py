from django.shortcuts import render, redirect, HttpResponse
from django.utils.safestring import mark_safe
import pymysql.cursors
from random import randint
from jinn.connect import *
from jinn.sql import *
from jinn.function import *
from algorithm.bayes import *
import imghdr
import markdown

cursor, conn = open1()


# personalcenter
def index(request):
    # userid=request.session['user_id']
    userid = 1
    # 游记数
    TravelsNumber = functionsql("select count(*) from t_travels where travels_user_id=%d" % int(userid))[0]["count(*)"]
    # 用户信息
    user_list = functionsql("select user_name,user_img,user_sex from t_user where user_id=%d" % int(userid))[0]
    # 提问数
    ProblemNumber = int(functionsql("select count(*) from t_problem where problem_user_id=%d" % int(userid))[0]["count(*)"])
    # 回答数
    AnswerNumber = int(functionsql("select count(*) from t_answer where answer_user_id=%d" % int(userid))[0]["count(*)"])
    APNumber = ProblemNumber + AnswerNumber
    # 结伴数
    CompanionsNumber = functionsql("select count(*) from t_companions where companions_user_id=%d" % int(userid))[0]["count(*)"]
    # 收藏数
    # 结伴收藏
    collection1 = int(functionsql("select count(*) from t_companions_collection where companions_collection_user_id=%d" % int(userid))[0]["count(*)"])
    # 游记收藏
    collection2 = int(functionsql("select count(*) from t_travels_collection where travels_collection_user_id=%d" % int(userid))[0]["count(*)"])
    # 图片收藏
    collection3 = int(functionsql("select count(*) from t_collectimg where collect_user_id=%d" % int(userid))[0]["count(*)"])
    CollectionNumber = collection1 + collection2 + collection3

    return render(request, 'index.html', {'user_list': user_list, "TravelsNumber": TravelsNumber, "APNumber": APNumber,
                                          "CompanionsNumber": CompanionsNumber, "CollectionNumber": CollectionNumber})


# 我的收藏
def house(request):
    try:
        userid = request.session['user_id']
    except:
        return render(request, 'register.html')
    if request.method == "GET":
        # 用户信息
        user_list = functionsql("select user_name,user_img,user_sex from t_user where user_id=%d" % int(userid))[0]
        # 结伴收藏
        companions_collection = functionsql("select com.* from t_companions_collection as collect,t_companions as com where collect.companions_collection_user_id=%d and collect.companions_collection_companions_id=com.companions_id" % int(userid))
        # 游记收藏
        travels_collection=functionsql("select tra.* from t_travels as tra,t_travels_collection as collect where collect.travels_collection_user_id=%d and collect.travels_collection_travels_id=tra.travels_id" % int(userid))
        for travels in travels_collection:
            user_list2 =functionsql("select user_name,user_img,user_sex,user_id from t_user where user_id=%d" % int(travels["travels_user_id"]))[0]
            travels["user_id"] = user_list2["user_id"]
            travels["user_img"] = user_list2["user_img"]
            travels["user_name"] = user_list2["user_name"]
            html = markdown.markdown(travels["travels_md"])
            reg = re.compile('<[^>]*>')
            text = reg.sub('', html)
            if len(text) > 200:
                shorttext = text[0:200] + "。。。"
            else:
                shorttext = text
            travels["shorttext"] = shorttext
        # imglist=cursor.fetchall()
        # 景点收藏
        scenicspot_list = functionsql(house1(userid))
        count_scenicspot=functionsql('select count(scenicspot_collection_user_id) as count1 from t_scenicspot_collection where scenicspot_collection_user_id='+str(userid))[0]['count1']
        count_travels = functionsql('select count(travels_collection_user_id) as count1 from t_travels_collection where travels_collection_user_id=' + str(userid))[0]['count1']
        return render(request, 'house.html',
                      {'companions_collection': companions_collection, "travels_collection": travels_collection,
                       "user_list": user_list, "scenicspot_list": scenicspot_list,'count_scenicspot':count_scenicspot,'count_travels':count_travels})
    else:
        type1 = request.POST.get("type")
        if type1 == "ScenicspotCollect":
            scenicspotid = request.POST.get("scenicspotid")
            jiajian = request.POST.get('jiajian')
            # 景点收藏加1
            if int(jiajian) == 1:
                functionsql1("insert into t_scenicspot_collection(scenicspot_collection_user_id,scenicspot_collection_scenicspot_id) value (%d,%d)" % (
                    int(userid), int(scenicspotid)))
            # 景点收藏减1
            else:
                functionsql1("delete from t_scenicspot_collection where scenicspot_collection_user_id=%d and scenicspot_collection_scenicspot_id=%d" % (
                    int(userid), int(scenicspotid)))
            return HttpResponse(1)
        elif type1 == "TravelsidCollect":
            travelsid = request.POST.get("travelsid")
            jiajian = request.POST.get('jiajian')
            # 游记收藏加1
            if int(jiajian) == 1:
                functionsql1("insert into t_travels_collection(travels_collection_user_id,travels_collection_travels_id) value (%d,%d)" % (
                    int(userid), int(travelsid)))
                functionsql1("update t_travels set travels_collection=travels_collection+1 where travels_id=%d" % int(travelsid))
            # 游记收藏减1
            else:
                functionsql1("delete from t_travels_collection where travels_collection_user_id=%d and travels_collection_travels_id=%d" % (
                    int(userid), int(travelsid)))
                functionsql1("update t_travels set travels_collection=travels_collection-1 where travels_id=%d" % int(travelsid))
            return HttpResponse(1)


def interlocution(request):
    try:
        userid = request.session['user_id']
    except:
        return render(request, 'register.html')
    if request.method == "GET":
        # 用户信息
        user = functionsql("select user_name,user_img,user_sex from t_user where user_id=%d" % int(userid))[0]
        # 我的提问
        problem_list = functionsql("select * from t_problem where problem_user_id=%d" % int(userid))
        for problem in problem_list:
            title = problem["problem_title"]
            if len(title) > 200:
                shorttitle = title[0:200] + "。。。"
            else:
                shorttitle = title
            problem["shorttitle"] = shorttitle
        # 提问数
        problem_number = functionsql("select count(*) as count from t_problem where problem_user_id=%d" % int(userid))[0]["count"]
        # 我的回答
        answer_list = functionsql("select a.*,p.* from t_answer as a,t_problem as p where a.answer_user_id=%d and p.problem_id=a.answer_problem_id" % int(
                userid))

        for answer in answer_list:
            html = markdown.markdown(answer["answer_md"])
            reg = re.compile('<[^>]*>')
            text = reg.sub('', html)
            if len(text) > 200:
                shorttext = text[0:200] + "。。。"
            else:
                shorttext = text
            answer["shorttext"] = shorttext
        # 回答数
        answer_number = functionsql("select count(*) as count from t_answer where answer_user_id=%d" % int(userid))[0]["count"]
        print(problem_list)
        return render(request, 'interlocution.html', {'problem_list': problem_list, "problem_number": problem_number,
                                                      "answer_list": answer_list, "answer_number": answer_number,
                                                      "user": user})
    else:
        pass


def plans(request):
    try:
        userid = request.session['user_id']
    except:
        return render(request, 'register.html')

    if request.method == "GET":
        user = functionsql("select count(a.travels_id) as count,b.user_name,b.user_img,b.user_sex from t_travels a,t_user b where b.user_id=a.travels_user_id and b.user_id=%d" % (
                int(userid)))[0]
        travels_list = functionsql("select * from t_travels where travels_user_id=%d" % int(userid))
        for travels in travels_list:
            travels["travels_divid"] = "div-" + str(travels["travels_id"])
            html = markdown.markdown(travels["travels_md"])
            reg = re.compile('<[^>]*>')
            text = reg.sub('', html)
            if len(text) > 200:
                shorttext = text[0:200] + "。。。"
            else:
                shorttext = text
            travels["shorttext"] = shorttext
        return render(request, 'plans.html', {'user': user, "travels_list": travels_list})
    else:
        travelsid = request.POST.get("travelsid")
        functionsql('delete from t_travels_collection where travels_collection_travels_id=%d'%int(travelsid))
        functionsql1("delete from t_travels where travels_id=%d" % int(travelsid))
        return HttpResponse(1)


def biography(request):#传图片
    img = request.FILES.get('imageData')
    city_name=request.POST.get('cityname')
    key = functionsql('select sign_num from t_sign where sign_name="img"')[0]
    functionsql1('update t_sign set sign_num=sign_num+1 where sign_name="img"')
    print (img)
    suffix = imghdr.what(img)
    city_id=functionsql('select city_id from t_city where city_name="%s"'%city_name)
    try:
        city_id=city_id[0]['city_id']
        type=1
    except:
        city_id=functionsql('select scenicspot_id from t_scenicspot where scenicspot_name="%s"'%city_name)[0]['scenicspot_id']
        type=2
    userid = request.session['user_id']
    username=request.session['user_name']
    img_url = qiniuyun('img' + str(key['sign_num']) + '.' + suffix, img, suffix,username)
    if(type==1):
        functionsql1("INSERT INTO `meetjinn`.`t_img` (`img_time`, `img_url`, `img_province_id`,`img_city_id`, `img_user_id`, `img_collection`) VALUES (now(),'%s', '1',%s, %s, '0')"%(img_url,str(city_id),str(userid)))
    else:
        functionsql1("INSERT INTO `meetjinn`.`t_img` (`img_time`, `img_url`, `img_province_id`, `img_scenicspot_id`, `img_user_id`, `img_collection`) VALUES (now(),'%s', '1',%s, %s, '0')"%(img_url,str(city_id),str(userid)))
    return redirect('/myimg/')




def myimg(request):#图片
    try:
        userid = request.session['user_id']
    except:
        return render(request, 'register.html')

    if request.method == "GET":
        # 用户信息
        user = functionsql("select user_name,user_img,user_sex from t_user where user_id=%d" % int(userid))[0]
        # 我上传的图片
        myimgList = functionsql("select img_id,img_url,DATE_FORMAT(img_time,'%Y年%m月') as img_time,img_collection from t_img where img_user_id=" + str(
                userid) + " order by img_time desc")
        for img in myimgList:
            img["divmyimgid"] = "div-" + str(img["img_id"])
        TimeLen = len(myimgList)
        yearmonthList = []
        if TimeLen >= 1:
            kong = []
            myimgList[0]["index"] = 0
            kong.append(myimgList[0])
            # 遍历每个图
            for i in range(1, TimeLen):
                if myimgList[i]["img_time"] == myimgList[i - 1]["img_time"]:
                    myimgList[i]["index"] = myimgList[i - 1]["index"] + 1
                    kong.append(myimgList[i])
                    if i == TimeLen - 1:
                        yearmonthList.append(kong)

                if myimgList[i]["img_time"] != myimgList[i - 1]["img_time"]:
                    myimgList[i]["index"] = 0
                    yearmonthList.append(kong)
                    kong = [myimgList[i]]
                    if i == TimeLen - 1:
                        yearmonthList.append(kong)
        if TimeLen == 1:
            kong = []
            kong.append(myimgList[0])
            yearmonthList.append(kong)
        # 我收藏的图片
        mycollectimgList = functionsql("select c.*,i.img_id,i.img_url from t_collectimg as c,t_img as i where c.collect_user_id=%d and i.img_id=c.img_id order by c.collect_img_time" % int(
                userid))
        count=functionsql('select count(img_id) as count from t_img where img_user_id='+str(userid))[0]['count']
        count_collection = functionsql('select count(img_id) as count from t_collectimg where collect_user_id=' + str(userid))[0]['count']
        return render(request, "myimg.html",
                      {"user": user, "yearmonthList": yearmonthList, "mycollectimgList": mycollectimgList,'count':count,'count_collection':count_collection})
    else:
        print(33)
        type1 = request.POST.get("type")
        if type1 == "DeleteImg":
            imgid = request.POST.get("imgid")
            functionsql1("delete from t_img where img_id=%d" % int(imgid))
            return HttpResponse(1)
        if type1 == "DeleteCollectImg":
            imgid = request.POST.get("imgid")
            jiajian = int(request.POST.get("jiajian"))
            # 添加收藏
            if jiajian == 1:
                functionsql1("insert into t_collectimg(img_id,collect_user_id,collect_img_time) value (%d,%d,(select now()))" % (
                    int(imgid), int(userid)))
            else:
                functionsql1("delete from t_collectimg where collect_user_id=%d and img_id=%d" % (int(userid), int(imgid)))
            return HttpResponse(1)


def install(request):
    try:
        userid = request.session['user_id']
    except:
        return render(request, 'register.html')
    if request.method == "GET":
        # 用户信息
        user =functionsql("select user_name,user_img,user_sex,DATE_FORMAT(user_birthday,'%Y-%m-%d') as user_birthday from t_user where user_id="+str(userid))[0]
        return render(request, "install.html", {"user": user})
    else:
        type1=request.POST.get('type')
        if(int(type1)==1):
            name=request.POST.get('user_name')
            sex=int(request.POST.get('Storage'))
            birthday=request.POST.get('birthday')
            functionsql1('UPDATE t_user SET user_name="%s",user_birthday="%s",user_sex=%s where user_id=%s'%(name,birthday,str(sex),str(userid)))
            return HttpResponse(1)
        else:
            img=request.FILES.get('img')
            print (img,type1)
            if(img):
                key = functionsql('select sign_num from t_sign where sign_name="img"')[0]
                functionsql1('update t_sign set sign_num=sign_num+1 where sign_name="img"')
                suffix = imghdr.what(img)
                img_url = qiniuyun('img' + str(key['sign_num']) + '.' + suffix, img, suffix)
                functionsql1('UPDATE t_user set user_img="%s" where user_id=%s'%(img_url,str(userid)))
                return HttpResponse(1)
            else:
                pass
            return HttpResponse(1)




def mate(request):
    try:
        userid = request.session['user_id']
    except:
        return render(request, 'register.html')


    if request.method == "GET":
        # 用户信息
        user = functionsql("select user_name,user_img,user_sex from t_user where user_id=%d" % int(userid))[0]

        # 我发起的结伴
        companions_list = functionsql("select *,DATE_FORMAT(companions_date,'%Y年%m月%d日') as companions_date2 from t_companions where companions_user_id=" + str(
                userid))
        # 我发起的结伴的数量
        companions_list_number = functionsql("select count(*) as count from t_companions where companions_user_id=" + str(userid))[0]["count"]

        # 我参加的结伴
        signup_list = functionsql("select c.*,DATE_FORMAT(c.companions_date,'%Y年%m月%d日') as companions_date2 from t_signup as s,t_companions as c where s.signup_state=1 and s.signuo_ascription_id=c.companions_id and s.signup_user_id=" + str(
                userid))
        # 我参加的结伴的数量
        signup_list_number = functionsql("select count(*) as count from t_signup where signup_state=1 and signup_user_id=" + str(userid))[0]["count"]

        # 我关注的结伴
        follow_list = functionsql("select c.*,DATE_FORMAT(c.companions_date,'%Y年%m月%d日') as companions_date2 from t_companions_follow as f,t_companions as c where f.companions_follow_companions_id=c.companions_id and f.companions_follow_user_id=" + str(
                userid))
        # 我关注的结伴的数量
        follow_list_number = functionsql("select count(*) as count from t_companions_follow where companions_follow_user_id=" + str(userid))[0]["count"]
        return render(request, "mate.html",
                      {"user": user, "companions_list": companions_list, "signup_list": signup_list,
                       "follow_list": follow_list,
                       "companions_list_number": companions_list_number, "signup_list_number": signup_list_number,
                       "follow_list_number": follow_list_number})
    else:
        pass
