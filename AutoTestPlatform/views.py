#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2020/10/13 7:16 下午
# @Author : wyf
# @File : views.py
# @Software: PyCharm
import logging
logger = logging.getLogger("首页")
import datetime
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from project_env.models import Project
from apitest.models import  Interface,Case,Report
from taste_user.models import Taste,Role
from django.core.paginator import Paginator
from lib.commonmethod import get_time_by_nexttime,time_add
#首页的视图函数
@login_required
def index(request):
    #概览页翻页参数
    page_num=request.GET.get("page_num",1)
    #用户对象
    user_obj=request.user
    if user_obj.is_superuser:
        # 项目概览
        project_num = Project.objects.all().count()
        # 接口概览
        interface_num = Interface.objects.all().count()
        # 测试用例概览
        case_num = Case.objects.all().count()
        # 测试报告概览
        report_num = Report.objects.all().count()
        # 定时任务列表
        task_obj = Taste.objects.all().values("taste_name", "status","taste_time")
    else:
        #项目概览
        project_num=Project.objects.filter(user__user_id=user_obj.user_id).count()
        #接口概览
        interface_num=Interface.objects.filter(project__user__user_id=user_obj.user_id).count()
        #测试用例概览
        case_num=Case.objects.filter(project__user__user_id=user_obj.user_id).count()
        #测试报告概览
        report_num=Report.objects.filter(task__project__user__user_id=user_obj.user_id).count()
        #定时任务列表
        task_obj=Taste.objects.filter(project__user__user_id=user_obj.user_id).values("taste_name","status","taste_time")
    for task in range(len(list(task_obj))):
        num=get_time_by_nexttime(task_obj[task]["taste_time"])
        task_obj[task]["taste_time"]=str(time_add(task_obj[task]["taste_time"],datetime.timedelta(days=num))).split(':')[0]
    page_obj=Paginator(task_obj,4)    #创建一个每页2条数据的分页对象
    page_range = page_obj.page_range  # 总的页数
    page_num_objs = page_obj.page(int(page_num))  # 得到具体页面的页面对象
    content={
        "user_obj":user_obj,
        "project_num":project_num,
        "interface_num":interface_num,
        "case_num":case_num,
        "report_num":report_num,
        "task_obj":task_obj,
        "page_range":page_range,
        "page_num_objs":page_num_objs
    }

    return render(request,'index.html',content)
#登陆功能的视图函数
def login(request):
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")

        if not all([username,password]):
            return render(request,"login.html",{"message":"用户名或密码错误"})
        # next_url=request.GET.get("next")
        #对用户名和密码进行正确性验证，若验证成功返回该登陆对象
        user_obj=auth.authenticate(username=username,password=password)
        if user_obj:
            # 记住用户登陆状态，将登录的用户封装到request.user中

            auth.login(request, user_obj)

            # permissions=Role.objects.filter(user=user_obj).values("permissions__url")
            # permission_list=[]
            # for item in permissions:
            #     permission_list.append(item["permissions__url"])
            #     request.session["permission_list"]=permission_list
            logger.info("登陆成功当前登陆用户为：%s"%request.user)
            return redirect('/index/')
    return render(request,"login.html")
@login_required
def loginout(request):
    '''退出登录'''
    auth.logout(request)
    return render(request,"login.html")
