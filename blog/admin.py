# Register your models here.
from django.contrib import admin
from .models import UserInfo

admin.site.site_header = 'Blog管理后台'
admin.site.site_title = '我的 博客'


@admin.register(UserInfo)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'password', 'email')
