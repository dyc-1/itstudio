from django.db import models
import random, time, os
from itstudio.settings import MEDIA_ROOTS

# Create your models here.


def upload_to(self, instance):
    all_char = '0123456789qazwsxedcrfvtgbyhnujmikolpQAZWSXEDCRFVTGBYHNUJIKOLPHRZIT'
    sid = str(time.time())[:10]
    for i in range(6):
        num = random.randint(0, 64)
        sid += all_char[num]
    image = '/Image_' + sid
    return '/'.join([instance])


class Register(models.Model):

    name = models.CharField(max_length=30, verbose_name='学生姓名')

    email = models.EmailField(verbose_name='电子邮箱')

    phone = models.CharField(max_length=30, verbose_name='手机号码')

    major = models.CharField(max_length=30, verbose_name='年级专业')

    departer = models.CharField(max_length=30, verbose_name='选择部门')

    status = models.IntegerField(verbose_name='目前阶段')

    enable = models.BooleanField(verbose_name='激活状态')

    sid = models.CharField(max_length=30, verbose_name='sid码')

    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def state(self):
        if self.status == 0:
            return '初审未开始'
        elif self.status == 1:
            return '初审通过'
        elif self.status == 2:
            return '初审未通过'
        elif self.status == 3:
            return '面试通过'
        elif self.status == 4:
            return '面试未通过'
        elif self.status == 5:
            return '笔试通过'
        elif self.status == 6:
            return '笔试未通过'
        elif self.status == 7:
            return '录取通过'
        elif self.status == 8:
            return '录取未通过'
        else:
            return '状态错误'

    def __str__(self):
        return str(self.email)

    class Meta:
        verbose_name = '注册信息管理'
        verbose_name_plural = verbose_name


class Work(models.Model):

    title = models.CharField(max_length=30, verbose_name='作品标题')

    img = models.ImageField(upload_to=upload_to, verbose_name='作品封面', default="default.jpg")

    year = models.CharField(max_length=30, blank=True, verbose_name='作品年份')

    url = models.TextField(verbose_name='作品链接')

    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = '作品展示管理'
        verbose_name_plural = verbose_name


class Department(models.Model):

    name = models.CharField(max_length=30, verbose_name='部门名称')

    introduce = models.TextField(verbose_name='部门介绍')

    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = '部门展示管理'
        verbose_name_plural = verbose_name


class Member(models.Model):

    name = models.CharField(max_length=30, verbose_name='成员名称')

    img = models.ImageField(upload_to=upload_to, verbose_name='成员图片', default="default.jpg")

    grade = models.CharField(max_length=30, verbose_name='成员年级')

    department = models.CharField(max_length=30, verbose_name='所属部门')

    quotes = models.TextField(verbose_name='成员名言')

    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = '成员展示管理'
        verbose_name_plural = verbose_name


class History(models.Model):

    title = models.CharField(max_length=30, verbose_name='历史名称')

    year = models.CharField(max_length=30, verbose_name='历史年份')

    detail = models.TextField(verbose_name='历史内容')

    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = '历史展示管理'
        verbose_name_plural = verbose_name


class Comment(models.Model):

    content = models.TextField(verbose_name='评论内容')

    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return str(self.content)

    class Meta:
        verbose_name = '用户评论管理'
        verbose_name_plural = verbose_name












