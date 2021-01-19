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
from project_env.views import get_Projects,add_Projects,delete_Projects,update_Projects,search_Projects
from project_env.views import get_env,add_env,delete_env,update_env,search_env

urlpatterns = [
    #项目
    url(r'^get_Projects/(?P<page_num>\d+)$',get_Projects.as_view(),name='get_Projects'),   #获取项目列表
    url(r'^add_Projects$',add_Projects.as_view(),name='add_Projects'),   #get获取添加项目页面，post添加项目信息
    url(r'^delete_Projects$',delete_Projects.as_view(),name='delete_Projects'),   #删除项目
    url(r'^update_Projects$',update_Projects.as_view(),name='update_Projects'),   #编辑项目
    url(r'^search_Projects$',search_Projects.as_view(),name='search_Projects'),   #搜索项目接口

    #环境
    url(r'^get_env/(?P<page_num>\d+)$',get_env.as_view(),name='get_env'),   #获取环境列表
    url(r'^search_env$',search_env.as_view(),name='search_env'),   #搜索环境接口
    url(r'^add_env$',add_env.as_view(),name='add_env'),   #get获取添加环境页面，post添加环境信息
    url(r'^update_env$', update_env.as_view(), name='update_env'),  # 编辑环境
    url(r'^delete_env$', delete_env.as_view(), name='delete_env'),  # 删除环境

]
