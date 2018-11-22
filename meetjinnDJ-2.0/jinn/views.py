from django.shortcuts import render, redirect, HttpResponse
from django.utils.safestring import mark_safe
import redis, random, pymysql
from jinn.connect import *
from jinn.sql import *
from jinn.function import *
from algorithm.bayes import *
import markdown
import html2text as ht
import jieba
import re
import numpy as np
from django.views.decorators.csrf import csrf_exempt

cursor, conn = open1()


def search(request):  # 目的地
    if request.method == 'GET':
        list = functionsql(search1)
        return render(request, 'destination.html', {'list': list})
    else:
        a = request.POST.get('data')
        a = a[0:-1]
        list = functionsql(search2(a))
        html = ''
        for view in list:
            html = html + '<div class="col-md-4 column"><a href=/scenicspot/?data=' + str(
                view['scenicspot_id']) + '><img src="' + view[
                       'scenicspot_img_url'] + '" alt="" style="width: 100%;height:215px"><div style="position: absolute; top: 0; left: 0;width: 100%;text-align: center;font-size: 1vw;color: white"><b>' + \
                   view['scenicspot_name'] + '</b></div></a></div>'
        return HttpResponse(html)


def homepage(request):  # 首页
    if request.method == "GET":
        list = functionsql(homepage1)
        list4 = functionsql('select * from t_companions order by companions_collection DESC limit 0,3')
        list1=functionsql('select a.city_name,b.* from t_city a,t_scenicspot b where a.city_id=b.scenicspot_city_id order by b.scenicspot_comment DESC limit 0,6')
        return render(request, 'homepage.html', {'list': list,'list1':list1[0],'list2':list1[1:3],'list3':list1[3:6],'list4':list4})
    else:
        city_name = request.POST.get('city')
        try:
            city_id = functionsql('select city_id from t_city where city_name="%s"' % city_name)[0]['city_id']
            return redirect('/region/?data=' + str(city_id))
        except:
            city_name = '%' + city_name + '%'
            scenicspot_id = \
                functionsql('select scenicspot_id from t_scenicspot where scenicspot_name like "%s"' % city_name)[0][
                    'scenicspot_id']
            return redirect('/scenicspot/?data=' + str(scenicspot_id))


def HanziToPinyin1(hanzi):  # 汉字转拼音
    from pypinyin import pinyin, lazy_pinyin
    return lazy_pinyin(hanzi)


def yuyinjianyan(request):  # 语音搜索
    audio = request.FILES.get('audioData')
    city_name = yuyinshibie(audio, 1)
    return HttpResponse(city_name)


def siri(request):  # siri
    audio = request.FILES.get('audioData')
    instructions = yuyinshibie(audio, 2)
    print (instructions)
    instructions=''.join(HanziToPinyin1(instructions))
    if ('youji' in instructions):
        url = '/travels/'
    elif ('mudidi' in instructions):
        url = '/search/'
    elif ('jieban' in instructions):
        url = '/companions/'
    elif ('bangdan' in instructions):
        url = '/list/'
    elif ('tuijian' in instructions):
        url = '/recommend/'
    elif (instructions in ['zhuce', 'denglu', 'xiugaimima']):
        url = '/register/'
    elif ('wenda' in instructions):
        url = '/qa/'
    elif (instructions in ['fabujieban']):
        url = '/releasecompanions/'
    elif (instructions in ['woyaotiwen']):
        url = '/issues/'
    elif (instructions in ['woyaoxieyouji']):
        url = '/wtn/'
    else:
        url = '1'
    return HttpResponse(url)


def huanxin(request):
    audio = request.FILES.get('audioData')
    instructions = yuyinshibie1(audio)
    if (instructions in ['嗨小觅', '嗨', '小觅', '小', '小米', '米', '海', '你好', '你', '好', '海小米', '海小觅', '小密你好', '小米你好', '小迷你号']):
        return HttpResponse(-1)
    else:
        return HttpResponse(1)


def companions(request):  # 结伴
    if request.method == "GET":
        list = functionsql(companions1)
        list1 = functionsql(companions2)
        return render(request, "companions.html", {'list': list, 'list1': list1})
    else:
        a = request.POST.get('data')
        list = functionsql(companions3(a))
        html = ''
        for view in list:
            html = html + '<a href="/travelnotes/?data=' + str(
                view['companions_id']) + '"><div class="col-md-3 col-6 column"><img src="' + view[
                       'companions_img_url'] + '" alt="" width="100%"><hr><h4>' + view[
                       'city_name'] + '</h4><span style="font-size: 12px">' + view[
                       'companions_title'] + '</span><br><table><tr><td><img src="' + view[
                       'user_img'] + '" class="round_icon" alt=""></td><td><span style="color: red;font-size: 20px">' + \
                   view['user_name'] + '</span></td></tr></table>期望人数' + str(
                view['companions_people_expect']) + '，' + str(view['companions_people']) + '人已报名</div></a>'
        return HttpResponse(html)


def companionsotes(request):  # 结伴详情
    if (request.method == "GET"):
        a = request.GET.get("data")
        list = functionsql(companionsotes1(a))[0]
        list['crux'] = '报名后可见'
        list['collection'] = 1
        try:
            user_id = request.session['user_id']
            signup = functionsql(
                'select signup_id from t_signup where signup_user_id=%d and signuo_ascription_id=%d' % (
                    int(user_id), int(a)))
            collection = functionsql(
                'select companions_collection_id from t_companions_collection where companions_collection_user_id=%s and companions_collection_companions_id=%s' % (
                    str(user_id), str(a)))
            if (signup):
                list['crux'] = list['companions_phone']
            if (collection):
                list['collection'] = 0
        except:
            list['collection'] = 0
            pass
        list1 = functionsql(
            'select city_name,city_img_url,city_id from t_city where city_id=' + str(list['companions_city_id']))[0]
        list['companions_md'] = mark_safe(markdown.markdown(list['companions_md']))
        list['companions_phone'] = 0
        return render(request, "companionsotes.html", {'list': list, 'list1': list1, 'a': a})
    else:
        try:
            user_id = request.session['user_id']
        except:
            return render(request, 'register.html')
        phone = request.POST.get("phone")
        sex = 1 if request.POST.get("sex") else 0
        text = request.POST.get("text")
        user_name = request.session['user_name']
        a = request.POST.get("a")
        functionsql1(
            "insert into t_signup(signup_user_id,signup_text,signuo_ascription_id,signup_phone,signup_sex) value(%d,'%s',%d,'%s',%d)" % (
                int(user_id), text, int(a), phone, int(sex)))
        return redirect('/companionsotes/?data=' + str(a))



def qa(request):  # 问答problem，answer
    if request.method == "GET":
        list1 = functionsql(qa1)
        list2 = functionsql(qa2)
        for i in list1:
            i['city_name'] = \
                functionsql('select city_name from t_city where city_id=%s' % str(i['problem_place_id']))[0][
                    'city_name']
        return render(request, "qa.html", {'list': list1, 'list2': list2})
    else:
        problem = request.POST.get('data')
        key = 0
        try:
            type = request.POST.get('type')
            if (int(type) == 2):
                key = 1
        except:
            pass
        list1 = []
        set1 = set()
        html = ''
        if (problem):
            fenci = jieba.cut(problem)
            for i in fenci:
                i.strip()
                if (i):
                    if (key == 0):
                        list2 = functionsql(qa3(i))
                    else:
                        list2 = functionsql(qa4(i))
                    list1 = list1 + list2
        else:
            if (key == 0):
                list1 = functionsql(qa3(''))
            else:
                list1 = functionsql(qa4(''))
        for j in list1:
            if (j['problem_id'] in set1):
                continue
            else:
                city_name = \
                    functionsql('select city_name from t_city where city_id=%s' % str(j['problem_place_id']))[0][
                        'city_name']
                set1.add(j['problem_id'])
                str1 = '''<table id="ta1" style="width: 100%;margin-bottom: 10px">
                        <tr>
                            <td><a href="/qadetails/?data=''' + str(j["problem_id"]) + '''"><h4>''' + j[
                    'problem_title'] + '''</h4></a>
                            </td>
                            <td></td>
                        </tr>
                        <tr>
                            <td colspan="2">
                                <div style="width: 50px;height: 220px">
                                    <div style="width: 100%;border-radius:100%;overflow:hidden;"><img
                                            src="''' + j['user_img'] + '''" alt="" width="50px" height="50px">
                                    </div>
                                </div>
                                <div style="width: 80%;height: 220px">
                                    <h5 style="margin-bottom: 20px">''' + j['user_name'] + '''</h5>
                                    <div>
                                        <p>''' + j['md1'] + '''</p>
                                    </div>
                                    <div style="clear: both;width: 100%;margin-top: 0">
                                        <div style="float: right" id="divbiao">
                                            <li>''' + j['time1'] + '''</li>
                                            <li><a href="/region/?data=''' + str(
                    j['problem_place_id']) + '''">''' + city_name + '''</a>
                                            </li>
                                        </div>
                                    </div>
                                </div>
                            </td>
                        </tr>
                        <tr>
                            <td colspan="2">
                                <hr>
                            </td>
                        </tr>
                    </table>'''
                html = html + str1
        return HttpResponse(html)


def travels(request):  # 游记
    if request.method == "GET":
        list = functionsql(travels1)
        for i in list:
            i['md'] = mark_safe(markdown.markdown(i['md1']))
            i['count']=functionsql('select count(travels_collection_id) as count1 from t_travels_collection where travels_collection_travels_id='+str(i['travels_id']))[0]['count1']
        return render(request, "travels.html", {'list': list})
    else:
        cityname = request.POST.get("data")
        cityid = functionsql('select city_id from t_city where city_name="%s"' % cityname)[0]['city_id']
        list = functionsql(travels2(cityid))
        html = ''
        for i in list:
            str1 = '''<div>
            <a href="/travelnotes/?data=''' + str(i['travels_id']) + '''">
                    <table style="margin: 0">
                        <tr>
                            <td colspan="2"><h4>''' + i['travels_title'] + '''</h4></td>
                        </tr>
                        <tr style="height: 150px;margin: 0">
                            <td rowspan="2" style="width: 220px">
                                <img src="''' + i['travels_img_url'] + '''" width="100%" alt="">
                            </td>
                            <td style="padding:20px">''' + i['md1'] + '''
                                　
                            </td>
                        </tr>
                        <tr style="height: 50px">
                            <td>
                                <li>收藏('''+str(i['travels_collection'])+''')</li>
                                <li>''' + i['time1'] + '''</li>
                                <li><span style="color: #ff6600">''' + i['user_name'] + '''</span></li>
                                <li><img src="''' + i['user_img'] + '''" alt="" class="round_icon"></li>
                            </td>
                        </tr>
                    </table>
                </div>
                <hr>'''
            html = html + str1
        return HttpResponse(html)


def travelnotes(request):  # 游记详情
    a = request.GET.get("data")
    list = functionsql(travelnotes1(a))[0]
    list1 = functioncity(list['travels_region_type'], list['travels_region_id'])
    list['travels_md'] = mark_safe(markdown.markdown(list['travels_md']))
    state=0
    try:
        user_id=request.session['user_id']
        statelist=functionsql('select travels_collection_id from t_travels_collection where travels_collection_travels_id=%s and travels_collection_user_id=%s'%(str(a),str(user_id)))[0]
        if(statelist):
            state=1
    except:
        pass
    return render(request, "travelsdetails.html", {'list': list, 'list1': list1,'state':state})



def list(request):  # 旅游榜单
    list = functionsql('select * from t_list_details')
    return render(request, "listdetails.html", {'list': list})


def listmain(request):  # 榜单详情
    a = request.GET.get("data")
    list = functionsql(listmain1(a))
    title = functionsql(listmain2(a))[0]
    return render(request, "detailsofthelist.html", {'list': list, 'title': title})


def region(request):  # 地区详情
    if request.method == "GET":
        a = request.GET.get('data')
        list = functionsql(region1(a))[0]
        list['count_img'] = \
            functionsql('select count(img_id) as imgcoun from t_img where img_city_id=%s' % str(list['city_id']))[0][
                'imgcoun']
        list['city_describe'] = mark_safe(markdown.markdown(list['city_describe']))
        return render(request, "placedetails.html", {'list': list})
    else:
        a = request.POST.get('data').strip()
        city = request.POST.get('city')
        name = functionsql('select city_name from t_city where city_id=%d' % int(city))[0]
        if (a == '概述'):
            list1 = functionsql(region1(city))[0]
            list = markdown.markdown(list1['city_describe'])
            list = '<div class="col-md-9 column" id="div222">' + list + '</div>'
        elif (a == '热门景点'):
            list1 = functionsql(region2(city))
            list = '<div class="col-md-12 column" id="div222"><h3>必游景点TOP5</h3><div style=";width: 100%"><hr>'
            key = 0
            for i in list1:
                key = key + 1
                str1 = '''<table id="tab1"><tr><td></td><td rowspan="4"><a href="/scenicspot/?data=''' + str(
                    i["scenicspot_id"]) + '''"><img src="''' + i['scenicspot_img_url'] + '''" alt=""></a></td></tr><tr><td>
                            <h4>''' + str(key) + ' ' + i["scenicspot_name"] + '''</h4><br>''' + i[
                           'md'] + '''</td></tr><tr><td></td></tr></table><hr>'''
                list = list + str1
            list = list + '</div></div>'
        elif (a == "热门游记"):
            list1 = functionsql(region3(city))
            list = '<div class="col-md-12 column" id="div222">'
            for i in list1:
                str1 = '''<a href="/travelnotes/?data=''' + str(
                    i[
                        'travels_id']) + '''"><table id="tab1"><tr><td colspan="3"><h4 class="h23" style="color: #ee6600">''' + \
                       i[
                           "travels_title"] + '''</h4></td></tr><tr><td rowspan="2"><img src="''' + i[
                           "travels_img_url"] + '''"alt=""></td><td colspan="2">“''' + i[
                           "md"] + '''</td></tr><tr><td></td><td><div style="width: 40px; height: 40px; float:left; border-radius: 50%; border: 3px solid #eee; overflow: hidden;"><img src="''' + \
                       i[
                           "user_img"] + '''" alt="" class="round" style="width: 40px; height: 40px;"></div><span style="color: #ff9900;line-height: 40px">''' + \
                       i["user_name"] + '''</span>&nbsp;&nbsp;&nbsp;''' + i["time1"] + '''</td></tr></table></a><hr>'''
                list = list + str1
            list = list + '</div>'
        elif (a == "问答"):
            list1 = functionsql(region4(city))
            list = '<div class="col-md-12 column" id="div222">'
            for i in list1:
                str1 = '''<table class="tab3"><tr><td><div style="width: 60px; height: 60px; float:left; border-radius: 50%; border: 3px solid #eee; overflow: hidden;">
                        <img src="''' + i["user_img"] + '''" alt=""  style="width:60px ;height:60px" >
                    </div>
                    </td>
                    <td width="70px" style="color: #ee6600;font-size:20px">
                        ''' + i["user_name"] + '''
                    </td>
                    <td><h4 style="width:700px;"><a style="color: #ee6600" href="/qadetails/?data='''+str(i["problem_id"])+'''">''' + i["problem_title"] + '''</a></h4></td>
                </tr>
                <tr>
                    <td></td>
                    <td style="width: 200px"><img src="https://b2-q.mafengwo.net/s11/M00/5B/AB/wKgBEFrkKX-AQUzIABrFbg1QffY893.png?imageMogr2%2Fthumbnail%2F%21140x105r%2Fgravity%2FCenter%2Fcrop%2F%21140x105%2Fquality%2F90" alt=""></td>
                    <td>''' + i["md1"] + '''</td>
                </tr>

                <tr>
                    <td></td>
                    <td></td>
                    <td>
                        <ul>
                            <li>''' + i["time1"] + '''</li>
                            <li>赞(''' + str(i["answer_fabulous"]) + ''')</li>
                            <li><img src="../static/img/Icon/dingwei.png" alt="" style="width:16px" >''' + name[
                    'city_name'] + '''</li>
                        </ul>
                    </td>
                </tr>
            </table>
            <hr>'''
                list = list + str1
            list = list + '</div>'
        return HttpResponse(list)


def scenicspot(request):  # 景点详情
    if request.method=="GET":
        a = str(request.GET.get("data"))
        list = functionsql(scenicspot1(a))[0]
        collectionstate='0'
        try:
            user_id = request.session['user_id']
            functionsql1('insert into t_behavior(user_id,item_id,active_type,active_date) value(%s,%s,1,now())' % (
                str(user_id), str(a)))
            state=functionsql('select scenicspot_collection_id from t_scenicspot_collection where scenicspot_collection_user_id=%s and scenicspot_collection_scenicspot_id=%s'%(str(user_id),str(a)))[0]
            if(state):
                collectionstate='1'
            loginstate = 1
        except:
            user_id=-1
            loginstate = 0



        list["scenicspot_md"] = mark_safe(markdown.markdown(list['scenicspot_md']))
        list1 = functionsql(scenicspot2(a))
        city_name = functionsql('select city_name from t_city where city_id=' + str(list['scenicspot_city_id']))[0][
            'city_name']
        list['count_img'] = \
            functionsql(
                'select count(img_id) as imgcoun from t_img where img_scenicspot_id=%s' % str(list['scenicspot_id']))[0][
                'imgcoun']
        weather1 = weather(city_name)

        # 评论
        commentlist = functionsql(comment1(3,a))
        html2 = ""
        for c in commentlist:
            # 该评论被我赞过的次数(0或1)
            if(loginstate==1):
                UserCommentFabulous = functionsql("select count(*) from t_fabulous where comment_fabulous_user_id=%d and comment_fabulous_comment_id=%d"%(int(user_id), int(c["comment_id"])))[0]["count(*)"]
            else:
                UserCommentFabulous=0

            if int(UserCommentFabulous) == 0:
                ZanImgSrc = "../static/img/fabulous/meizan2.png"
            else:
                ZanImgSrc = "../static/img/fabulous/yizan2.png"

            # 该评论是不是我写的

            # 是我写的
            if int(c["comment_user_id"]) == int(user_id):
                shan = '<a href="javascript:;" onclick="DeleteComment(this)" data-scenicspotid="' + str(
                    a) + '" data-commentid="' + str(
                    c["comment_id"]) + '" class="date-dz-pl pl-hf hf-con-block pull-left"> 删除 </a>'
                huifu = '<a href="javascript:;" data-commentid="''" class="date-dz-pl pl-hf hf-con-block pull-left"></a>'
            # 不是我写的
            else:
                shan = ''
                # huifu=''
                huifu = '<a href="javascript:;" class="date-dz-pl pl-hf hf-con-block pull-left"></a>'
            html2 += '<div id="' + str(c["comment_id"]) + '" class ="comment-show-con clearfix">' \
                                                          '<div class="comment-show-con-img pull-left">' \
                                                          '<img style="width:100%;border-radius: 50%" src="' + str(
                c["user_img"]) + '" alt="">' \
                                 '</div>' \
                                 '<div class="comment-show-con-list pull-left clearfix">' \
                                 '<div class="pl-text clearfix" style=";margin-top: 20px">' \
                                 '<a href="#" class="comment-size-name"> ' + str(c["user_name"]) + ': </a>' \
                                                                                                   '<span class="my-pl-con" > ' + str(
                c["comment_text"]) + ' </span>' \
                                     '</div>' \
                                     '<div style="display:fiex;text-align:right;">' \
                                     '<div style="margin-top:5px"> ' \
                     + str(c["comment_time"]) + \
                     '</div>' \
                     '<div style="display:flex;float:right">' \
                     '<div style="margin-top:5px;margin-right:10px">' + shan + '</div>' \
                                                                               '<div style="margin-top:5px">' + huifu + '</div>' \
                                                                                                                        '<div style="margin-top:5px"><span class="pull-left date-dz-line"> | </span></div>' \
                                                                                                                        '<div class="praise">' \
                                                                                                                        '<div style="width: auto;height: 25px;padding: 0"> <span id="praise" class="praise-span1" style="margin:0">' \
                                                                                                                        '<img style="height:25px;width:25px" onclick="zancomment(this)" src="' + ZanImgSrc + '" id="praise-img" data-commentid="' + str(
                c["comment_id"]) + '"/> </span>' \
                                   '</div>' \
                                   '<div style="text-align:center">' \
                                   '<span id="praise-number-' + str(
                c["comment_id"]) + '" class="praise-span2" style="font-size:1px">' \
                     + str(c["comment_fabulous"]) + \
                     '</span>' \
                     '</div>' \
                     '</div>' \
                     '</div>' \
                     '</div>' \
                     '<div class="hf-list-con"></div>' \
                     '</div>' \
                     '</div>'
        # html2="<button>按钮</button>"
        html = mark_safe(html2)

        return render(request, "scenicspotdetails.html", {'list': list, 'list1': list1, 'weather': weather1,'collectionstate':collectionstate,"html":html,"a":a})
    else:
        type1=request.POST.get("type")
        if type1=="dianzan":
            jiajian = request.POST.get("jiajian")
            commentid = request.POST.get("commentid")
            try:
                userid = request.session['user_id']
            except:
                return render(request,'register.html')
            if int(jiajian) == 1:
                functionsql1(
                    "update t_comment set comment_fabulous=comment_fabulous+1 where comment_id=%d" % int(commentid))
                functionsql1(
                    "insert into t_fabulous(comment_fabulous_user_id,comment_fabulous_comment_id) values(%d,%d)" % (
                    int(userid), int(commentid)))
            else:
                functionsql1(
                    "update t_comment set comment_fabulous=comment_fabulous-1 where comment_id=%d" % int(commentid))
                functionsql1(
                    "delete from t_fabulous where comment_fabulous_user_id=%d and comment_fabulous_comment_id=%d" % (
                    int(userid), int(commentid)))
            # 赞回答
            return HttpResponse(1)
        if type1 == "writecomment":
            # 用户id
            try:
                userid = request.session['user_id']
            except:
                return render(request,'register.html')
            # 评论内容
            newcommentTEXT = request.POST.get("newcomment")
            # 评论对象id
            a = request.POST.get("a")

            # 数据库插入评论
            cursor, conn = open1()  # 获取游标
            functionsql1(writecomment1(userid,newcommentTEXT,a,3))#  3是评论类型
            # cursor.execute("insert into t_comment(comment_text, comment_user_id, comment_time, comment_fabulous, comment_object_id, comment_type)" \
            # "values('%s', % d, now(), 0, % d, 2)"%(newcomment,int(userid),int(answerid)))
            # conn.commit()

            # commentid=functionsql("select last_insert_id()")[0]["last_insert_id()"]

            # 获取刚插入的评论的id
            try:
                with conn.cursor() as cursor:  # 增加
                    sql = "insert into t_comment(comment_text, comment_user_id, comment_time, comment_fabulous, comment_object_id, comment_type) " \
                            "values('%s', % d, now(), 0, % d, 2)" % (newcommentTEXT, int(userid), int(a))
                    cursor.execute(sql)
                    conn.commit()
                    sql = 'SELECT LAST_INSERT_ID() AS id;'
                    cursor.execute(sql)
                    commentid = cursor.fetchone()[0]
            finally:
                conn.close()


            newcomment = functionsql("select c.* from t_comment as c where c.comment_id=%d" % int(commentid))[0]

            userinfo = functionsql(user(userid))[0]

            html2 = '<div class ="comment-show-con clearfix" id="'+str(commentid)+'">' \
                     '<div class="comment-show-con-img pull-left">' \
                     '<img style="width:100%;border-radius: 50%" src="' + str(userinfo["user_img"]) + '" alt="">' \
                                                                                                      '</div>' \
                                                                                                      '<div class="comment-show-con-list pull-left clearfix">' \
                                                                                                      '<div class="pl-text clearfix" style=";margin-top: 20px">' \
                                                                                                      '<a href="#" class="comment-size-name"> ' + str(userinfo["user_name"]) + ': </a>' \
                                         '<span class="my-pl-con" > ' + str(newcommentTEXT) + ' </span>' \
                                                                                              '</div>' \
                                                                                              '<div style="display:fiex;text-align:right;">' \
                                                                                              '<div style="margin-top:5px"> ' \
                     + str(newcomment["comment_time"]) + \
                     '</div>' \
                     '<div style="display:flex;float:right">' \
                     '<div style="margin-top:5px;margin-right:10px">' + \
                     '<a href="javascript:;" onclick="DeleteComment(this)" data-answerid="' + str(
                a) + '" data-commentid="' + str(commentid) + '" class="date-dz-pl pl-hf hf-con-block pull-left"> 删除 </a>' + \
                     '</div>' \
                     '<div style="margin-top:5px">' + '<a href="javascript:;" class="date-dz-pl pl-hf hf-con-block pull-left"></a>'+ '</div>' \
                                                          '<div style="margin-top:5px"><span class="pull-left date-dz-line"> | </span></div>' \
                                                          '<div class="praise">' \
                                                          '<div style="width: auto;height: 25px;padding: 0"> <span id="praise" class="praise-span1" style="margin:0">' \
                                                          '<img style="height:25px;width:25px" onclick="zancomment(this)" src="' + "../static/img/fabulous/meizan2.png" + '" id="praise-img" data-commentid="' +str(commentid) + '"/> </span>' \
                                 '</div>' \
                                 '<div style="text-align:center">' \
                                 '<span id="praise-number-' + str((commentid)) + '" class="praise-span2" style="font-size:1px">' \
                + "0" + \
                '</span>' \
                '</div>' \
                '</div>' \
                '</div>' \
                '</div>' \
                '<div class="hf-list-con"></div>' \
                '</div>' \
                '</div>'
            html = mark_safe(html2)
            return HttpResponse(html)
        if type1 == "DeleteComment":
            commentid=request.POST.get("commentid")
            try:
                functionsql1("delete from t_comment where comment_id=%d"%int(commentid))
            except:
                pass

def page_not_found(request):
    return render(request, '404.html')


def recommend(request):  # 推荐
    try:
        user_id = request.session['user_id']
    except:
        return render(request, 'register.html')
    user_score1 = functionsql('select * from t_user_label where user_id=%s' % user_id)[0]
    city_score1 = functionsql("select * from t_scenicspot_label")
    list = []
    for i in city_score1:
        user_score = np.array([user_score1['food'], user_score1['mountain'], user_score1['sea'], user_score1['modern'],
                               user_score1['history'], user_score1['explore'], user_score1['price'],
                               user_score1['number']], dtype=float16)
        scenicspot_score = np.array(
            [i['food'], i['mountain'], i['sea'], i['modern'], i['history'], i['explore'], i['price'], i['number']])
        cos = np.dot(user_score, scenicspot_score) / (
                math.sqrt(np.dot(user_score, user_score)) * math.sqrt(np.dot(scenicspot_score, scenicspot_score)))
        list.append([i['scenicspot_id'], cos])

    visited = functionsql('select item_id from t_behavior where user_id=%s and active_type=3'%str(user_id))
    for i in visited:
        for j in list:
            if(int(j[0])==int(i['item_id'])):
                list.remove(j)

    list.sort(key=lambda x: x[1], reverse=True)
    ss = []
    k1 = 0
    for k in list:
        k1 += 1
        ss1 = functionsql('select * from t_scenicspot where scenicspot_id=%s' % int(k[0]))[0]
        pattern1 = re.compile(r"景点概述\*\*(.*?)----", re.S)
        rese = re.search(pattern1, ss1['scenicspot_md']).group(0)[6:-5]
        ss1['title'] = rese
        ss1['placeofname'] = k1
        ss.append(ss1)
        if (len(ss) > 5):
            break
    return render(request, 'recommend.html', {'list': ss})
