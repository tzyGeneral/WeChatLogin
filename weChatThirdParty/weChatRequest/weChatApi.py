import requests
import json
from weChatThirdParty.config.wechatCof import APPSECRET, APPID


class WeChatApi:

    @staticmethod
    def get_component_access_token(ticket: str):
        """
        获取微信令牌
        原文档：https://developers.weixin.qq.com/doc/oplatform/Third-party_Platforms/api/component_access_token.html
        """
        url = "https://api.weixin.qq.com/cgi-bin/component/api_component_token"
        data = {
            "component_appid": APPID,  # 第三方平台 appid
            "component_appsecret": APPSECRET,  # 第三方平台 appsecret
            "component_verify_ticket": ticket  # 微信后台推送的 ticket
        }
        response = requests.post(url, data=json.dumps(data))
        result = response.json()
        return result

    @staticmethod
    def get_pre_auth_code(component_access_token):
        """
        获取微信的预授权码
        原文档：https://developers.weixin.qq.com/doc/oplatform/Third-party_Platforms/api/pre_auth_code.html
        """
        url = f"https://api.weixin.qq.com/cgi-bin/component/api_create_preauthcode?component_access_token={component_access_token}"
        data = {
            "component_appid": APPID
        }
        response = requests.post(url, data=json.dumps(data))
        result = response.json()
        return result

    @staticmethod
    def get_auth_message(component_access_token, auth_code):
        """
        使用授权码获取授权信息
        原文档：https://developers.weixin.qq.com/doc/oplatform/Third-party_Platforms/api/authorization_info.html
        """
        url = f"https://api.weixin.qq.com/cgi-bin/component/api_query_auth?component_access_token={component_access_token}"
        data = {
            "component_appid": APPID,
            "authorization_code": auth_code  # 授权码, 会在授权成功时返回给第三方平台（扫码成功回调后回获取）
        }
        response = requests.post(url, data=json.dumps(data))
        result = response.json()
        return result

    @staticmethod
    def get_authorizer_info(component_access_token, authorizer_appid):
        """
        获取授权方的帐号基本信息
        原文档：https://developers.weixin.qq.com/doc/oplatform/Third-party_Platforms/api/api_get_authorizer_info.html
        """
        url = f"https://api.weixin.qq.com/cgi-bin/component/api_get_authorizer_info?component_access_token={component_access_token}"
        data = {
            "component_appid": APPID,
            "authorizer_appid": authorizer_appid
        }
        responseAuth = requests.post(url, data=json.dumps(data))
        result = responseAuth.json()
        return result

    @staticmethod
    def authorizer_token(component_access_token, authorizer_appid, authorizer_refresh_token):
        """
        刷新接口调用令牌、
        原文档：https://developers.weixin.qq.com/doc/oplatform/Third-party_Platforms/api/api_authorizer_token.html
        """
        url = f"https://api.weixin.qq.com/cgi-bin/component/api_authorizer_token?component_access_token={component_access_token}"
        data = {
            "component_appid": APPID,
            "authorizer_appid": authorizer_appid,
            "authorizer_refresh_token": authorizer_refresh_token
        }
        response = requests.post(url, data=json.dumps(data))
        result = response.json()
        return result