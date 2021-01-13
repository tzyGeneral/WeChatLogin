from rest_framework.response import Response
from rest_framework.decorators import APIView
from rest_framework import status
from weChatThirdParty.cache.cachetool import setCache,getCache


class HelloView(APIView):
    """测试视图"""

    def get(self, request, *args, **kwargs):
        rsp = {"status": status.HTTP_200_OK, "msg": "ok"}
        try:
            # setCache(cacheName='default')(key="1", value="2", timeout=10)
            a = getCache(cacheName='default')(key="1")
            print(a)
            rsp["data"] = "hello world"
        except Exception as e:
            rsp["msg"] = str(e)
        return Response(rsp)
