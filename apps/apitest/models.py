from django.db import models
class Interface(models.Model):
    '''接口类'''
    if_id=models.AutoField(primary_key=True, null=False,verbose_name='接口id')
    if_name=models.CharField(max_length=50,verbose_name='接口名称')
    if_url=models.CharField(max_length=50,verbose_name='接口地址')
    method=models.CharField(max_length=4,verbose_name='接口请求方法')
    data_type = models.CharField(max_length=4,verbose_name='接口请求头类型')
    project=models.ForeignKey('project_env.Project',on_delete=models.CASCADE,verbose_name='项目')
    description=models.CharField(max_length=50,verbose_name='接口描述')
    request_header_param=models.TextField(verbose_name='请求头')
    request_body_param = models.TextField(verbose_name='请求体')
    response_header_param = models.TextField(verbose_name='响应头')
    response_body_param = models.TextField(verbose_name='响应体')

    def __str__(self):
        return self.if_name
class Case(models.Model):
    '''测试用例类'''
    case_id=models.AutoField(primary_key=True, null=False,verbose_name='用例ID')
    case_name=models.CharField(max_length=50,verbose_name='用例名称')
    project=models.ForeignKey('project_env.Project',on_delete=models.CASCADE,verbose_name='项目')
    description=models.CharField(max_length=50,verbose_name='用例描述')
    content=models.TextField(verbose_name='用例内容')

    def __str__(self):
        return self.case_name
class Plan(models.Model):
    '''测试计划类'''
    plant_id=models.AutoField(primary_key=True, null=False,verbose_name='计划id')
    plant_name=models.CharField(max_length=50,verbose_name='计划名称')
    project=models.ForeignKey('project_env.Project',on_delete=models.CASCADE,verbose_name='项目')
    env=models.ForeignKey('project_env.Environment',on_delete=models.CASCADE,verbose_name='环境')
    description = models.CharField(max_length=50,verbose_name='计划描述')
    content=models.TextField(verbose_name='计划内容')

    def __str__(self):
        return self.plant_name
class Report(models.Model):
    '''测试报告类'''
    report_id=models.AutoField(primary_key=True, null=False,verbose_name='报告ID')
    report_name=models.CharField(max_length=50,verbose_name='报告名称')
    plant=models.ForeignKey('Plan',on_delete=models.CASCADE,verbose_name='报告对应的计划',null=True)
    content = models.TextField(verbose_name='报告内容')
    case_num=models.IntegerField(null=True,verbose_name='用例数量')
    pass_num = models.IntegerField(null=True,verbose_name='通过数量')
    fail_num = models.IntegerField(null=True,verbose_name='失败数量')
    error_num = models.IntegerField(null=True,verbose_name='错误数量')
    task=models.ForeignKey('taste_user.Taste',on_delete=models.CASCADE,verbose_name='报告对应的任务',null=True)

    def __str__(self):
        return self.report_name

