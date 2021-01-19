import datetime,time
import logging
logger = logging.getLogger("定时任务页")
from lib.execute import Execute
from lib.sendemail import sendEmail
from db.mixin import LoginRequiredMixin
from lib.sendtaskemail import send_email
from django.http import JsonResponse
from django.db.models import Q
from django.shortcuts import render,redirect,HttpResponse,reverse
from taste_user.models import Taste,User
from django.core.paginator import Paginator
from apitest.models import Plan,Report
from project_env.models import Project,Environment
from django.views.generic import View
from django.contrib import messages
from lib.task import diango_task
from lib.commonmethod import get_time_by_nexttime,time_add
#定时任务
class add_task(LoginRequiredMixin,View):
    def get(self,requests):
        pro_objs=Project.objects.all() #项目对象
        content={
            "pro_objs":pro_objs
        }
        return render(requests,'taste_user/task_add.html',content)
    def post(self,requests):
        task_name=requests.POST.get("task_name")
        prj_id=requests.POST.get("prj_id")
        env_id = requests.POST.get("env_id")
        plan_ids=requests.POST.getlist("plan_id")
        prj=Project.objects.get(prj_id=prj_id)
        env=Environment.objects.get(env_id=env_id)
        # for plan_id in plan_ids:
        #     plan=Plan.objects.get(plant_id=plan_id)
        task_obj=Taste.objects.filter(taste_name=task_name,project=prj,env=env,plans=plan_ids)
        if task_obj:
            messages.error(requests,"项目已存在")
        else:
            description=requests.POST.get("description")
            # user_id=int(requests.POST.get("user_name"))
            # user_obj=User.objects.get(user_id=user_id)
            corn = requests.POST.get("datetimepicker")
            # for plan_id in plan_ids:
            #     plan = Plan.objects.get(plant_id=plan_id)
            Taste(taste_name=task_name,taste_time=corn,description=description,project=prj,env=env,plans=plan_ids).save()
            return redirect(reverse('taste_user:search_task',kwargs={"page_num":1}))
        return render(requests,'taste_user/task_add.html')

class search_task(LoginRequiredMixin,View):
    def get(self,requests,page_num):
        user = requests.user
        if user.is_superuser:
            tasks = Taste.objects.all()
        else:
            tasks=Taste.objects.filter(project__user__user_id=user.user_id)
        page_obj=Paginator(tasks,3) #创建一个每页2条数据的分页对象
        page_range=page_obj.page_range #总的页数
        page_num_objs=page_obj.page(int(page_num)) #得到具体页面的页面对象
        active_number=page_num_objs.number  #当前活动页码
        obj_lists=page_num_objs.object_list #当前活动页数据
        content={
            "page_range":page_range,
            "active_number":active_number,
            "obj_lists":obj_lists,
            "page_obj":page_num_objs,
            "user_obj":user

        }
        return render(requests,'taste_user/task_index.html',content)
class search_task_name(LoginRequiredMixin,View):
    '''主页搜索接口试图'''
    def get(self,requests):
        task_name=requests.GET.get("task_name")
        user=requests.user
        if user.is_superuser:
            task_objs=Taste.objects.filter(taste_name=task_name)
        else:
            task_objs=Taste.objects.filter(taste_name=task_name,project__user__user_id=user.user_id)
        content={
            "obj_lists":task_objs,
            "user_obj": user
        }
        return render(requests,'taste_user/task_index.html',content)
class edit_task(LoginRequiredMixin,View):
    '''编辑试图'''
    def get(self,requests,page_num):
        task_obj=Taste.objects.get(taste_id=page_num)
        prj_obj=Project.objects.all()
        content={
            "task_obj":task_obj,
            "prj_obj":prj_obj
        }
        return render(requests,'taste_user/task_edit.html',content)
    def post(self,requests,page_num):
        task_obj=Taste.objects.filter(taste_id=page_num)
        task_name=requests.POST.get("task_name")          #任务名称
        prj_id=requests.POST.get("prj_id")
        pro_obj=Project.objects.get(prj_id=prj_id)     #系统对象
        env_id=requests.POST.get("env_id")
        env_obj=Environment.objects.get(env_id=env_id)   #环境对象
        description=requests.POST.get("description")     #任务描述
        corn=requests.POST.get("datetimepicker")   #任务时间
        corn=datetime.datetime.strptime(corn,'%Y-%m-%d:%H')
        plan_ids = requests.POST.getlist("plan_id")      #计划ID列表
        task_obj.update(taste_name=task_name,taste_time=corn,description=description,project=pro_obj,env=env_obj,plans=plan_ids)
        return redirect(reverse('taste_user:search_task',kwargs={"page_num":1}))
class delete_task(LoginRequiredMixin,View):
    '''删除试图'''
    def get(self,requests):
        page_num=requests.GET.get("task_id")
        try:
            Taste.objects.filter(taste_id=page_num).delete()
            return JsonResponse({"code":0,"msg":"删除成功"})
        except Exception as e:
            return JsonResponse({"code":1,"msg":"删除失败"})
class get_next_runtime(LoginRequiredMixin,View):
    '''获取下次运行日期'''
    def get(self,requests):
        task_id=requests.GET.get("task_id")
        task_obj=Taste.objects.filter(taste_id=task_id).values("taste_time")
        cron=list(task_obj)[0].get("taste_time")
        status = Taste.objects.filter(taste_id=task_id).values("status")
        if list(status)[0].get("status")==0 or list(status)[0].get("status")==2:
            num = get_time_by_nexttime(cron)
            new_date = str(time_add(cron, datetime.timedelta(days=num))).split(':')[0]
            return JsonResponse({'code':0,"result":"现在启动后下次的运行时间为："+str(new_date)})
        elif list(status)[0].get("status")==1 or list(status)[0].get("status")==3:
            num = get_time_by_nexttime(cron)
            new_date = str(time_add(cron,datetime.timedelta(days=num))).split(':')[0]
            return JsonResponse({'code':1,"result":new_date})
        else:
            return JsonResponse({'code':2,"result":"获取下次运行时间失败!!!"})
class run(LoginRequiredMixin,View):
    def post(self,requests):
        '''
        开启、关闭、重启 任务
        :param requests:1开启、2和4暂停、3重启    models:(0,'STOP'),(1,'RUNNING'),(2, 'PAUSE'),(3,'RESUME')
        :return: 返回ajax状态码用于前端更改任务状态
        '''
        status_flag=int(requests.POST.get("flag"))
        user = requests.POST.get("user")  # 用户ID
        task_id = requests.POST.get("task_id")  # 任务ID
        task_obj= Taste.objects.get(taste_id=task_id)
        time_obj= str(task_obj.taste_time).split(":")[1]
          # 任务对象
        uuid = "任务对象"+task_id
        task = diango_task()     #实例化定时任务对象
        logger.info("...............定时任务:%s 开始运行................."%task_obj.taste_name)
        task.addtask(run_task, uuid,time_obj, user, task_obj)
        if status_flag==1:
            task.starttask()              #开始定时执行
            Taste.objects.filter(taste_id=task_id).update(status=1)  #更改状态为running
            return JsonResponse({"code":1})
        elif status_flag==2 or status_flag==4:
            task.pausejob(uuid)      #暂停任务
            Taste.objects.filter(taste_id=task_id).update(status=2)  #更改状态pause
            return JsonResponse({"code":2})
        elif status_flag==3:
            task.resumejob(uuid)    # 重启任务
            Taste.objects.filter(taste_id=task_id).update(status=3)  #更改状态resume
            return JsonResponse({"code":3})
        else:
            task.removejob(uuid)
            return JsonResponse({"code":4})
class run_once(LoginRequiredMixin,View):
    '''运行一次'''
    def post(self,requests):
        user=requests.POST.get("user")  #用户ID
        task_id=requests.POST.get("task_id")   #任务ID
        task_obj = Taste.objects.get(taste_id=task_id) #任务对象
        task_report_obj=run_task(user,task_obj)
        # 有错误报告则发送邮件
        if task_report_obj.fail_num>0 or task_report_obj.error_num>0:
            # sendemail_obj=sendEmail(user_obj.email)
            # sendemail_obj.sendEmailFun("http://127.0.0.1:8001/",task_report_obj.task_id)
            # send_email(user_obj.email,"http://127.0.0.1:8001/",task_report_obj.task_id)
            return JsonResponse({"code":0,"message":"有失败或者错误的批次任务,请移至邮件查看详情！！！"})
        else:
            return JsonResponse({"code":1,"message":"测试报告已经生成,可在测试报告管理模块查看。"})

def run_task(user_id,task_obj):
    '''
    运行测试任务，生成对应的report
    :param task_id: 任务ID
    :return: 实例化后的report对象
    '''
    user_obj = User.objects.get(user_id=user_id)
    # task_obj = Taste.objects.get(taste_id=task_id)  # 任务对象
    env_id = task_obj.env.env_id  # 任务对象对应的环境
    plans = eval(task_obj.plans)  # 任务对应的计划list
    case_nums = 0  # 用例总数
    pass_num = 0  # 用例通过数
    fail_num = 0  # 用例失败数
    error_num = 0  # 用例错误数
    case_list = []  # 用例结果大list
    plan_obj_zanshi = None
    for plan in plans:
        plan_obj = Plan.objects.get(plant_id=plan)
        logger.info("该定时任务对应的测试计划：%s"%plan_obj.plant_name)
        cases = eval(plan_obj.content)
        case_nums += len(cases)
        for case in cases:
            logger.info("开始运行用例：%s"%case)
            execute_obj = Execute(case, env_id)
            run_result = execute_obj.run_case()
            case_list.append(run_result)
            if run_result["result"] == "pass":
                pass_num += 1
            elif run_result["result"] == "fail":
                fail_num += 1
            else:
                error_num += 1
    report_name = task_obj.taste_name + "-" + time.strftime("%Y%m%d%H%M%S")
    task_report_obj = Report(report_name=report_name, plant=plan_obj_zanshi, content=case_list, case_num=case_nums,
                             pass_num=pass_num, fail_num=fail_num, error_num=error_num, task=task_obj)
    task_report_obj.save()
    logger.info("已经生成对应的测试报告：%s"%task_report_obj.report_name)
    send_email(user_obj.email, "http://127.0.0.1:8001/", task_report_obj.task_id)
    logger.info("...........已经发送至对应邮箱，请注意查收.............")
    return task_report_obj

#测试报告
class search_report(LoginRequiredMixin,View):
    def get(self,requests,page_num):
        '''获取测试报告'''
        user=requests.user
        if user.is_superuser:
            report_obj_all = Report.objects.all().order_by('-report_id').values()  # 全部报告对象
            all_count=Report.objects.all().count()   # 获取要显示数据库的总数据条数
        else:
            report_obj_all=Report.objects.filter(task__project__user__user_id=user.user_id).order_by('-report_id').values()
            all_count=Report.objects.filter(task__project__user__user_id=user.user_id).count()   # 获取要显示数据库的总数据条数
            if not report_obj_all:
                report_obj_all = Report.objects.filter(plant__project__user__user_id=user.user_id).order_by('-report_id').values()
                all_count=Report.objects.filter(task__project__user__user_id=user.user_id).count()  # 获取要显示数据库的总数据条数
        for report_obj in report_obj_all:
            report_obj["time"]=report_obj.get("report_name").split('-')[1][0:10]
            try:
                id=report_obj.get("task_id")
                task_obj=Taste.objects.get(taste_id=id)
                report_obj["task"]=task_obj.taste_name
            except:
                report_obj["task"]=""
        # page=Paginator(report_obj_all,10)   #创建每页5条数据的翻页对象
        # page_range=page.page_range    #总页数
        # page_info=page.page(int(page_num))#具体页分页对象
        # content={
        #     "page_info":page_info,
        #     "page_info_list":page_info.object_list,
        #     "page_range":page_range,
        #     "user_obj": user
        # }
        # return render(requests,'taste_user/report_index.html',content)
        from lib.pageinfo import pageinfo
        page_info=pageinfo(page_num,all_count,'/taste_user/report',)
        url_list=report_obj_all[page_info.start_data():page_info.end_data()]
        content={
            "user_list":url_list,
            "page_info":page_info
        }
        return render(requests, 'taste_user/report_index.html', content)



class search_report_task_name(LoginRequiredMixin,View):
    #通过报告名称和任务名称组合搜索
    def get(self,requests):
        report_name=requests.GET.get("report_name")
        task_name=requests.GET.get("task_name")
        user=requests.user
        if user.is_superuser:
            page_info=Report.objects.filter(Q(report_name=report_name) | Q(task__taste_name=task_name)).order_by('-report_id').values()
        else:
            page_info=Report.objects.filter(Q(report_name=report_name) | Q(task__taste_name=task_name),task__project__user__user_id=user.user_id).order_by('-report_id').values()
        for report_obj in page_info:
            report_obj["time"]=report_obj.get("report_name").split('-')[1][0:10]
            try:
                id=report_obj.get("task_id")
                task_obj=Taste.objects.get(taste_id=id)
                report_obj["task"]=task_obj.taste_name
            except:
                report_obj["task"]=""
        content={
            "page_info_list":page_info,
            "user_obj":user
        }
        return render(requests, 'taste_user/report_index.html', content)

#用户管理
class get_user(LoginRequiredMixin,View):
    def get(self,requests):
        return HttpResponse("ok........")












