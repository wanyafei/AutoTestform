from django.conf import settings
from django.core.mail import send_mail
def send_email(to_email,env,task):
    subject = "自动化测试"
    message = ""
    html_message = "<h1>测试报告中含有错误或者失败的用例,点击连接查看详情:</h1><a href=%sapitest/query_report?task_id=%s /a>%sapitest/query_report?task_id=%s" % (
    env, task, env, task)
    sender = settings.EMAIL_FROM
    receiver = [to_email]
    send_mail(subject, message, sender, receiver, html_message=html_message)

