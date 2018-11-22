from django.shortcuts import render, redirect, HttpResponse
from django.utils.safestring import mark_safe
import pymysql.cursors
from random import randint
from jinn.connect import *
from jinn.sql import *
from jinn.function import *
from algorithm.bayes import *
import imghdr

cursor, conn = open1()



def passimg(request):  # 七牛云传图片
    img = request.FILES.get('imageData')
    key = functionsql('select sign_num from t_sign where sign_name="img"')[0]
    functionsql1('update t_sign set sign_num=sign_num+1 where sign_name="img"')
    suffix = imghdr.what(img)
    username=request.session['user_name']
    img_url = qiniuyun('img' + str(key['sign_num']) + '.' + suffix, img, suffix,username)
    return HttpResponse(img_url)


def wtn(request):  # 写游记,Write a travel note
    if request.method == "GET":
        try:
            request.session['user_id']
            return render(request, 'writetravel.html')
        except:
            return render(request, 'register.html')
    else:
        html = request.POST.get("html")
        img = request.FILES.get("img")
        title = request.POST.get("title")
        place = request.POST.get('place')
        userid = request.session['user_id']
        consumption = request.POST.get("consumption")
        date = request.POST.get("date")
        key = functionsql('select sign_num from t_sign where sign_name="travels"')[0]
        functionsql1('update t_sign set sign_num=sign_num+1 where sign_name="travels"')
        suffix = imghdr.what(img)
        img_url = qiniuyun('travels' + str(key['sign_num']) + '.' + suffix, img, suffix)
        functionsql1(wtn1(html, img_url, title, place, userid, consumption, date))
        last = functionsql("select max(travels_id) as travels_id from t_travels")[0]['travels_id']
        return redirect('/travels/?data=' + str(last))

def companioncollection(request):#结伴收藏
    try:
        user_id=request.session['user_id']
    except:
        return render(request, 'register.html')
    type1=request.POST.get('type')
    com=request.POST.get('companion')
    if(int(type1)==1):
        functionsql1('insert into t_companions_collection(companions_collection_user_id,companions_collection_companions_id) value(%s,%s)'%(str(user_id),str(com)))
    else:
        functionsql1('delete from t_companions_collection where companions_collection_user_id=%s and companions_collection_companions_id=%s'%(str(user_id),str(com)))
    return HttpResponse(1)


def scenicspotcollection(request):#景点收藏
    try:
        user_id=request.session['user_id']
    except:
        return render(request, 'register.html')

    type1=request.POST.get('type')
    com=request.POST.get('companion')
    print (com)
    if(int(type1)==1):
        functionsql1('insert into t_behavior(user_id,item_id,active_type,active_date) value(%s,%s,3,now())'%(str(user_id),str(com)))
        functionsql1('insert into t_scenicspot_collection(scenicspot_collection_user_id,scenicspot_collection_scenicspot_id) value(%s,%s)'%(str(user_id),str(com)))
    else:
        functionsql1('delete from t_scenicspot_collection where scenicspot_collection_user_id=%s and scenicspot_collection_scenicspot_id=%s'%(str(user_id),str(com)))
    return HttpResponse(1)


def travelscollection(request):#游记收藏
    try:
        user_id=request.session['user_id']
    except:
        return render(request, 'register.html')
    type1=request.POST.get('type')
    com=request.POST.get('companion')
    print (com,type1)
    if(int(type1)==1):
        print (str(user_id),str(com))
        functionsql1('insert into t_travels_collection(travels_collection_user_id,travels_collection_travels_id) value(%s,%s)'%(str(user_id),str(com)))
    else:
        functionsql1('delete from t_travels_collection where travels_collection_user_id=%s and travels_collection_travels_id=%s'%(str(user_id),str(com)))
    return HttpResponse(1)




def releasecompanions(request):  # 发布结伴
    if request.method == "GET":
        try:
            request.session['user_id']
            return render(request, 'releasecompanions.html')
        except:
            return render(request, 'register.html')
    else:
        html = request.POST.get("html")
        img = request.FILES.get("img")
        title = request.POST.get("title")
        place = request.POST.get('place')
        userid = request.session['user_id']
        date = request.POST.get("date")
        expect = request.POST.get("expect")
        time = request.POST.get("time")
        phone = request.POST.get("phone")
        key = functionsql('select sign_num from t_sign where sign_name="companions"')[0]
        functionsql1('update t_sign set sign_num=sign_num+1 where sign_name="companions"')
        suffix = imghdr.what(img)
        img_url = qiniuyun('companions' + str(key['sign_num']) + '.' + suffix, img, suffix)
        functionsql1(releasecompanions1(html, img_url, title, place, userid, date, expect, time, phone))
        last = functionsql("select max(companions_id) as companions_id from t_companions")[0]['companions_id']
        return redirect('/releasecompanions/?data=' + str(last))


def issues(request):  # 发布问题
    if request.method == "GET":
        try:
            a = request.session['user_id']
            return render(request, "putquestionsto.html")
        except:
            return render(request, 'register.html')
    else:
        userid = request.session['user_id']
        title = request.POST.get('title')
        text = request.POST.get('text')
        place = request.POST.get("place")
        label = request.POST.get("Storage")
        functionsql1(issues1(title, text, place, userid, label))
        return redirect('/qa/')



def comment(request):  # 评论
    pass


def gtt(request):  # 点赞Give the thumbs-up
    pass


def signin(request):  # 登录
    if (request.method == "GET"):
        return render(request, "register.html")
    else:
        phone = request.POST.get('phone')
        password = request.POST.get('pass')
        state = 0
        list = functionsql("select user_id,user_password,user_name from t_user where user_phone='%s'" % str(phone))
        if (list):
            list = list[0]
            if (str(password) == str(list['user_password'])):
                state = 1
                request.session['is_login'] = True
                request.session["user_id"] = list['user_id']
                request.session["user_name"] = list["user_name"]
            else:
                state = 2
        return HttpResponse(state)


def logout(request):  # 登出
    if not request.session.get('is_login', None):
        return redirect("/homepage/")
        # 如果本来就未登录，也就没有登出一说
    request.session.flush()
    return redirect("/homepage/")


def personalcenter(request):  # personalcenter
    pass


def register(request):  # 注册、更改密码
    if request.method == "GET":
        return render(request, 'register.html')
    else:
        type = request.POST.get('type')
        if (int(type) == 2):
            phone = request.POST.get('zcphone')
            password = request.POST.get('zcpass')
            name = request.POST.get('zcname')
            functionsql1('INSERT INTO `t_user`(user_phone,user_name,user_password) VALUES ("%s","%s","%s")' % (
            phone, name, password))
        else:
            phone = request.POST.get('czphone')
            password = request.POST.get('czpass')
            functionsql1('UPDATE t_user SET user_password ="' + str(password) + '"where user_phone=' + str(phone))
    return redirect("/homepage/")



def verver(request):  # 验证码验证
    phone = request.POST.get('phone')
    type = request.POST.get('type')
    verification = request.POST.get('ver')
    state = '0'  # 验证码错误
    ver = \
        functionsql(
            'select ver_verification,ver_expiry,now() as now from t_verification where ver_phone="%s"' % phone)[
            0]
    if (int(ver['ver_verification']) == int(verification)):
        if (ver['ver_expiry'] > ver["now"]):
            state = '1'  # 验证码正确
        else:
            state = '2'  # 验证码过期
    return HttpResponse(state)


def verificationcode(request):  # 验证码
    phone = request.POST.get('phone')
    type = request.POST.get('type')
    ver = randint(100000, 999999)
    if (type == '1'):
        result = functionsql1(verificationcode1(phone, ver))
        obtainverificationcode(phone, ver)
    elif (type == '2'):
        id = functionsql('select user_id from t_user where user_phone="%s"' % phone)
        if (id):
            id = id[0]
            result = functionsql1(verificationcode1(phone, ver))
            obtainverificationcode(phone, ver)
        else:
            result = 2
    return HttpResponse(result)
