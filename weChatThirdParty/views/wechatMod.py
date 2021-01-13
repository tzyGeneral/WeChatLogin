from rest_framework.response import Response
from rest_framework.decorators import APIView
from rest_framework_xml.parsers import XMLParser
from rest_framework import status
from weChatThirdParty.commont.WXBizMsgCrypt import WXBizMsgCrypt
from weChatThirdParty.config.wechatCof import TOKEN, encodingAESKey, APPID
from weChatThirdParty.cache.cachetool import setCache, getCache, deleteCache, get_pre_auth_code_cache, get_component_access_token_cache
from weChatThirdParty.weChatRequest.weChatApi import WeChatApi
from weChatThirdParty.models import WechatUserInfo
import xmltodict
import json
import time
import datetime


class TextXMLParser(XMLParser):
    media_type = 'text/xml'


class VerifyTicketView(APIView):
    parser_classes = (TextXMLParser, )
    """接收验证票据（component_verify_ticket）"""
    def post(self, request, *args, **kwargs):
        signature = request.GET.get("signature")
        timestamp = request.GET.get("timestamp")
        nonce = request.GET.get("nonce")
        msg_signature = request.GET.get("msg_signature")

        encryptData = request.data
        # 字典转化为xml字符串
        encryptDataXml = xmltodict.unparse(encryptData)
        decrypt_test = WXBizMsgCrypt(TOKEN, encodingAESKey, APPID)
        ret, decrypt_xml = decrypt_test.DecryptMsg(encryptDataXml, msg_signature, timestamp, nonce)

        # 将xml字符串转化为字典dict
        decrypt_xml = xmltodict.parse(decrypt_xml)
        decrypt_xml = json.loads(json.dumps(decrypt_xml))
        # 将数据存入缓存中
        setCache(cacheName="ticket_cache")(key="ticket", value=decrypt_xml, timeout=60*60*3)

        return Response("success")


class QrcodeView(APIView):

    def get(self, request, *args, **kwargs):
        rsp = {"status": status.HTTP_200_OK, "msg": "ok"}
        qrType = request.GET.get("qrType", "")
        try:
            pre_auth_code = get_pre_auth_code_cache()
            # 这里是微信配置的回调链接
            redirectUri = f"http://www.xxx.com/wechat/authCallback"
            if qrType == "phone":
                url = f"https://mp.weixin.qq.com/safe/bindcomponent?action=bindcomponent&no_scan=1&component_appid={APPID}&" \
                      f"pre_auth_code={pre_auth_code}&redirect_uri={redirectUri}&auth_type=3#wechat_redirect"
            else:
                url = f"https://mp.weixin.qq.com/cgi-bin/componentloginpage?component_appid={APPID}&pre_auth_code={pre_auth_code}" \
                      f"&redirect_uri={redirectUri}"
            # 授权码使用完后进行清除
            deleteCache(cacheName='ticket_cache')(key="pre_auth_code")
            rsp["data"] = url
        except Exception as e:
            rsp["status"] = status.HTTP_500_INTERNAL_SERVER_ERROR
            rsp["msg"] = str(e)
        return Response(rsp)


class WeChatCallBackView(APIView):
    """用户扫码后回调进行的页面"""

    def get(self, request, *args, **kwargs):
        rsp = {"status": status.HTTP_200_OK, "msg": "ok"}
        try:
            auth_code = request.GET.get("auth_code")
            expires_in = request.GET.get("expires_in")

            # 请求微信api工具类的初始化
            weChatApi = WeChatApi()

            component_access_token = get_component_access_token_cache()

            # 获取授权信息
            authorizer_info = weChatApi.get_auth_message(component_access_token, auth_code)
            # 将授权方信息存入缓存
            authorizer_appid = authorizer_info["authorization_info"]["authorizer_appid"]  # 授权方 appid
            appidKey = authorizer_appid.replace(" ", '')  # 防止存入缓存时有空格存储失败
            timeout = authorizer_info["authorization_info"]["expires_in"]
            cacheData = {
                "authorizer_access_token": authorizer_info["authorization_info"]["authorizer_access_token"],
                "expires_in": authorizer_info["authorization_info"]["expires_in"],
                "authorizer_refresh_token": authorizer_info["authorization_info"]["authorizer_refresh_token"],
                "time_now": int(time.time())
            }
            setCache(cacheName='ticket_cache')(key=appidKey, value=cacheData, timeout=int(timeout))

            try:
                # 获取授权公众号的基本信息
                resultAuth = weChatApi.get_authorizer_info(component_access_token, authorizer_appid)
                # 存储到数据库中
                userDic = {
                    "nick_name": resultAuth["authorizer_info"]["nick_name"],
                    "authorizer_appid": authorizer_appid,
                    # "head_img": resultAuth["authorizer_info"]["head_img"],
                    "service_type_info": resultAuth["authorizer_info"]["service_type_info"].get("id", 0),
                    "verify_type_info": resultAuth["authorizer_info"]["verify_type_info"].get("id", 0),
                    "user_name": resultAuth["authorizer_info"]["user_name"],
                    "principal_name": resultAuth["authorizer_info"]["principal_name"],
                    "alias": resultAuth["authorizer_info"]["alias"],
                    "qrcode_url": resultAuth["authorizer_info"]["qrcode_url"],

                    "authorizer_access_token": authorizer_info["authorization_info"]["authorizer_access_token"],
                    "authorizer_refresh_token": authorizer_info["authorization_info"]["authorizer_refresh_token"],
                    "create_time": datetime.datetime.now()
                }
                authAppid = WechatUserInfo.objects.filter(authorizer_appid=authorizer_appid)
                if authAppid.exists():
                    authAppid.update(**userDic)
                else:
                    WechatUserInfo.objects.create(**userDic)

            except Exception as e:
                rsp["status"] = status.HTTP_401_UNAUTHORIZED
                rsp["msg"] = str(e)

            context = {
                "appid": authorizer_appid
            }
            # 这里假如是网页项目则可以返回web页面地址，或者自己的页面
            # return render(request, 'callback.html', context)
            rsp["data"] = context

        except Exception as e:
            rsp["status"] = status.HTTP_500_INTERNAL_SERVER_ERROR
            rsp["msg"] = str(e)
        return Response(rsp)