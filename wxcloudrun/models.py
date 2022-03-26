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
    countryid = models.IntegerField()

class Country(models.Model):
     # 一级区域 村、社区
    id = models.AutoField
    first = models.CharField(max_length = 50)
    # 二级 小区
    two = models.CharField(max_length = 50)
    # 三级
    three = models.CharField(max_length = 50)
    # 四级
    four = models.CharField(max_length = 100)

    class Meta:
         unique_together = (
             ('first', 'two'),
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
     userid = models.IntegerField()


     class Meta:
         unique_together = (
             ('idcard', 'addtime'),
         )