from django.shortcuts import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from taste_user.models import Role
import re
#权限的中间件
class permissionMiddleware(MiddlewareMixin):
    def process_request(self,request):
        current_path=request.path
        #设置白名单放行
        for reg in ["/admin/*","/login/","/loginout/"]:
            ret=re.search(reg,current_path)
            if ret:
                return None
        #校验是否登陆
        #权限验证
        user=request.user
        permissions=Role.objects.filter(user=user).values("permissions__url")
        permission_list=[]
        for item in permissions:
            permission_list.append(item["permissions__url"])

        for reg in permission_list:
            reg="^%s$"%reg
            ret=re.search(reg,current_path)
            if ret:
                return None
        return HttpResponse("没有访问权限。。。。。")
