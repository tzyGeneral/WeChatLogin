from django.urls import path
from weChatThirdParty.views import baseMod, wechatMod


urlpatterns = [
    path('hello', baseMod.HelloView.as_view()),
    # 接收微信验证票据（component_verify_ticket）
    path('notify', wechatMod.VerifyTicketView.as_view()),
    # 获取auth_code的回调url（自己在微信后台配置）
    path('authCallback', wechatMod.WeChatCallBackView.as_view()),
    # 获取授权的二维码
    path('qrcode', wechatMod.QrcodeView.as_view())
]