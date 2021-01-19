from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy
from taste_user.models import User,Role,Permission

#用户表admin配置
class userconfig(UserAdmin):
    #设置显示的字段
    list_display = ['user_id','username','account','project','phone','email','password']
    # 列表界面可编辑
    list_editable = ['username','phone','email','project','password']
        # 按id降序排列
    ordering = ['-user_id']
    # 搜索功能
    search_fields = ['username']
    # 增加用户时密码为密文
    add_fieldsets = (
        (None, {u'fields': ('username', 'password1', 'password2')}),
        # 增加页面显示字段设置
        (gettext_lazy('User Information'), {'fields': ('project', 'email', 'phone', 'account','roles')}),)

admin.site.site_header = '用户配置'
admin.site.site_title = '后台用户配置'

admin.site.register(User,userconfig)
#角色表admin配置
class roleconfig(admin.ModelAdmin):
    list_display = ['name']
admin.site.register(Role,roleconfig)

#权限表admin配置
class permission(admin.ModelAdmin):
    list_display = ['name','url']
    ordering = ['-pk']
admin.site.register(Permission,permission)




