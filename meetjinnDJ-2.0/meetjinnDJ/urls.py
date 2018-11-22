"""meetjinnDJ URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from jinn import views, view1, view3, views2

urlpatterns = [
    # --------------------读----首页类------------
    path('admin/', admin.site.urls),
    path('search/', views.search),  # 目的地
    path('homepage/', views.homepage),  # 首页
    path('qa/', views.qa),  # 问答
    path('companions/', views.companions),  # 结伴
    path('companionsotes/', views.companionsotes),  # 结伴详情
    path('travels/', views.travels),  # 游记
    path('travelnotes/', views.travelnotes),  # 游记详情
    path('list/', views.list),  # 榜单
    path('listmain/', views.listmain),  # 榜单详情
    path('region/', views.region),  # 地区详情
    path('scenicspot/', views.scenicspot),  # 景点详情

    # ---------------------写--------------------
    path('wtn/', view1.wtn),  # 写游记
    path('releasecompanions/', view1.releasecompanions),  # 发布结伴
    path('issues/', view1.issues),  # 发布问题
    path('qadetails/', view3.qadetails),  # 回答问题
    path('comment/', view1.comment),  # 评论
    path('gtt/', view1.gtt),  # fabulous
    path('signin/', view1.signin),  # 登录
    path('personalcenter/', view1.personalcenter),  # personalcenter
    path('register/', view1.register),  # 注册
    path('verification/', view1.verificationcode),  # 验证码
    path('logout/', view1.logout),  # 注销
    path('verver/', view1.verver),  # 验证码验证
    path('passimg/', view1.passimg),  # 传图片
    path('recommend/', views.recommend),  # 推荐
    path("soutu/", view3.soutu),  # 搜索图片
    path("yuyinshibie/", views.yuyinjianyan),  # 搜索图片
    path("companioncollection/", view1.companioncollection),  # 结伴收藏
    path("scenicspotcollection/", view1.scenicspotcollection),  # 景点收藏
    path("travelscollection/", view1.travelscollection),  # 游记收藏
    path("questionanswering/", view3.questionanswering),  # 游记收藏

    # ----------------------siri板块--------------------
    path("siri/", views.siri),  # siri
    path("huanxin/", views.huanxin),  # siri

    # ---------------------个人中心板块---------------------
    path('myimg/', views2.myimg),  # 我的图片
    path('house/', views2.house),  # 我的收藏
    path('index/', views2.index),  # 个人中心首页
    path('install/', views2.install),  # 设置
    path('interlocution/', views2.interlocution),  # 问答
    path('mate/', views2.mate),  # 结伴
    path('plans/', views2.plans),  # 我的游记
    path('biography/', views2.biography),  # 传图片
]

handler404 = views.page_not_found
handler500 = views.page_not_found
