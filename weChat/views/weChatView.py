import time
import hashlib
import requests
from lxml import etree
from weChat.config.appKeys import APPID, APPSECRET
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from weChat.utils import weChatRequest
from weChat.cache.cachetool import OtherAuthUserLoginCache


@api_view(['GET'])
def weChatLoginQrcodeView(request):
    """获取二维码"""
    t = time.time()
    h = hashlib.md5()
    h.update(str(t).encode(encoding='utf-8'))
    state = h.hexdigest()
    # 扫描后给微信的重定向url地址（这个地址会携带code与status）
    redirectUrl = "127.0.0.1:8000/api/weChatLogin"
    url = f'https://open.weChat.qq.com/connect/qrconnect?appid={APPID}&redirect_uri={redirectUrl}&response_type=code' \
          f'&scope=snsapi_login&state={state}#wechat_redirect'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            html = etree.HTML(response.text)
            img = html.xpath('//div[@class="wrp_code"]/img[1]/@src')
            qrcode = "https://open.weChat.qq.com" + img[0]
        else:
            qrcode = ''
    except Exception as e:
        qrcode = ''
    return Response({"weChatQrcodeImg": qrcode})


@api_view(['GET'])
def weChatLgoinView(request):
    """微信登陆"""
    code = request.GET.get("code", '')  # 通过微信redirectUrl获取到的授权码
    if not code:
        rsp = {"status": status.HTTP_401_UNAUTHORIZED, "msg": "微信授权码缺失"}
        return Response(rsp)
    # 请求微信服务器，获取到openid和access_token
    result = weChatRequest(
        url=f"https://api.weixin.qq.com/sns/oauth2/access_token?appid={APPID}&secret="
            f"{APPSECRET}&code={code}&grant_type=authorization_code"
    )
    openid = result.get("openid", "")
    access_token = result.get("access_token", "")
    if not openid or not access_token:
        rsp = {"status": status.HTTP_401_UNAUTHORIZED, "msg": "请求微信服务器失败"}
        return Response(rsp)
    userInfo = OtherAuthUserLoginCache().getUserInfoFromCache(openid=openid, accessToken=access_token)
    access_token = userInfo.token(days=1)
    refresh_token = userInfo.token(days=7)



