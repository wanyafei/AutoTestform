"""AutoTestPlatform URL Configuration

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
from django.contrib import admin
from django.urls import path
from django.conf.urls import include,url
from AutoTestPlatform.views import index,login,loginout
urlpatterns = [
    url(r'^admin/', admin.site.urls), #后台管理模块
    url(r'^$', index), #首页
    url(r'^index/', index), #首页
    url(r'^login/',login),  #登陆
    url(r'^loginout/',loginout),#退出登录
    url(r'^apitest/',include(('apitest.urls','apitest'),namespace='apitest')),#接口测试模块
    url(r'^webtest/',include(('webtest.urls','webtest'),namespace='webtest')),#页面测试模块
    url(r'^project_env/',include(('project_env.urls','project_env'),namespace='project_env')),#项目&环境管理模块
    url(r'^taste_user/',include(('taste_user.urls','taste_user'),namespace='taste_user')),#任务&用户管理模块
]
