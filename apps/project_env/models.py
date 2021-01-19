from django.db import models
class Project(models.Model):
    '''项目模型类'''
    status_choice={
        (0, '失效'),
        (1, '有效')
    }
    prj_id=models.AutoField(primary_key=True,null=False,verbose_name='项目id')
    prj_name=models.CharField(max_length=50,verbose_name='项目名称')
    version=models.CharField(max_length=20,verbose_name='项目版本')
    description=models.CharField(max_length=100,verbose_name='项目描述')
    status=models.SmallIntegerField(default=1,choices=status_choice,verbose_name='项目状态')

    def __str__(self):
        return self.prj_name
class Environment(models.Model):
    '''环境模型类'''
    status_choice={
        (0, '失效'),
        (1, '有效')
    }
    env_id=models.AutoField(primary_key=True,null=False,verbose_name='环境id')
    env_name=models.CharField(max_length=50,verbose_name='环境名字')
    url=models.CharField(max_length=100,verbose_name='环境url')
    description=models.CharField(max_length=100,verbose_name='环境描述')
    status=models.SmallIntegerField(default=1,choices=status_choice,verbose_name='环境状态')
    project=models.ForeignKey('Project',on_delete=models.CASCADE,verbose_name='项目名称')

    def __str__(self):
        return self.env_name
