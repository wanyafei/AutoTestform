from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
from email.header import Header
import smtplib
class sendEmail():
    def __init__(self,receiver):
        '''初始化封装邮件对象'''
        self.from_user="18201037154@163.com"
        self.from_password="HMCTBAUGRXFSEKDP"
        self.smtp_server="smtp.163.com"
        self.mail_port=25
        self.receiver=receiver
        self.mime=MIMEMultipart()   #实例化邮件对象
    def sendEmailFun(self,env,task):
        '''发送邮件'''
        text_info="<h1>测试报告中含有错误或者失败的用例,点击连接查看详情:</h1><a href=%sapitest/query_report?task_id=%s /a>%sapitest/query_report?task_id=%s"%(env,task,env,task)
        self.mime.attach(MIMEText(text_info,"plain","utf-8")) #构建邮件正文
        self.mime['From'] = formataddr(('自动化测试', self.from_user))  # 邮件的发件人
        self.mime['To'] = Header("Tester", 'utf-8')  # 邮件的收件人
        self.mime['Subject'] = Header('自动化测试报告', 'utf-8').encode()  # 邮件的主题
        #链接服务器、登陆、发送邮件
        server=smtplib.SMTP(self.smtp_server,self.mail_port)   #构造链接邮件对象
        server.login(self.from_user,self.from_password)     #登录邮箱
        server.sendmail(self.from_user,self.receiver,self.mime.as_string())  #发送邮件
        server.quit()   #退出，释放资源
        print(u"邮件发送成功")

