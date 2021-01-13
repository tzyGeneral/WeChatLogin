from django.db import models

# Create your models here.


class WechatUserInfo(models.Model):
    """授权公众号信息"""
    SERVICE_TYPE_INFO = (
        (0, "订阅号"),
        (1, "由历史老帐号升级后的订阅号"),
        (2, "服务号")
    )
    VERIFY_TYPE_INFO = (
        (-1, "未认证"),
        (0, "微信认证"),
        (1, "新浪微博认证"),
        (2, "腾讯微博认证"),
        (3, "已资质认证通过但还未通过名称认证"),
        (4, "已资质认证通过、还未通过名称认证，但通过了新浪微博认证"),
        (5, "已资质认证通过、还未通过名称认证，但通过了腾讯微博认证")
    )

    uid = models.AutoField(verbose_name='用户id', db_column='id', primary_key=True)
    nick_name = models.CharField(verbose_name='昵称', db_column='nick_name', default='', max_length=100)
    authorizer_appid = models.CharField(verbose_name='授权方 appid', db_column='authorizer_appid', default='', max_length=100)
    # head_img = models.CharField(verbose_name='头像', db_column='head_img', default='', max_length=400)
    service_type_info = models.IntegerField(choices=SERVICE_TYPE_INFO, verbose_name='公众号类型', db_column='service_type_info', default=0)
    verify_type_info = models.IntegerField(choices=VERIFY_TYPE_INFO, verbose_name='公众号认证类型', db_column='verify_type_info', default=0)
    user_name = models.CharField(verbose_name='原始 ID', db_column='user_name', default='', max_length=100)
    principal_name = models.CharField(db_column='principal_name', verbose_name='主体名称', default='', max_length=100)
    alias = models.CharField(db_column='alias', verbose_name='公众号所设置的微信号', default='', max_length=50)
    qrcode_url = models.CharField(db_column='qrcode_url', verbose_name='二维码图片的 URL', default='', max_length=500)

    authorizer_access_token = models.CharField(db_column='authorizer_access_token', verbose_name='接口调用令牌', default='', max_length=300)
    authorizer_refresh_token = models.CharField(db_column='authorizer_refresh_token', verbose_name='刷新令牌', default='', max_length=300)
    create_time = models.DateTimeField(db_column='create_time', auto_now=True)


class WechatArticle(models.Model):
    """授权公众号内的文章"""
    id = models.AutoField(verbose_name='公众号id', db_column='id', primary_key=True)
    media_id = models.CharField(db_column='media_id', verbose_name='素材id', default='', max_length=200)
    title = models.CharField(db_column='title', verbose_name='标题', default='', max_length=300)
    author = models.CharField(db_column='author', verbose_name='作者', default='', max_length=100)
    content = models.TextField(db_column='content', verbose_name='文章内容', default='')
    url = models.CharField(db_column='url', verbose_name='图文页的URL', default='', max_length=500)
    create_time = models.DateTimeField(db_column='create_time', verbose_name='这篇图文消息素材的发布时间', auto_now=True)
    update_time = models.DateTimeField(db_column='update_time', verbose_name='这篇图文消息素材的最后更新时间', auto_now=True)
    is_check = models.BooleanField(db_column='is_check', verbose_name='是否检测', default=False)
    subName = models.ForeignKey(WechatUserInfo, on_delete=models.CASCADE, verbose_name='所属的公众号')