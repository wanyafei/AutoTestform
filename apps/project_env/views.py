import logging
logger = logging.getLogger("项目管理-环境管理")
from django.shortcuts import render,redirect
from django.urls import reverse
from db.mixin import LoginRequiredMixin
from django.core.paginator import Paginator
from django.views.generic import View
from project_env.models import Project,Environment
from django.contrib import messages
class get_Projects(LoginRequiredMixin,View):
    def get(self,requests,page_num):
        '''获取项目列表视图'''
        logger.info("查询项目列表页数为：%s"%page_num)
        user=requests.user
        if user.is_superuser:
            pro_list = Project.objects.all()  #管理员对应的项目对象
        else:
            pro_list=Project.objects.filter(user__user_id=user.user_id) #获取当前登陆的普通用户的的项目对象
        pageitor=Paginator(pro_list,5)  #创建一页十条的分页对象
        pages=pageitor.page(int(page_num))   #得到具体页数的页面对象
        numbers=pages.number               #当前活动页数
        new_pro_list=pages.object_list    #具体页数的页面数据
        page_nums=pageitor.page_range  #数据可分为的页码数
        #封装页面上下文
        content={
            "pages":pages,
            "page_nums":page_nums,
            "pro_list":new_pro_list,
            "numbers":numbers,
            "user_obj":user
        }
        logger.info("获取项目列表视图的上下文content:%s"%content)
        return render(requests,'project_env/index.html',content)

class add_Projects(LoginRequiredMixin,View):
    def get(self,requests):
        '''获取添加项目页面视图'''
        return render(requests,'project_env/add.html')
    def post(self,requests):
        '''增加项目'''
        #获取前端传入的入参
        logger.info("添加项目参数为：%s" % requests.POST)
        prj_name=requests.POST.get('prj_name')  #项目名称
        #校验项目名称是否重复，重复的项目名称新增失败
        name=Project.objects.filter(prj_name=prj_name)
        pro_description = requests.POST.get('description')  # 项目描述
        prj_version = requests.POST.get('prj_version')  # 项目版本
        pro_status = requests.POST.get('pro_status')  # 项目状态
        if name:
            messages.error(requests,"项目已存在")
        else:
            #项目实例化
            prj=Project(prj_name=prj_name,version=prj_version,description=pro_description,status=pro_status)
            prj.save()
            logger.info("项目%s新增成功！！！" % prj)
            return redirect(reverse('project_env:get_Projects',kwargs={"page_num":1}))
        return render(requests,'project_env/add.html',{"name":prj_name,"pro_description":pro_description,"prj_version":prj_version,"pro_status":pro_status,"message":"项目名称重复了"})


class delete_Projects(LoginRequiredMixin,View):
    def get(self,requests):
        '''删除项目(传入项目ID)'''
        pro_id=requests.GET.get('pro_id')
        Project.objects.filter(prj_id=pro_id).delete()
        logger.info("项目%s删除成功！！！" % pro_id)
        return redirect(reverse('project_env:get_Projects',kwargs={"page_num":1}))

class update_Projects(LoginRequiredMixin,View):
    def get(self,requests):
        '''get获取编辑页面(传入项目ID)数据返现'''
        pro_id=requests.GET.get("pro_id")   #实例化指定的项目对象
        project=Project.objects.filter(prj_id=pro_id)[0]
        content={
            "project":project,
        }
        return render(requests,'project_env/update.html',content)
    def post(self,requests):
        '''编辑信息提交'''
        pro_id=requests.GET.get("pro_id")
        pro_info=Project.objects.filter(prj_id=pro_id)
        logger.info("更新项目%s的更新参数为:%s" %(pro_info,requests.POST))
        prj_name=requests.POST.get("prj_name")           #修改 项目名称
        if Project.objects.filter(prj_name=prj_name) and prj_name!=pro_info[0].prj_name:
            messages.error(requests, "项目已存在")
        else:
            description=requests.POST.get("description")           #修改 项目描述
            prj_version=requests.POST.get("prj_version")           #修改 项目版本
            pro_status=requests.POST.get("pro_status")           #修改 项目状态
            pro_info.update(prj_name=prj_name,version=prj_version,description=description,status=pro_status)
            logger.info("更新项目完成！！！")
            return redirect(reverse('project_env:get_Projects', kwargs={"page_num": 1}))
        project = Project.objects.filter(prj_id=pro_id)[0]
        return render(requests,'project_env/update.html',{"project":project,"message":"项目名称重复了"})
class search_Projects(LoginRequiredMixin,View):
    def get(self,requests):
        '''根据项目名称搜索接口'''
        project_name=requests.GET.get("project_name")
        logger.info("根据项目名称%s搜索接口" % project_name)
        user=requests.user
        if user.is_superuser:
            pro_list=Project.objects.filter(prj_name=project_name)  #实例化要查询的项目对象
        else:
            pro_list = Project.objects.filter(prj_name=project_name,user__user_id=user.user_id)
        content={
            "pro_list":pro_list,
            "user_obj": user
        }
        logger.info("根据项目名称搜索接口的返回值上下文:%s" % content)
        return render(requests,'project_env/index.html',content)
#环境相关
class get_env(LoginRequiredMixin,View):
    def get(self,requests,page_num):
        '''获取环境列表视图'''
        user=requests.user
        if user.is_superuser:
            env_list = Environment.objects.all()  #获取到当前登陆用户对应的项目环境
        else:
            env_list=Environment.objects.filter(project__user__user_id=user.user_id) #获取到当前登陆用户对应的项目环境
        pageitor=Paginator(env_list,2)  #创建一页十条的分页对象
        pages=pageitor.page(int(page_num))   #得到具体页数的页面对象
        numbers=pages.number               #当前活动页数
        new_env_list=pages.object_list    #具体页数的页面数据
        page_nums=pageitor.page_range  #数据可分为的页码数
        #封装页面上下文
        content={
            "pages":pages,
            "page_nums":page_nums,
            "env_list":new_env_list,
            "numbers":numbers,
            "user_obj":user
        }
        logger.info("获取环境列表视图返回值上下文:%s" % content)
        return render(requests,'project_env/env_index.html',content)

class add_env(LoginRequiredMixin,View):
    def get(self,requests):
        '''获取添加环境页面'''
        pro_lists=Project.objects.all()
        content={
            "pro_lists":pro_lists
        }
        return render(requests,'project_env/env_add.html',content)
    def post(self,requests):
        '''添加环境'''
        logger.info("环境添加的参数:%s" % requests.POST)
        env_url=requests.POST.get("env_url")
        env=Environment.objects.filter(url=env_url)
        env_name = requests.POST.get("env_name")
        description = requests.POST.get("description")
        prj_id = requests.POST.get("prj_id")
        pro_lists=Project.objects.filter(prj_id=prj_id)
        env_status = requests.POST.get("env_status")
        if env :
            messages.error(requests,"环境地址host重复了")
        else:
            #实例化环境对象
            envs=Environment(env_name=env_name,url=env_url,description=description,status=env_status,project=pro_lists[0])
            envs.save()
            logger.info("新增环境完成！！！")
            return redirect(reverse('project_env:get_env',kwargs={"page_num":1}))
        return render(requests,'project_env/env_add.html',{"env_name":env_name,"description":description,"pro_lists":pro_lists,"env_url":env_url,"env_status":env_status,"message":"该环境地址库中已经存在"})

class delete_env(LoginRequiredMixin,View):
    def get(self,requests):
        '''删除环境'''
        env_id=requests.GET.get('env_id')
        Environment.objects.get(env_id=env_id).delete()
        logger.info("删除环境完成！！！")
        return redirect(reverse('project_env:get_env',kwargs={"page_num":1}))
class update_env(LoginRequiredMixin,View):
    def get(self,requests):
        '''获取编辑页面'''
        env_id=requests.GET.get("env_id")
        env=Environment.objects.get(env_id=env_id)
        content={
            "env":env,
            "projrcts":Project.objects.all()
        }
        return render(requests,'project_env/env_update.html',content)
    def post(self,requests):
        '''进行编辑接口操作'''
        env_id = requests.GET.get("env_id")
        env_info=Environment.objects.filter(env_id=env_id)
        env_url=requests.POST.get("env_url")
        if Environment.objects.filter(url=env_url) and env_info[0].url != env_url:
            messages.error(requests,"环境地址host重复了")
        else:
            env_name = requests.POST.get("env_name")
            description = requests.POST.get("description")
            env_pro = requests.POST.get("env_pro")
            pro=Project.objects.get(prj_id=env_pro)
            env_status = requests.POST.get("env_status")
            env_info.update(env_name=env_name,description=description,project=pro,url=env_url,status=env_status)
            return redirect(reverse('project_env:get_env', kwargs={"page_num": 1}))
        env=Environment.objects.get(url=env_url)
        projrcts=Project.objects.all()
        content={
            "env":env,
            "projrcts":projrcts,
            "message":"该环境地址库中已经存在"
        }
        return render(requests,'project_env/env_update.html',content)

class search_env(LoginRequiredMixin,View):
    def get(self,requests):
        '''搜索环境接口'''
        user=requests.user
        env_name=requests.GET.get("env_name")
        if user.is_superuser:
            env=Environment.objects.filter(env_name=env_name)
        else:
            env=Environment.objects.filter(env_name=env_name,project__user__user_id=user.user_id)
        content={
            "env_list":env,
            "user_obj": user
        }
        return render(requests,'project_env/env_index.html',content)











