from datetime import datetime

from django.db import models


# Create your models here.
class Counters(models.Model):
    id = models.AutoField
    count = models.IntegerField(max_length=11, default=0)
    createdAt = models.DateTimeField(default=datetime.now(), )
    updatedAt = models.DateTimeField(default=datetime.now(),)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'Counters'  # 数据库表名

class User(models.Model):
    # 用户名不能重复
    id = models.AutoField
    name = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50)
# 1 超级管理员， 2 普通管理员  3 普通人员
    role = models.IntegerField()
    # 区域
    # countryid = models.IntegerField()
    # 哪个社区 哪个村的
    area = models.CharField(max_length = 50)

class Country(models.Model):
     # 一级区域 村、社区
    id = models.AutoField
    first = models.CharField(max_length = 50)
    # 二级 小区
    two = models.CharField(max_length = 50)
    # 三级
    three = models.CharField(max_length = 50)

    class Meta:
         unique_together = (
             ('first', 'two', 'three'),
         )

class History(models.Model):
     name = models.CharField(max_length=50)
     sex = models.CharField(max_length=5)
     age = models.SmallIntegerField()
     birth = models.DateField()
     idcard = models.CharField(max_length=50)
     iphone = models.CharField(max_length=20)
     addtime = models.DateField()
     times = models.SmallIntegerField()
     # 一级地址
     area = models.CharField(max_length = 200)

     # 二级地址
     two = models.CharField(max_length= 200)

     # 管理员的id
     userid = models.IntegerField()

     class Meta:
         indexes = [
             models.Index(fields=['times'])
         ]
         unique_together = (
             ('idcard', 'addtime'),
         )

class Alluser(models.Model):
    idcard = models.CharField(max_length=50)
    first = models.CharField(max_length=50)
    two = models.CharField(max_length=50)
    class Meta:
        unique_together = (
            ('idcard')
        )
