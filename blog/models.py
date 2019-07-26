from django.db import models


class UserInfo(models.Model):
    username = models.CharField('姓名', max_length=15)
    password = models.CharField('密码', max_length=200)
    email = models.EmailField('邮箱')


class Event(models.Model):
    title_name = models.CharField(max_length=100)  # 发布会标题
    attend_num = models.IntegerField()  # 参加人数
    status = models.BooleanField()  # 状态
    address = models.CharField(max_length=200)  # 地址
    start_time = models.DateTimeField('events time')  # 发布会时间
    create_time = models.DateTimeField(auto_now=True)  # 创建时间（自动获取当前时间）

    def __str__(self):
        return self.title_name


class Guest(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)  # 关联发布会
    name = models.CharField(max_length=64)  # 姓名
    phone = models.CharField(max_length=16)  # 手机号
    email = models.EmailField()  # 邮箱
    sign = models.BooleanField()  # 签到状态
    create_time = models.DateTimeField(auto_now=True)  # 创建时间（自动获取当前时间）

    class Meta:
        unique_together = ("event", "phone")

    def __str__(self):
        return self.name

