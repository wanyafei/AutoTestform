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
from apitest.views import get_interviews,add_interviews,del_interviews,update_interviews,search_interviews,download_file,upload_file
from apitest.views import get_testcase,add_testcase,search_testcase,update_testcase,del_testcase,find_prj_if,case_run
from apitest.views import get_plant,add_plant,update_plant,delete_plant,run_plan,query_report,search_plan
urlpatterns = [
    #接口管理
    url(r'^get_interviews/(?P<page_num>\d+)$',get_interviews.as_view(),name='get_interviews'),   #获取接口列表
    url(r'^search_interviews$',search_interviews.as_view(),name='search_interviews'),  #搜索接口
    url(r'^add_interviews$',add_interviews.as_view(),name='add_interviews'),  #添加接口
    url(r'^update_interviews$', update_interviews.as_view(), name='update_interviews'),  # 编辑接口
    url(r'^del_interviews$', del_interviews.as_view(), name='del_interviews'),  # 编辑接口
    url(r'^download_file$', download_file.as_view(), name='download_file'),  # 下载模版接口
    url(r'^upload_file$', upload_file.as_view(), name='upload_file'),  # 上传文件接口

    #用例管理
    url(r'^get_testcase/(?P<page_num>\d+)$', get_testcase.as_view(), name='get_testcase'),  # 获取用例列表
    url(r'^add_testcase$', add_testcase.as_view(), name='add_testcase'),  # 添加用例
    url(r'^search_testcase$', search_testcase.as_view(), name='search_testcase'),  # 搜索用例
    url(r'^update_testcase$', update_testcase.as_view(), name='update_testcase'),  # 编辑用例
    url(r'^del_testcase$', del_testcase.as_view(), name='del_testcase'),  # 编辑用例
    url(r'^find_prj_if$', find_prj_if.as_view(), name='find_prj_if'),  # 查找项目下对应的接口
    url(r'^case_run$',case_run.as_view(),name='case_run'), #案例运行接口

    #测试计划管理
    url(r'^get_plant/(?P<page_num>\d+)$',get_plant.as_view(),name='get_plant'), #获取测试计划列表页
    url(r'^search_plan$',search_plan.as_view(),name='search_plan'), #主页搜索测试计划
    url(r'^add_plant$',add_plant.as_view(),name='add_plant'),#添加测试计划
    url(r'^update_plant$',update_plant.as_view(),name='update_plant'),#更新测试计划
    url(r'^delete_plant$',delete_plant.as_view(),name='delete_plant'),#删除测试计划
    url(r'^run_plan$',run_plan.as_view(),name='run_plan'),#运行测试计划
    url(r'^query_report$',query_report.as_view(),name='query_report'),#查看测试报告
]
