from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status


@api_view(['GET'])
def helloView(request):
    rsp = {"status": status.HTTP_200_OK, "msg": "ok"}
    try:
        rsp["data"] = "hello world"
    except Exception as e:
        rsp["msg"] = str(e)
    return Response(rsp)


@api_view(['GET'])
def refreshTokenView(request):
    """通过Refresh Token 更改 AccessToken"""

