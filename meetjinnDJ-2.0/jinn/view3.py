from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.utils.safestring import mark_safe
import pymysql.cursors
from random import randint
from jinn.connect import *
from jinn.sql import *
from jinn.function import *
from algorithm.bayes import *
import imghdr

cursor, conn = open1()

def qadetails(request):#回答
    if request.method == "GET":
        i = 0
        j =9999999999
        # 用户id
        try:
            userid = request.session['user_id']
            loginstate = 1
        except:
            userid=-1
            loginstate=0
        problem_id = request.GET.get('data')  # 获取问题id=2
        problem0 = functionsql(problem(problem_id))[0]  # 获取问题具体内容
        answer_list = functionsql(answer(problem_id, i, j))  # 获取所有回答
        city=functionsql('select * from t_city where city_id='+str(problem0['problem_place_id']))[0]

        for answers in answer_list:
            #回答的评论数
            answers["comment_number"]=functionsql("select count(*) as count from t_comment where comment_type=2 and comment_object_id=%d"%int(answers["answer_id"]))[0]["count"]
            #赞回答的按钮id
            answers["zan_id"]="zan-"+str(answers["answer_id"])
            # 获取该回答总赞数
            answers["answerFabulous"] = functionsql(answerfabulous(answers["answer_id"]))[0]

            # 此用户赞了该回答的次数（0或1）
            if(loginstate==1):
                answers["userfabulous"] = functionsql(userfabulous(userid, answers["answer_id"]))[0]["count(*)"]
            else:
                answers["userfabulous"]=0


            if answers["userfabulous"]==0:
                answers["zancolor"]="black"
            else:
                answers["zancolor"]="red"

            # 获取赞行为id
            fabulousID = functionsql(fabulousid(userid, answers["answer_id"]))

            if len(fabulousID) == 0:
                answers["fabulousid"] = -1
            else:
                answers["fabulousid"] = fabulousID[0]

            answers["writeCommentID"] = "writeCommentID" + str(answers["answer_id"])
            answers['divIDdiva'] = "divdiva" + str(answers["answer_id"])
            answers['divPARENTa'] = "#divdiva" + str(answers["answer_id"])
            answers["commentareaID"] = "commentareaID" + str(answers["answer_id"])
            answers["aHREF"] = "#commentareaID" + str(answers["answer_id"])
            answers["commentlist_id"] = "commentlist" + str(answers["answer_id"])
            answers['answer_md'] = mark_safe(markdown.markdown(answers['answer_md']))
        answer_number = len(answer_list)  # 回答人数
        return render(request, "qadetails.html",
                      {"answer_list": answer_list, "problem0": problem0, "answer_number": answer_number,'city':city})
    else:
        # 用户id
        try:
            userid = request.session['user_id']
            loginstate = 1
        except:
            userid=-1
            loginstate=0
        type = request.POST.get("type")
        if type == "loading":
            clicktime = int(request.POST.get('clicktime')) - 1
            clicktime_j = clicktime + 1
            problem_id = request.POST.get('problemid')
            answer_list = functionsql(answer(problem_id, clicktime, clicktime_j))  # 获取所有回答
            html = ""
            for a in answer_list:
                a['answer_md'] = mark_safe(markdown.markdown(a['answer_md']))
                html += '<div style="margin: 20px auto;box-shadow: 0 0 0.4px 2px rgba(58,58,58,0.13);background-color: white">' \
                        '<div style="margin: 10px;width: auto">' \
                        '<div class="answer"  ><div><div>' \
                        '<img src="' + str(a['user_img']) + '" style="width: 30px;height: 30px;border-radius: 50%">' \
                                                            '</div><div>' + str(a['user_name']) + '</div></div><div>' \
                                                                                                  '<span>' + str(
                    a['answer_fabulous']) + '人赞了TA</span></div>' \
                                            '<div style="text-align:left">' + str(
                    a['answer_md']) + '</div></div>'+ \
                        '<div style="width: 100%;height: 100px;border: 1px black solid">' \
                        ' <div> 赞 </div>' \
                        '<div class="panel-group" id="'+"divdiva" + str(a["answer_id"])+'" >' \
                            '<div class="panel-heading" >' \
                                '<a class="panel-title collapsed" data-toggle="collapse" data-parent="'+"#divdiva" + str(a["answer_id"])+'" href="'+"#commentareaID" + str(a["answer_id"])+'" data-answerid="'+str(a["answer_id"])+'" onclick="loadcomment(this)">评论(点击弹出) </a>' \
                        '</div>' \
                        '</div>' \
                        '</div>' \
                        '<div id="'+"commentareaID" + str(a["answer_id"])+'" class ="panel-collapse collapse">' \
                        '<div class="panel-body comment-block" >< !--下方弹出来内容 -->' \
                        '<div class="comment-areaarea">< !--评论区域 begin -->' \
                        '<div class="reviewArea clearfix">' \
                        '< textarea id = "'+"writeCommentID" + str(a["answer_id"])+'" class ="content comment-input" placeholder = "评论一下&hellip;" onkeyup = "keyUP(this)">' \
                        '</textarea>' \
                        '<a href="javascript:;" class ="plBtn" onclick="sentcomment(this)" data-answerid = "'+ str(a["answer_id"])+'">评论</a>' \
                        '</div>' \
                        '<div class="comment-listlist">' \
                        '<div class="comment-show" id="'+"commentlist" + str(a["answer_id"])+'">' \
                        '</div>' \
                        '</div>' \
                        '</div>' \
                        '</div>' \
                        '</div>' \
                        '</div>' \
                        '</div>'
            html = mark_safe(html)
            return HttpResponse(html)
        #加载评论
        if type == "comment":
            answerid = int(request.POST.get("answerid"))
            commentlist = functionsql(comment1(2, answerid))
            html2 = ""
            for c in commentlist:
                # 该评论被我赞过的次数(0或1)
                if(loginstate==1):
                    UserCommentFabulous = functionsql(
                        "select count(*) from t_fabulous where comment_fabulous_user_id=%d and comment_fabulous_comment_id=%d" % (
                        int(userid), int(c["comment_id"])))[0]["count(*)"]
                else:
                    UserCommentFabulous=0

                if int(UserCommentFabulous) == 0:
                    ZanImgSrc="../static/img/fabulous/meizan2.png"
                else:
                    ZanImgSrc = "../static/img/fabulous/yizan2.png"

                # 该评论是不是我写的

                #是我写的
                if int(c["comment_user_id"]) == int(userid and loginstate==1):
                    shan='<a href="javascript:;" onclick="DeleteComment(this)" data-answerid="'+str(answerid)+'" data-commentid="'+str(c["comment_id"])+'" class="date-dz-pl pl-hf hf-con-block pull-left"> 删除 </a>'

                #不是我写的
                else:
                    shan=''
                    #huifu=''
                html2 += '<div id="'+str(c["comment_id"])+'" class ="comment-show-con clearfix">' \
                            '<div class="comment-show-con-img pull-left">' \
                                '<img style="width:100%;border-radius: 50%" src="' + str(c["user_img"]) + '" alt="">' \
                            '</div>' \
                            '<div class="comment-show-con-list pull-left clearfix">' \
                                '<div class="pl-text clearfix" style=";margin-top: 20px">' \
                                    '<a href="#" class="comment-size-name"> ' + str(c["user_name"]) + ': </a>' \
                                    '<span class="my-pl-con" > ' + str(c["comment_text"]) + ' </span>' \
                                '</div>' \
                                '<div style="display:fiex;text-align:right;">' \
                                    '<div style="margin-top:5px"> ' \
                                        + str( c["comment_time"]) + \
                                    '</div>' \
                                    '<div style="display:flex;float:right">' \
                                        '<div style="margin-top:5px;margin-right:10px">'+shan+'</div><div style="margin-top:5px"><span class="pull-left date-dz-line"> | </span></div>' \
                                        '<div class="praise">' \
                                            '<div style="width: auto;height: 25px;padding: 0"> <span id="praise" class="praise-span1" style="margin:0">' \
                                                '<img style="height:25px;width:25px" onclick="zancomment(this)" src="'+ZanImgSrc+'" id="praise-img" data-commentid="'+str(c["comment_id"])+'"/> </span>' \
                                            '</div>' \
                                            '<div style="text-align:center">' \
                                                '<span id="praise-number-'+str(c["comment_id"])+'" class="praise-span2" style="font-size:1px">' \
                                                +str(c["comment_fabulous"])+ \
                                                '</span>' \
                                            '</div>' \
                                        '</div>' \
                                    '</div>' \
                                '</div>' \
                                '<div class="hf-list-con"></div>' \
                            '</div>' \
                         '</div>'
            # html2="<button>按钮</button>"
            html2 = mark_safe(html2)
            return HttpResponse(html2)
            # ajax 写评论
        if type == "writecomment":
            # 用户id
            userid = request.session['user_id']
            # 评论内容
            # newcomment=886
            newcommentTEXT = request.POST.get("newcomment")
            reselt=baidutext(newcommentTEXT)
            if(reselt!='1'):
                reselt='"'+reselt[0]+'"不合规,不合规原因：'+reselt[1]
                return JsonResponse({'reselt':'1','content':reselt})
                return HttpResponse(reselt)
            # 评论对象id
            answerid = request.POST.get("answerid")
            # 数据库插入评论
            cursor, conn = open1()  # 获取游标
            functionsql1(writecomment(userid,newcommentTEXT,answerid))
            # cursor.execute("insert into t_comment(comment_text, comment_user_id, comment_time, comment_fabulous, comment_object_id, comment_type)" \
            # "values('%s', % d, now(), 0, % d, 2)"%(newcomment,int(userid),int(answerid)))
            # conn.commit()

            # commentid=functionsql("select last_insert_id()")[0]["last_insert_id()"]

            # 获取刚插入的评论的id
            try:
                with conn.cursor() as cursor:  # 增加
                    sql = "insert into t_comment(comment_text, comment_user_id, comment_time, comment_fabulous, comment_object_id, comment_type) " \
                            "values('%s', % d, now(), 0, % d, 2)" % (newcommentTEXT, int(userid), int(answerid))
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
                answerid) + '" data-commentid="' + str(commentid) + '" class="date-dz-pl pl-hf hf-con-block pull-left"> 删除 </a>' + \
                     '</div>' \
                     '<div style="margin-top:5px">' + '<a href="javascript:;" class="date-dz-pl pl-hf hf-con-block pull-left"> 回复 </a>'+ '</div>' \
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
            html2 = mark_safe(html2)
            return JsonResponse({'reselt':'2','html':html2})
        if type == "dianzan":
            jiajian=request.POST.get("jiajian")
            commentid=request.POST.get("commentid")
            userid=1
            if int(jiajian)==1:
                functionsql1("update t_comment set comment_fabulous=comment_fabulous+1 where comment_id=%d"%int(commentid))
                functionsql1("insert into t_fabulous(comment_fabulous_user_id,comment_fabulous_comment_id) values(%d,%d)"%(int(userid),int(commentid)))
            else:
                functionsql1("update t_comment set comment_fabulous=comment_fabulous-1 where comment_id=%d" % int(commentid))
                functionsql1("delete from t_fabulous where comment_fabulous_user_id=%d and comment_fabulous_comment_id=%d"%(int(userid),int(commentid)))
        # 赞回答
        if type=="zananswer":
            userid = request.session['user_id']
            jiajian=int(request.POST.get("jiajian"))
            answerid=request.POST.get("answerid")
            if jiajian==1:
                functionsql1("update t_answer set answer_fabulous=answer_fabulous+1 where answer_id=%d"%int(answerid))
                functionsql1("insert into t_answer_fabulous(answer_fabulous_user_id,answer_fabulous_answer_id) values(%d,%d)"%(int(userid),int(answerid)))
            else:
                functionsql1("update t_answer set answer_fabulous=answer_fabulous-1 where answer_id=%d"%int(answerid))
                functionsql1("delete from t_answer_fabulous where answer_fabulous_user_id=%d and answer_fabulous_answer_id=%d"%(int(userid),int(answerid)))

        if type == "DeleteComment":
            commentid=request.POST.get("commentid")
            try:
                functionsql1("delete from t_comment where comment_id=%d"%int(commentid))
            except:
                pass
        if type=="XieHuifu":
            userid = request.session['user_id']
            #被回复的评论id
            commentid = request.POST.get("commentid")
            #被回复的人的id
            comment_user_id=functionsql("select comment_user_id from t_comment where comment_id=%d"%int(commentid))
            #评论所在的回答的id
            answerid=functionsql("select comment_object_id from t_comment where comment_id=%d and comment_type=%d"%(int(),int()))
            #回复框的id
            huifuid="huifu-"+str(commentid)
            huifu='<div class="reviewArea clearfix">' \
                       '<textarea id="'+huifuid+'" class="content comment-input"' \
                       'placeholder="评论一下&hellip;"></textarea>' \
                       '<a href="javascript:;" class="plBtn" onclick="FaHuifu"' \
                       'data-answerid="'+str(answerid)+'" data-commentid="'+str(commentid)+'" data=>评论</a>' \
                       '</div>'
            huifu=mark_safe(huifu)
            return HttpResponse(huifu)


def soutu(request):
    if request.method == "GET":
        try:
            city_id=int(request.GET.get("city_id"))
            imglist=functionsql("select i.*,u.user_id,u.user_name,u.user_img,u.user_sex from t_img as i,t_user as u where i.img_city_id=%d and i.img_user_id=u.user_id"%city_id)
        except:
            scenicspot_id=int(request.GET.get("scenicspot_id"))
            imglist=functionsql("select i.*,u.user_id,u.user_name,u.user_img,u.user_sex from t_img as i,t_user as u where i.img_scenicspot_id=%d and i.img_user_id=u.user_id"%scenicspot_id)
        userid = request.session['user_id']
        for img in imglist:
            img["collect_icon_id"]="icon-"+str(img["img_id"])
            #我收藏这个图片的次数
            #为0
            if functionsql("select count(*) from t_collectimg where img_id=%d and collect_user_id=%d"%(int(img["img_id"]),int(userid)))[0]["count(*)"]==0:
                img["collect_icon_src"]="../static/img/Icon/xin.png"
            else:
                img["collect_icon_src"] = "../static/img/Icon/xin2.png"

        return render(request,"picturewaterfall.html",{"imglist":imglist})
    else:
        imgid=request.POST.get("imgid")
        jiajian=int(request.POST.get("jiajian"))
        userid = request.session['user_id']
        if jiajian==1:
            functionsql1("insert into t_collectimg(img_id,collect_user_id) value (%d,%d)"%(int(imgid),int(userid)))
            functionsql1("update t_img set img_collection=img_collection+1 where img_id=%d"%int(imgid))
        else:
            functionsql1("delete from t_collectimg where img_id=%d and collect_user_id=%d" % (int(imgid), int(userid)))
            functionsql1("update t_img set img_collection=img_collection-1 where img_id=%d" % int(imgid))



def questionanswering(request):
    html=request.POST.get('html')
    user_id=request.session['user_id']
    problem_id=request.POST.get('id')
    import html2text as ht
    text_maker = ht.HTML2Text()
    text_maker.bypass_tables = False
    text = text_maker.handle(html)
    functionsql1('insert into t_answer(answer_user_id,answer_md,answer_time,answer_problem_id,answer_fabulous) value(%s,"%s",now(),%s,0)'%(str(user_id),str(text),str(problem_id)))
    return HttpResponse(1)