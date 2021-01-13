import datetime
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from weChat.models import UserInfo
from weChat.tools.makeRefreshToken import getRefreshToekn


@api_view(['GET'])
def helloView(request):
    rsp = {"status": status.HTTP_200_OK, "msg": "ok"}
    try:
        rsp["data"] = "hello world"
    except Exception as e:
        rsp["msg"] = str(e)
    return Response(rsp)


@api_view(['GET', 'POST'])
def refreshTokenView(request):
    """通过Refresh Token 更改 AccessToken"""
    refresh_token = request.data.get("refresh_token", "")
    userObj = UserInfo.objects.filter(refresh_token=refresh_token).first()
    # 假如改用户存在
    if userObj.exists():
        # 判断是否过期
        if userObj.refresh_token_expire_date < datetime.datetime.now():
            # 可以刷新
            access_token = userObj.token(7)
            refresh_token = getRefreshToekn(userObj.user_id)
            expire_date = datetime.datetime.now() + datetime.timedelta(days=7)
            userObj.refresh_token = refresh_token
            userObj.refresh_token_expire_date = expire_date
            userObj.save()
            return Response({
                "status": 200,
                "access_token": access_token,
                "expires_in": 604800,  # token有效期为7天
                "refresh_token": refresh_token,
                "nickName": userObj.nickname
            })
    return Response({"status": status.HTTP_204_NO_CONTENT, "mas": "请重新登录"})

