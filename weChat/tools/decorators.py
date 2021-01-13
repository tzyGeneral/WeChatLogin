import jwt
from functools import wraps
from django.conf import settings
from django.http import JsonResponse
from weChat.cache.cachetool import UserInfoCache
from weChat.config import SIGN_ERR, NOT_AUTHENTICATE


def my_login_required(view_func):
    """自定义登陆验证，验证token是否过期"""

    def _wrapped_view(request, *args, **kwargs):
        try:
            auth = request.META.get('HTTP_AUTHORIZATION').split()
        except AttributeError:
            # request.user = UserModel.objects.get(user_id='4')
            return JsonResponse({"code": NOT_AUTHENTICATE, "message": "不存在authenticate头"})
        else:
            token = auth[0]
            try:
                dic = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                user_id = dic.get("user_id")
                user = UserInfoCache().getUserObj(user_id)
                if not user:
                    raise ValueError("用户不存在")
                request.user = user
            except jwt.ExpiredSignatureError:
                return JsonResponse({"status_code": SIGN_ERR, "message": "Token 过期"})
            except jwt.InvalidTokenError:
                return JsonResponse({"status_code": SIGN_ERR, "message": "无效 token"})
            except Exception as e:
                return JsonResponse({"status_code": SIGN_ERR, "message": "用户不存在"})

        return view_func(request, *args, **kwargs)

    return wraps(view_func)(_wrapped_view)
