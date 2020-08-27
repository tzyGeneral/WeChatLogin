from django.urls import path
from weChat.views import weChatView
from weChat.views import baseView
from weChat.views import webView


urlpatterns = [
    path('/hello/', baseView.helloView),
    # 获取登陆使用的二维码
    path('/weChatLoginImg/', weChatView.weChatLoginQrcodeView),
    # 微信扫码登陆
    path('/weChatLogin/', weChatView.weChatLgoinView),

    # 普通账号密码登陆，注册
    path('/webLogin/', webView.loginView),
    path('/webRegister/', webView.registerView),

    # 刷新accessToken
    path('/refresh_token', )

]