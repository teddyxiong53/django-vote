from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class BaseModel(models.Model):
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_delete = models.BooleanField(default=False, verbose_name='删除标记')

    class Meta:
        abstract = True # 说明是一个抽象模型类

class User(AbstractUser, BaseModel):
    class Meta:
        db_table = 'df_user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

class AddressManager(models.Manager):
    '''
    改变默认的行为，默认是得到all
    '''
    def get_default_address(self, user):
        try :
            address = self.model.objects.get(user=user, is_default=True)
        except self.model.DoesNotExsit:
            address = None

        return address

class Address(BaseModel):
    user = models.ForeignKey('User',on_delete=models.CASCADE, verbose_name='所属账号')
    receiver = models.CharField(max_length=20, verbose_name='收件人')
    addr = models.CharField(max_length=256, verbose_name='收件地址')
    zip_code = models.CharField(max_length=6, null=True, verbose_name='邮政编码')
    phone = models.CharField(max_length=11, verbose_name='手机号码')
    is_default = models.BooleanField(default=False, verbose_name='是否默认')

    # 使用自定义的模型管理
    objects = AddressManager()

    class Meta:
        db_table = 'df_address'
        verbose_name = '地址'
        verbose_name_plural = verbose_name

