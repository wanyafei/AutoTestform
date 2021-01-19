from django.shortcuts import render,redirect,HttpResponse
from django.http import JsonResponse
from db.mixin import LoginRequiredMixin
from django.urls import reverse
from django.db.models import Q
import json,time,os
from AutoTestPlatform.settings import BASE_DIR,UPLOAD_ROOT
from lib.execute import Execute
from lib.excelmethod import excelOpern
from django.views.generic import View
from django.http import FileResponse
from apitest.models import Interface,Case,Plan,Report
from project_env.models import Project,Environment
from taste_user.models import User,Taste
from django.core.paginator import Paginator
class get_interviews(LoginRequiredMixin,View):
    def get(self,requests,page_num):
        '''获取接口管理列表视图'''
        user=requests.user
        if user.is_superuser:
            interfaces_lists = Interface.objects.all()  # 获取到当前登陆用户所属项目对应的接口对象
        else:
            interfaces_lists=Interface.objects.filter(project__user__user_id=user.user_id)  #获取到当前登陆用户所属项目对应的接口对象
        page_obj=Paginator(interfaces_lists,per_page=8) #对现有数据实例化出一个每页展示2条的分页对象
        page_num_obj=page_obj.page(int(page_num))   #获取具体页面的对象
        active_number=page_num_obj.number         #当前活动页数
        page_num_obj_lists=page_num_obj.object_list    #具体页面的对象数据列表
        number_range=page_obj.page_range    #现有数据可分的页码数
        content={
            "number_range":number_range,
            "page_num_obj_lists":page_num_obj_lists,
            "active_number":active_number,
            "page_num_obj":page_num_obj,
            "user_obj":user
        }
        return render(requests,'apitest/interface_index.html',content)


class add_interviews(LoginRequiredMixin,View):
    def get(self,requests):
        '''获取添加接口页面'''
        projects=Project.objects.all()
        content={
            "projects":projects
        }
        return render(requests,'apitest/interface_add.html',content)

    def post(self,requests):
        '''添加接口'''
        if_name=requests.POST.get("if_name")   #接口名称
        prj_id=requests.POST.get("prj_id")     #项目id
        project=Project.objects.get(prj_id=prj_id) #项目对象
        url=requests.POST.get("url")           #接口url
        exit_obj = Interface.objects.filter(Q(if_url=url) & Q(project=project))
        method=requests.POST.get("method")     #请求方法
        data_type = requests.POST.get("data_type")  #传输类型
        description = requests.POST.get("description")  #接口描述
        request_header_data = requests.POST.get("request_header_data")  #请求头对象
        request_body_data = requests.POST.get("request_body_data")      #请求体对象
        response_header_data = requests.POST.get("response_header_data")  #响应头对象
        response_body_data = requests.POST.get("response_body_data")  # 相应体对象
        if exit_obj:
            return JsonResponse({'code':1,"data":"该环境下的接口已经存在了"})
        else:
            if_obj=Interface(if_name=if_name,if_url=url,method=method,data_type=data_type,project=project,description=description,
                  request_header_param=request_header_data,request_body_param=request_body_data,
                  response_header_param=response_header_data,response_body_param=response_body_data
                  )
            if_obj.save()
            # return redirect(reverse('apitest:get_interviews',kwargs={"page_num":1}))
            return JsonResponse({'code':2,"data":"添加接口成功"})


class del_interviews(LoginRequiredMixin,View):
    def get(self,requests):
        '''删除接口'''
        interface_id=requests.GET.get('interface_id')
        Interface.objects.get(if_id=interface_id).delete()
        return redirect(reverse('apitest:get_interviews',kwargs={"page_num":1}))
class update_interviews(LoginRequiredMixin,View):
    def get(self,requests):
        '''获取编辑页面'''
        interface_id=requests.GET.get('interface_id')
        if_obj=Interface.objects.get(if_id=interface_id)
        if if_obj.request_header_param.count(',')>=2:    #请求头
            request_header_list=if_obj.request_header_param[1:-1].split('},{')
            qingqoutou = [request_header_list[i] + "}" if i % 2 == 0 else "{" + request_header_list[i] for i in
                          range(len(request_header_list))]
            qingqoutou_lists = [json.loads(ii) for ii in qingqoutou]
        elif if_obj.request_header_param.count(',') == 1:
            qingqoutou_lists=json.loads(if_obj.request_header_param[1:-1])
        else:
            qingqoutou_lists= {}
        if if_obj.request_body_param.count(',')>=2:   #请求体
            request_body_lists = if_obj.request_body_param[1:-1].split('},{')
            requ_bo_lists = [request_body_lists[i] + "}" if i % 2 == 0 else "{" + request_body_lists[i] for i in
                             range(len(request_body_lists))]
            qingqouti_lists = [json.loads(ii) for ii in requ_bo_lists]
        elif if_obj.request_body_param.count(',') == 1:
            qingqouti_lists = json.loads(if_obj.request_body_param[1:-1])
        else:
            qingqouti_lists= {}
        if if_obj.response_header_param.count(',')>=2:   #相应头
            response_header_lists = if_obj.response_header_param[1:-1].split('},{')
            resp_he_lists = [response_header_lists[i] + "}" if i % 2 == 0 else "{" + response_header_lists[i] for i in
                             range(len(response_header_lists))]
            xiangyingtou_lists = [json.loads(ii) for ii in resp_he_lists]
        elif if_obj.response_header_param.count(',') == 1:
            xiangyingtou_lists = json.loads(if_obj.response_header_param[1:-1])
        else:
            xiangyingtou_lists= {}
        if if_obj.response_body_param.count(',')>=2:   #相应体
            response_body_lists = if_obj.response_body_param[1:-1].split('},{')
            resp_bo_lists = [response_body_lists[i] + "}" if i % 2 == 0 else "{" + response_body_lists[i] for i in
                             range(len(response_body_lists))]
            xiangyingti_lists = [json.loads(ii) for ii in resp_bo_lists]
        elif if_obj.response_body_param.count(',') == 1:
            xiangyingti_lists = json.loads(if_obj.response_body_param[1:-1])
        else:
            xiangyingti_lists={}
        prjs=Project.objects.all()
        content={
            "if_obj":if_obj,
            "prjs":prjs,
            "qingqoutou_lists":qingqoutou_lists,
            "qingqouti_lists": qingqouti_lists,
            "xiangyingtou_lists": xiangyingtou_lists,
            "xiangyingti_lists": xiangyingti_lists,
            "qingqiutou_flag":if_obj.request_header_param.count(','),
            "qingqiuti_flag":if_obj.request_body_param.count(','),
            "xiangyingtou_flag":if_obj.response_header_param.count(','),
            "xiangyingti_flag":if_obj.response_body_param.count(',')
        }
        return render(requests,'apitest/interface_update.html',content)
    def post(self,requests):
        '''进行编辑操作'''
        interface_id=requests.GET.get('if_obj_id')
        inter_info=Interface.objects.filter(if_id=interface_id)
        if_name=requests.POST.get('if_name') #接口名称
        prj_id=requests.POST.get('prj_id')   #编辑接口的ID
        url=requests.POST.get('url')     #URL
        project=Project.objects.get(prj_id=prj_id)   #接口所属的项目
        exit_obj = Interface.objects.filter(Q(if_url=url) & Q(project=project))
        method = requests.POST.get("method")  # 请求方法
        data_type = requests.POST.get("data_type")  # 传输类型
        description = requests.POST.get("description")  # 接口描述
        request_header_data = requests.POST.get("request_header_data")  # 请求头对象
        request_body_data = requests.POST.get("request_body_data")  # 请求体对象
        response_header_data = requests.POST.get("response_header_data")  # 响应头对象
        response_body_data = requests.POST.get("response_body_data")  # 相应体对象
        if exit_obj and inter_info[0].if_url != url and inter_info[0].project.prj_id != prj_id:
            return JsonResponse({'code':1,"data":"该环境下的接口已经存在了"})
        else:
            inter_info.update(if_name=if_name, if_url=url, method=method, data_type=data_type, project=project,
                               description=description,
                               request_header_param=request_header_data, request_body_param=request_body_data,
                               response_header_param=response_header_data, response_body_param=response_body_data
                               )
            return JsonResponse({'code':2,"data":"添加接口成功"})
class search_interviews(LoginRequiredMixin,View):
    def get(self,requests):
        '''搜索接口，入参为接口名称'''
        serach_interface_name = requests.GET.get('interface_name')
        user=requests.user
        if user.is_superuser:
            serach_interface_obj = Interface.objects.filter(if_name=serach_interface_name)
        else:
            serach_interface_obj = Interface.objects.filter(if_name=serach_interface_name,project__user__user_id=user.user_id)
        content={
            "page_num_obj_lists":serach_interface_obj,
            "user_obj": user
        }
        return render(requests,'apitest/interface_index.html',content)
class download_file(LoginRequiredMixin,View):
    def get(self,requests):
        '''下载接口模版'''
        file=open(os.path.join(BASE_DIR,'static/file',"接口模版.xlsx"),'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="template.xlsx"'
        return response
class upload_file(LoginRequiredMixin,View):
    def post(self,request):
        '''上传的文件入库'''
        file_obj=request.FILES.get('select_file')
        if not os.path.exists(UPLOAD_ROOT):
            os.makedirs(UPLOAD_ROOT)
        try:
            if file_obj is None:
                return HttpResponse('请选择要上传的文件！')
            #循环二进制文件写入 chunk方法是块级读取写入文件
            f=open(os.path.join(BASE_DIR,UPLOAD_ROOT,file_obj.name),'wb')
            for chunk in file_obj.chunks():
                f.write(chunk)
            f.close()
        except Exception as e:
            return JsonResponse({'code':2,"message":"上传文件失败"})
        #进行文件解析、校验、写入数据库
        upload_file_obj=excelOpern(UPLOAD_ROOT+"/"+file_obj.name,"接口")
        for file in upload_file_obj.read_excel_rows_dict():
            interface_name=file["接口名称"]
            prject_name = file["所属项目"]
            api = file["api地址"]
            method = file["请求方式"]
            contenttype = file["数据传输方式"]
            interface_desc = file["接口描述"]
            request_head = file["请求头"]
            # 重新组装请求头信息
            request_head_list=request_head.split(":")
            request_head_list_all=[]
            request_head_dict = {}
            request_head_dict["var_name"]=request_head_list[0]
            request_head_dict["var_remark"] = request_head_list[1]
            request_head_list_all.append(request_head_dict)
            request_body = eval(file["请求体"])
            # 重新组装请求体信息
            request_body_list_all=[]
            for body in request_body.items():
                request_body_dict = {}
                for item in range(len(body)):
                    if item==0:
                        request_body_dict["var_name"]=body[item]
                    elif item==1:
                        request_body_dict["var_remark"] =body[item]
                request_body_list_all.append(request_body_dict)
            response_body = eval(file["响应体"])
            # 重新组装相应体信息
            response_body_list_all = []
            for body in response_body.items():
                response_body_dict = {}
                for item in range(len(body)):
                    if item == 0:
                        response_body_dict["var_name"] = body[item]
                    elif item == 1:
                        response_body_dict["var_remark"] = body[item]
                response_body_list_all.append(response_body_dict)
            response_head = file["响应头"]

            if not all([interface_name,prject_name,api,method,contenttype,request_head_list_all,response_body_list_all]):
                return JsonResponse({'code':1,"message":"文件有必输项目为空"})
            try:
                project = Project.objects.get(prj_name=prject_name)  # 项目对象
            except Exception as e:
                return JsonResponse({'code': 1, "message": "文件中项目名称有误"})
            exit_obj = Interface.objects.filter(Q(if_url=api) & Q(project=project) & Q(if_name=interface_name))
            if exit_obj:
                return JsonResponse({'code': 1, "message": "接口已经存在"})

            if_obj=Interface(if_name=interface_name, if_url=api, method=method, data_type=contenttype,
                                   project=project,
                                   description=interface_desc,
                                   request_header_param=json.dumps(request_head_list_all),
                                   request_body_param=json.dumps(request_body_list_all),
                                   response_header_param=json.dumps(response_head),
                                   response_body_param=json.dumps(response_body_list_all)
                                   )
            if_obj.save()
        return JsonResponse({'code': 0, "message": "文件导入成功！"})





class get_testcase(LoginRequiredMixin,View):
    def get(self,requests,page_num):
        '''获取用例列表的视图'''
        user=requests.user
        if user.is_superuser:
            testcase_obj = Case.objects.all()  # 获取当前用户所对应的所有的用例对象
        else:
            testcase_obj=Case.objects.filter(project__user__user_id=user.user_id)  #获取当前用户所对应的所有的用例对象
        page_obj=Paginator(testcase_obj,per_page=8)  #实例化出每页2条数据的页面对象
        page_range=page_obj.page_range   #现有数据可分为的页码数
        page_num_obj=page_obj.page(int(page_num))   #具体页面数据对象
        page_active_num=page_num_obj.number     #当前活动页面页码
        number_range=page_num_obj.object_list#当前活动页面具体数据列表
        content={
            "number_range":number_range,
            "page_active_num":page_active_num,
            "page_num_obj":page_num_obj,
            "page_range":page_range,
            "user_obj":user
        }
        return render(requests,'apitest/testcase_index.html',content)
class add_testcase(LoginRequiredMixin,View):
    def get(self,requests):
        '''获取添加用例的视图'''
        page_obj_all=Project.objects.all()
        content={
            "page_obj_all":page_obj_all
        }
        return render(requests,'apitest/testcase_add.html',content)
    def post(self,requests):
        '''添加用例'''
        case_name=requests.POST.get("case_name")   #用例名称
        prj_id = requests.POST.get("prj_id")      #项目id
        project=Project.objects.get(prj_id=prj_id)  #实例化project对象
        content=requests.POST.get("content")      #content
        description = requests.POST.get("description")  #用例描述
        exit_obj=Case.objects.filter(Q(project=project) & Q(case_name=case_name))
        if exit_obj:
            return JsonResponse({"code":0,"message":"该项目下的用例已经存在！！！"})
        else:
            Case(case_name=case_name,project=project,description=description,content=content).save()
            return JsonResponse({"code":1,"message":"用例添加成功！！！"})
class search_testcase(LoginRequiredMixin,View):
    def get(self,requests):
        '''搜索操作'''
        testcase_name=requests.GET.get("testcase_name")
        user=requests.user
        if user.is_superuser:
            case_obj=Case.objects.filter(case_name=testcase_name)
        else:
            case_obj=Case.objects.filter(case_name=testcase_name,project__user__user_id=user.user_id)
        content={
            "number_range":case_obj,
            "user_obj": user
        }
        return render(requests,'apitest/testcase_index.html',content)

class update_testcase(LoginRequiredMixin,View):
    def get(self,requests):
        '''获取更新视图'''
        testcase_id=requests.GET.get("testcase_id")
        case_obj=Case.objects.get(case_id=testcase_id)
        projects=Project.objects.all()
        if_obj_by_project=Interface.objects.filter(project=Project.objects.get(prj_id=case_obj.project.prj_id)).values()
        content={
            "case_obj":case_obj,
            "projects":projects,
            "if_obj_by_project":if_obj_by_project
        }
        return render(requests,'apitest/testcase_update.html',content)
    def post(self,requests):
        '''进行更新操作'''
        case_id=requests.POST.get("case_id")
        case_obj=Case.objects.filter(case_id=case_id)
        case_name = requests.POST.get("case_name")  # 用例名称
        prj_id = requests.POST.get("prj_id")  # 项目id
        project = Project.objects.get(prj_id=prj_id)  # 实例化project对象
        content = requests.POST.get("content")  # content
        description = requests.POST.get("description")  # 用例描述
        exit_obj = Case.objects.filter(Q(project=project) & Q(case_name=case_name))
        if exit_obj and case_obj.first().case_name != case_name and case_obj.first().project.prj_id != prj_id:
            return JsonResponse({"code": 0, "message": "该项目下的用例已经存在！！！"})
        else:
            case_obj.update(case_name=case_name, project=project, description=description, content=content)
            return JsonResponse({"code": 1, "message": "用例添加成功！！！"})
class del_testcase(LoginRequiredMixin,View):
    def get(self,requests):
        '''进行删除操作'''
        testcase_id=requests.GET.get("testcase_id")
        Case.objects.get(case_id=testcase_id).delete()
        return redirect(reverse('apitest:get_testcase',kwargs={"page_num":1}))
class find_prj_if(LoginRequiredMixin,View):
    def get(self,requests):
        request_type=requests.GET.get("type")
        prj_id=requests.GET.get("prj_id")

        #通过项目ID查找项目下的接口
        if request_type == "get_if_by_prj_id":
            interface=Interface.objects.filter(project=Project.objects.get(prj_id=prj_id)).values()
            #查询并将结果转换成json
            return JsonResponse(list(interface),safe=False)
        # 通过项目ID查找项目下的环境
        elif request_type == "get_env_by_prj_id":
            env=Environment.objects.filter(Q(project=Project.objects.get(prj_id=prj_id)) & Q(status=1)).values()
            return JsonResponse(list(env),safe=False)
        # 通过项目ID查找项目下的用例
        elif request_type == "get_tc_by_prj_id":
            tc=Case.objects.filter(project=Project.objects.get(prj_id=prj_id)).values()
            return JsonResponse(list(tc),safe=False)
        # 通过接口ID查找接口信息
        elif request_type == "get_if_by_if_id":
            if_id = requests.GET.get("if_id")
            interface=Interface.objects.filter(if_id=if_id).values()
            return JsonResponse(list(interface),safe=False)
        elif request_type == "get_plan_by_prj_env_id":
            '''通过项目和环境ID，查找对应的计划'''
            env_id=requests.GET.get("env_id")
            plan_objs=Plan.objects.filter(Q(project=Project.objects.get(prj_id=prj_id)) & Q(env=Environment.objects.get(env_id=env_id))).values()
            return JsonResponse(list(plan_objs),safe=False)
        elif request_type == "get_user_by_prj_id":
            '''通过项目id查找对应的用户,基于双下划线的一对多反向查询'''
            #user_objs=Project.objects.filter(prj_id=prj_id).values("user__user_id","user__username")
            '''基于双下划线的一对多正向查询'''
            user_objs=User.objects.filter(project__prj_id=prj_id).values("user_id","username")
            return JsonResponse(list(user_objs),safe=False)
class case_run(LoginRequiredMixin,View):
    def post(self,requests):
        #运行用例调试类视图
        case_id=requests.POST.get("case_id")   #用例ID
        env_id=requests.POST.get("env_id")    #环境
        execute=Execute(case_id,env_id)#实例化执行类得到execute()对象
        execute_result=execute.run_case()  #执行后的结果
        #调试结果返回至前端回调函数
        return JsonResponse(execute_result)
class get_plant(LoginRequiredMixin,View):
    '''获取测试计划试图'''
    def get(self,requests,page_num):
        user=requests.user
        if user.is_superuser:
            plan_obj = Plan.objects.all()  # 查出所有的测试计划对象,管理员
        else:
            plan_obj=Plan.objects.filter(project__user__user_id=user.user_id)  #查出普通用户所有的测试计划对象
        page=Paginator(plan_obj,per_page=2)  #创建出一个翻页对象
        page_range=page.page_range    #可分的页数
        page_num_obj=page.page(int(page_num))  #具体页面可翻页对象
        active_num=page_num_obj.number  #具体页面活动页码数
        plan_objs=page_num_obj.object_list #具体页面可翻页对象对应的数据列表
        content={
            "page_range":page_range,
            "plan_objs":plan_objs,
            "active_num":active_num,
            "page_num_obj":page_num_obj,
            "user_obj":user
        }
        return render(requests,'apitest/plant_index.html',content)
class add_plant(LoginRequiredMixin,View):
    '''添加测试计划视图'''
    def get(self,requests):
        '''获取添加页面'''
        pro_objs=Project.objects.all()  #获取所有项目对象供添加页面选择
        content={
            "pro_objs":pro_objs
        }
        return render(requests,'apitest/plant_add.html',content)
    def post(self,requests):
        '''进行添加操作'''
        plan_name=requests.POST.get("plan_name")  #计划名称
        prj_id=requests.POST.get("prj_id")     #项目ID
        pro_obj=Project.objects.get(prj_id=prj_id) #实例出项目对象
        env_id=requests.POST.get("env_id")   #环境
        env_obj=Environment.objects.get(env_id=env_id)  #实例化环境对象
        description=requests.POST.get("description")  #测试计划描述
        contents=requests.POST.getlist("case_id")     #用例集合
        plan_obj=Plan(plant_name=plan_name,project=pro_obj,env=env_obj,description=description,content=contents)
        plan_obj.save()
        return redirect(reverse('apitest:get_plant',kwargs={"page_num":1}))

class update_plant(LoginRequiredMixin,View):
    '''更新测试计划视图'''
    def get(self,requests):
        '''获取更新页面'''
        plan_id=requests.GET.get("plan_id")  #具体要更新的计划ID
        update_obj=Plan.objects.get(plant_id=plan_id)
        pro_objs = Project.objects.all()
        content={
            "update_obj":update_obj,
            "pro_objs":pro_objs
        }
        return render(requests,'apitest/plant_update.html',content)
    def post(self,requests):
        '''进行更新操作'''
        plan_obj_id=requests.GET.get("plan_id")
        update_obj=Plan.objects.filter(plant_id=plan_obj_id)
        plan_name=requests.POST.get("plan_name")
        prj_id=requests.POST.get("prj_id")
        pro_obj=Project.objects.get(prj_id=prj_id)
        env_id=requests.POST.get("env_id")
        env_obj=Environment.objects.get(env_id=env_id)
        description=requests.POST.get("description")
        case_id=eval(requests.POST.get("case_id"))
        plan=Plan.objects.filter(plant_name=plan_name,project=pro_obj,env=env_obj,content=case_id)
        if plan:
            return JsonResponse({"code":0,"msg":"该测试计划已经重复了,可修改部分字段后重新编辑。"})
        else:
            update_obj.update(plant_name=plan_name,project=pro_obj,env=env_obj,description=description,content=case_id)
            return JsonResponse({"code":1,"msg":"编辑成功！！！"})
class delete_plant(LoginRequiredMixin,View):
    '''删除测试计划视图'''
    def get(self,requests):
        '''删除操作'''
        plan_id=requests.GET.get("plan_id")
        Plan.objects.get(plant_id=plan_id).delete()
        return redirect(reverse('apitest:get_plant',kwargs={"page_num":1}))
class search_plan(LoginRequiredMixin,View):
    '''搜索测试计划试图'''
    def get(self,requests):
        plan_name=requests.GET.get("plan_name")
        user=requests.user
        if user.is_superuser:
            plan_objs=Plan.objects.filter(plant_name=plan_name)
        else:
            plan_objs = Plan.objects.filter(plant_name=plan_name,project__user__user_id=user.user_id)
        content={
            "plan_objs":plan_objs,
            "user_obj": user
        }
        return render(requests,'apitest/plant_index.html',content)


class run_plan(LoginRequiredMixin,View):
    '''运行测试报告视图'''
    def post(self,requests):
        plan_id=requests.POST.get("plan_id")
        plan=Plan.objects.get(plant_id=plan_id)
        env=plan.env.env_id      #计划对象对应的环境
        content=eval(plan.content)  #计划对应的content
        case_num=len(content)  #测试用例数
        pass_num=0             #用例通过数
        fail_num=0            # 用例失败数
        error_num=0           # 用例错误数
        case_list=[]          #测试计划中测试用例集
        for case_obj in content:
            execute_obj=Execute(case_obj,env)
            run_result=execute_obj.run_case()
            case_list.append(run_result)
            if run_result["result"] == "pass":
                pass_num+=1
            elif run_result["result"] == "fail":
                fail_num+=1
            else:
                error_num += 1
        report_name=plan.plant_name+"-"+time.strftime("%Y%m%d%H%M%S")
        if Report.objects.filter(plant=plan):
            Report.objects.filter(plant=plan).update(report_name=report_name,plant=plan,content=case_list,case_num=case_num,
                                                     pass_num=pass_num,fail_num=fail_num,error_num=error_num,task=None)
        else:
            Report(report_name=report_name,plant=plan,content=case_list,case_num=case_num,
                   pass_num=pass_num,fail_num=fail_num,error_num=error_num,task=None).save()
        return HttpResponse(plan.plant_name+"执行成功！")
class query_report(LoginRequiredMixin,View):
    '''查看测试报告视图'''
    def get(self,requests):
        plan_id=requests.GET.get('plan_id',None)    #测试报告对应的测试计划ID
        task_id=requests.GET.get('task_id',None)    #测试报告对应的测试任务ID
        report_id=requests.GET.get('report_id',None)   #测试报告对应的测试报告ID
        if plan_id and report_id is None:
            plan=Plan.objects.get(plant_id=plan_id)
            report=Report.objects.filter(Q(plant=plan) & Q(task_id=None)).first() #report对象
            report_content=eval(report.content)   #report content内容
            content={
            "report":report,
            "report_content":report_content
            }
        elif report_id:
            report_obj=Report.objects.get(report_id=report_id)
            report_content = eval(report_obj.content)  # report content内容
            content={
                "report": report_obj,
                "report_content": report_content
            }
        else:
            task_obj=Taste.objects.get(taste_id=task_id)
            report = Report.objects.filter(task=task_obj).order_by('-report_id').first()
            report_content = eval(report.content)  # report content内容
            content={
                "report": report,
                "report_content": report_content
        }
        return render(requests,'testreport.html',content)












