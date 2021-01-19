from django.db import models
from django.contrib.auth.models import AbstractUser
class Taste(models.Model):
    '''任务模型类'''
    status_choice={
        (0,'STOP'),
        (1,'RUNNING'),
        (2, 'PAUSE'),
        (3,'RESUME')
    }
    taste_id=models.AutoField(primary_key=True,null=False,verbose_name='任务ID')
    status=models.SmallIntegerField(default=0,choices=status_choice,verbose_name='任务状态')
    taste_name=models.CharField(max_length=20,verbose_name='任务名称')
    taste_time=models.CharField(max_length=30,verbose_name='任务日期')
    description=models.CharField(max_length=50,verbose_name='任务描述')
    project=models.ForeignKey('project_env.Project',on_delete=models.CASCADE,verbose_name='项目名称')
    env=models.ForeignKey('project_env.Environment',on_delete=models.CASCADE,verbose_name='环境名称')
    # plan=models.ForeignKey('apitest.Plan',on_delete=models.CASCADE,verbose_name='计划名称')
    plans=models.TextField(verbose_name='测试计划')
    # user=models.ForeignKey('User',on_delete=models.CASCADE,verbose_name='负责人')

    def __str__(self):
        return self.taste_name
class User(AbstractUser,models.Model):
    '''用户模型类'''
    user_id=models.AutoField(primary_key=True,null=False,verbose_name='用户ID')
    account=models.CharField(max_length=20,verbose_name='账号')
    # user_name=models.CharField(max_length=20,verbose_name='用户名称')
    # passward=models.CharField(max_length=20,verbose_name='密码')
    phone=models.CharField(max_length=11,verbose_name='手机号',unique=True)
    email=models.EmailField(max_length=30,verbose_name='邮箱号')
    #projects=models.ForeignKey('project_env.Project',on_delete=models.CASCADE,verbose_name='项目名称')
    project=models.ForeignKey('project_env.Project',on_delete=models.CASCADE,verbose_name='项目名称')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建日期')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新日期')
    roles=models.ManyToManyField("Role")
    def __str__(self):
        return self.username

class Role(models.Model):
    name=models.CharField(max_length=32)
    permissions=models.ManyToManyField("Permission")

    def __str__(self):
        return self.name
class Permission(models.Model):
    name=models.CharField(max_length=32)
    url=models.CharField(max_length=45)

    def __str__(self):
        return self.name



