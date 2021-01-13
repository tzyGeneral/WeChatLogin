from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from weChat.models import LocalAuth
from weChat.tools.makeRefreshToken import getRefreshToekn
from weChat.form import RegisterForm
import datetime


@api_view(['GET', 'POST'])
def loginView(request):
    """用户登陆，签发 RefreshToken 和 AccessToken """
    username = request.data.get("username", "")
    password = request.data.get("password", "")
    user = LocalAuth.getVaildUser(username, password)
    if not user:
        return Response({"status": status.HTTP_401_UNAUTHORIZED, "msg": "账号密码错误"})
    refresh_token = getRefreshToekn(user.user_id)
    access_token = user.token(days=7)
    user.refresh_token = refresh_token
    user.refresh_token_expire_date = datetime.datetime.now() + datetime.timedelta(days=7)
    user.save()
    return Response({
        "status": 200,
        "access_token": access_token,
        "expires_in": 604800,  # token有效期为7天
        "refresh_token": refresh_token,
        "nickName": user.nickname
    })


@api_view(['POST'])
def registerView(request):
    """用户注册"""
    register_form = RegisterForm(request.data)
    if register_form.is_valid():
        username: str = register_form.cleaned_data.get('username', '')
        password: str = register_form.cleaned_data.get('password', '')
        confirmPassword: str = register_form.cleaned_data.get('confirmPassword', '')
        if password != confirmPassword:
            return Response({"status": status.HTTP_401_UNAUTHORIZED, "mag": "两次输入密码不一致"})
        user, is_create = LocalAuth.getOrCreate(username=username, password=password)
        if not is_create:
            return Response({"status": status.HTTP_401_UNAUTHORIZED, "msg": "用户已经存在"})
        elif not user:
            return Response({"status": status.HTTP_401_UNAUTHORIZED, "msg": "注册失败"})
        else:
            return Response({"status": status.HTTP_200_OK, "msg": "注册成功"})
    else:
        return Response({"status": status.HTTP_401_UNAUTHORIZED, "msg": "输入的账号密码格式有误"})

