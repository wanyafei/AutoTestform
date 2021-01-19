"""daily URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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


from django.conf.urls import url
from taste_user.views import add_task,search_task,get_next_runtime,run_once,run,edit_task,delete_task,search_task_name
from taste_user.views import search_report,search_report_task_name
from taste_user.views import get_user
urlpatterns = [
    #定时任务管理
    url(r'^add_task$',add_task.as_view(),name='add_task'), #添加任务
    url(r'^search_task/(?P<page_num>\d+)$',search_task.as_view(),name='search_task'),#获取主列表页
    url(r'^get_next_runtime$', get_next_runtime.as_view(), name='get_next_runtime'),  # 获取下次运行时间
    url(r'^run_once$',run_once.as_view(),name='run_once'),#运行一次
    url(r'^run$',run.as_view(),name='run'),#执行、关闭
    url(r'^edit_task/(?P<page_num>\d+)$',edit_task.as_view(),name='edit_task'),  #编辑任务
    url(r'^delete_task$',delete_task.as_view(),name='delete_task'), #删除任务
    url(r'^search_task_name$',search_task_name.as_view(),name='search_task_name'),  #首页搜索接口

    #用户管理
    url(r'^get_user$',get_user.as_view(),name='get_user'),    #获取用户管理列表页面
    #测试报告管理
    url(r'^report/(?P<page_num>\d+)$',search_report.as_view(),name='search_report'), #获取测试报告首页
    url(r'^search_report_task$',search_report_task_name.as_view(),name='search_report_task') #首页搜索
]
