import string
import random
import jwt
from datetime import datetime, timedelta
from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator
from django.contrib.auth.hashers import make_password, check_password
from django.db.models.signals import pre_save

from weChat.tools import Snowflake

sf = Snowflake(1)


class UserInfo(models.Model):
    """用户模型"""
    user_id = models.CharField(verbose_name='用户id', max_length=50, unique=True)
    nickname = models.CharField(verbose_name='昵称', default='', max_length=30)
    phone = models.IntegerField(unique=True, validators=[
        RegexValidator(regex='^\d{11}$', message='手机号格式不对', code='手机号格式不对')], null=True)
    gender = models.IntegerField(verbose_name='性别', db_column='gender', null=True, blank=True)
    profileImageUrl = models.CharField(verbose_name='头像链接', db_column='profileImageUrl', max_length=200)
    city = models.CharField(verbose_name='城市', max_length=20, db_column='city', null=True, blank=True)
    email = models.EmailField(verbose_name='绑定邮箱', db_column='email', default='')

    refresh_token = models.CharField(verbose_name="刷新令牌", unique=True, db_column='user_refresh_token', max_length=255,
                                     null=True)
    refresh_token_expire_date = models.DateTimeField(verbose_name="refresh_token失效日期", null=True)

    @staticmethod
    def random_nickname():
        """生成随机的昵称"""
        ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 10))
        return ran_str

    def token(self, days=1):
        return self._generate_jwt_token(days)

    def _generate_jwt_token(self, days: int):
        token = jwt.encode({
            'exp': datetime.utcnow() + timedelta(days=days),
            'lat': datetime.utcnow(),
            'data': {
                'user_id': self.user_id
            }
        }, settings.SECRET_KEY, algorithm='HS256')
        return token.decode("utf-8")

    def __str__(self):
        return self.user_id


class LocalAuth(models.Model):
    """本地验证"""
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    username = models.CharField(verbose_name="账号", max_length=50, unique=True)
    password = models.CharField(verbose_name="密码", db_column="password", max_length=255)
    update_time = models.DateTimeField(auto_now=True, verbose_name="创建时间")

    @staticmethod
    def getVaildUser(username, password):
        """验证是否为有效用户"""
        try:
            auth = LocalAuth.objects.filter(username=username).first()
            if not auth: return None
            check_password(password, auth.password)
        except:
            return None
        return auth.user

    @staticmethod
    def getOrCreate(username, password):
        """获取或者创建账户"""
        try:
            password = make_password(password)
            user, is_create = LocalAuth.objects.get_or_create(username=username, password=password)
        except:
            return None, False
        return user, is_create

    @staticmethod
    def updatePassword(user, oldPassword, newPassword):
        """更新账户的密码"""
        try:
            local_auth = LocalAuth.objects.get(user=user)
            if check_password(oldPassword, local_auth.password):
                LocalAuth.objects.filter(user=user).update(password=make_password(newPassword))
            else:
                return "账号密码错误", False
        except Exception:
            return "用户不存在", False
        return '', True

    @staticmethod
    def resetPassword(user, newPassword):
        """重新设置密码"""
        try:
            LocalAuth.objects.filter(user=user).update(password=make_password(newPassword))
        except Exception:
            return "重新设置密码失败", False
        return "", True


class OtherAuth(models.Model):
    """三方登陆验证"""
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    oauth_id = models.CharField(verbose_name='唯一识别码', max_length=50, unique=True)
    oauth_name = models.CharField(verbose_name="第三方平台", db_column='oauth_name', max_length=100)
    refresh_token = models.CharField(verbose_name='refreshToken', db_column='refresh_token', max_length=150)
    oauth_expires = models.DateTimeField(null=True, blank=True, verbose_name="过期时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="创建时间")


def create_user_obj_handler(sender, instance, *args, **kwargs):
    """接受信号,用于创建用户信息的处理器"""
    try:
        _ = instance.user
    except Exception as e:
        if isinstance(instance, LocalAuth):
            prefix = 'th'
        elif isinstance(instance, OtherAuth):
            prefix = instance.oauth_name
        user_id = '{}_{}'.format(prefix, sf.generate())
        user = UserInfo.objects.create(user_id=user_id)
        instance.user = user


def user_profile_handler(sender, instance, *args, **kwargs):
    """生成随机昵称"""
    if not instance.nickname:
        instance.nickname = sender.random_nickname()


pre_save.connect(receiver=user_profile_handler, sender=UserInfo)  # 当UserInfo调用save方法时生成随机昵称
pre_save.connect(receiver=create_user_obj_handler, sender=LocalAuth)  # 本地登录，创建用户信息save方法时执行同步生成UserInfo
pre_save.connect(receiver=create_user_obj_handler, sender=OtherAuth)  # 第三方登录，创建用户信息save方法时执行同步生成UserInfo
