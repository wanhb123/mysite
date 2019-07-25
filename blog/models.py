from django.db import models


class UserInfo(models.Model):
    username = models.CharField('姓名', max_length=15)
    password = models.CharField('密码', max_length=200)
    email = models.EmailField('邮箱')


