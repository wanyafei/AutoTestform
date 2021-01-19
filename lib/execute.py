import requests,json,re
from project_env.models import Environment
from apitest.models import Case,Interface
import logging
#案例执行类方法
class Execute():
    def __init__(self,case_id,env_id):
        '''
        初始化类方法
        :param case_id: 用例ID
        :param env_id: 环境ID
        '''
        self.case_id=case_id
        self.env_id=env_id
        self.url,self.prj_id=self.get_env_by_envid(self.env_id) #通过环境ID取环境URL及项目ID

        self.extract_global_dict={}  #定义全局的存储提取字段值的空字典项

    def run_case(self):
        '''
        执行运行接口
        :return: 返回页面所需的展示数据{case_id,case_name,step_counter[inter1,inter2],result}
        '''
        case_obj=Case.objects.get(case_id=self.case_id)  #case对象
        case_content=case_obj.content  #case_content
        logging.info("用例对应的content内容是：%s"%case_content)
        if isinstance(case_content,str):
            case_content=json.loads(case_content)
        case_result = {"case_id":self.case_id,"case_name":case_obj.case_name,"result":"pass"}
        case_step_list=[]
        if not case_content:
            case_result["result"] = "contents is empty"
        for contents in case_content:
            step_info=self.step(contents)    #step()返回封装后的接口测试结果
            case_step_list.append(step_info)
            if step_info["result"]=="fail":
                case_result["result"]="fail"
                break
            if step_info["result"]=="Error":
                case_result["result"] = "Error"
                break
        case_result["step_list"]=case_step_list
        logging.info("用例运行后的运行结果是%s"%case_result)
        return case_result


    def step(self,content):
        '''
        接口测试步骤函数
        :param content: interface_counter
        :return: 返回测试封装后的字典对象
        '''
        if_id=content["if_id"]
        inter_obj=Interface.objects.get(if_id=if_id)
        logging.info("用例包含的接口是：%s"%inter_obj.if_name)
        var_list=self.extract_variables(content) #提取的值
        #提取值替换变量
        if var_list:
            for variable_field in var_list:
                try:
                    reality_value=self.extract_global_dict[variable_field]
                except ValueError:
                    reality_value=""
                content=json.loads(self.repalce_var(content,variable_field,reality_value))
        #接口请求
        if_info_dict = {"url": inter_obj.if_url, "header": content["header"], "body": content["body"]}
        if_info_dict["url"] = self.url + inter_obj.if_url  # 接口URL
        if_info_dict["method"] = inter_obj.method  # 请求方法
        if_info_dict["data_type"] = inter_obj.data_type  # 数据类型
        logging.info("接口的参数为：%s"%if_info_dict)
        try:
            res=self.run_interface(if_info_dict["url"],if_info_dict["method"],if_info_dict["header"],if_info_dict["body"],if_info_dict["data_type"])
            logging.info("接口运行返回值是：%s"%res)
            if_info_dict["res_status_code"]=res.status_code
            if_info_dict["res_content"] =res.text
        except requests.RequestException as e:
            if_info_dict["result"]="Error"
            if_info_dict["msg"]=str(e)
            return if_info_dict
        #提取参数处理,将提取参数设置成全局的变量
        if content["extract"]:
            self.set_extract(content["extract"],if_info_dict["res_content"])
        #检查点处理
        if content["validators"]:
            if_info_dict["result"],if_info_dict["msg"] =self.validator_result(content["validators"],if_info_dict["res_content"])
        else:
            if_info_dict["result"]="pass"
            if_info_dict["msg"]="没有设置检查项"

        return if_info_dict
    def repalce_var(self,content,extract_value,reality_value):
        '''
        替换函数，将提取的字段值赋值给$对应的字段
        :param content: 内容
        :param extract_value: 下个接口要使用的带有$的字段
        :param reality_value: 上个接口提取的字段值
        :return:替换后的字串
        '''
        if not isinstance(content,str):
            content_str=json.dumps(content)
        extract_value="$"+extract_value
        content=content_str.replace(str(extract_value),str(reality_value))
        return content
    def extract_variables(self,content):
        '''
        提取接口字段中带有$的值列表
        :param content:interface_counter
        :return:返回正则匹配到的一个列表组合
        '''
        regexp_variable=r"\$([\w_]+)"#定义正则匹配规则-匹配含有$的字符
        if not isinstance(content,str):
            str_content=str(content)
        try:
            extract_list=re.findall(regexp_variable,str_content)
            return extract_list
        except TypeError:
            return []
    def validator_result(self,validator_list,res):
        '''
        验证结果函数
        :param validator_list: 验证字段列表
        :param res: 接口相应结果
        :return:
        '''
        result=""
        msg=""
        for validator_field in validator_list:
            check_field=validator_field["check"]
            expect_filed=validator_field["expect"]
            param_val=str(self.get_parms(check_field,res))
            if expect_filed[0]==">" and param_val>expect_filed[1:]:
                result = "pass"
                msg = "接口测试通过"
            elif expect_filed[0]=="<" and param_val<expect_filed[1:]:
                result = "pass"
                msg = "接口测试通过"
            elif expect_filed == param_val:
                result="pass"
                msg="接口测试通过"
            else:
                result="fail"
                msg="测试失败:【字段："+check_field+"预期结果是:"+expect_filed+",实际结果是:"+param_val+"】"
                break
        return result,msg


    def set_extract(self,extract_dict,res_counter):
        '''
        将提取值存放到对应的全局字典项中
        :param extract_dict: 提取字段字典
        :param res_counter: 接口返回的响应信息
        :return:
        '''
        for k,v in extract_dict.items():
            k_value=self.get_parms(k,res_counter)  #get_parms()函数，在返回内容counter中拿到提取变量对应的value值
            self.extract_global_dict[k]=k_value

    def get_parms(self,key,res):
        '''
        在内容中获取某一参数的值
        :param key: 参数
        :param res: 响应内容
        :return:
        '''
        if isinstance(res,str):
            try:
                res=json.loads(res)
            except:
                res=""
        if isinstance(res,dict):
            param_val=self.get_parms_requests(key,res)
        if param_val:
            return param_val
        else:
            return None


    def get_parms_requests(self,key,res):
        '''
        在内容中获取某一参数的值
        :param key: 要提取的参数
        :param requests: 响应值
        :return: 返回在响应值中提取到的key 对应的value值
        '''
        for k,v in res.items():
            if k==key:
                return v
            else:
                if isinstance(v,dict):
                    ret=self.get_parms_requests(key,v)
                    if ret is not None:
                        return ret
                if isinstance(v,list):
                    for i in v:
                        if isinstance(i,dict):
                            ret = self.get_parms_requests(key, i)
                            if ret is not None:
                                return ret




    def run_interface(self,url,method,header,body,data_type):
        '''
        发送请求接口
        :param url: 接口URL
        :param method: 请求方法
        :param header: 请求头
        :param body: 请求体
        :param data_type: 请求数据类型
        :return:
        '''
        if method=="get":
            res=requests.get(url=url,params=body,headers=header,verify=False)
        if method=="post":
            if data_type=="json":
                res=requests.post(url=url,json=body,headers=header,verify=False)
            if data_type=="data":
                res=requests.post(url=url,data=body,headers=header,verify=False)
        return res

    def get_env_by_envid(self,env_id):
        '''
        通过环境ID取环境URL及项目ID
        :param env_id: 环境ID
        :return:
        '''
        env_obj=Environment.objects.get(env_id=env_id)
        prj_id=env_obj.project.prj_id
        return env_obj.url,prj_id
if __name__ == '__main__':
    data={
        "a1":11,
        "a2":"$token"
    }
    print(Execute(11, 22).extract_variables(data))