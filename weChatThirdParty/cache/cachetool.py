from django.core.cache import caches
from weChatThirdParty.weChatRequest.weChatApi import WeChatApi

weChatApi = WeChatApi()


def setCache(cacheName: str = 'default'):
    cache = caches[cacheName]

    def _set(key, value, timeout):
        cache.set(key, value, timeout)
    return _set


def getCache(cacheName: str = 'default'):
    cache = caches[cacheName]

    def _get(key):
        result = cache.get(key)
        return result
    return _get


def deleteCache(cacheName: str = 'default'):
    cache = caches[cacheName]

    def _delete(key):
        cache.delete(key)
    return _delete


def get_pre_auth_code_cache():
    """
    从缓存中获取 pre_auth_code
    """
    preAuthCodeResult = getCache(cacheName='ticket_cache')(key="pre_auth_code")
    if not preAuthCodeResult:
        component_access_token = get_component_access_token_cache()
        preAuthCodeResult = weChatApi.get_pre_auth_code(component_access_token)
        expiresIn = preAuthCodeResult.get("expires_in", 60 * 8)
        setCache(cacheName='ticket_cache')(key="pre_auth_code", value=preAuthCodeResult, timeout=int(expiresIn))
    pre_auth_code = preAuthCodeResult.get("pre_auth_code")
    return pre_auth_code


def get_component_access_token_cache():
    """
    从缓存中获取 component_access_token
    """
    # 获取验证票据
    ticketData = getCache(cacheName='ticket_cache')(key="ticket")
    verify_ticket = ticketData.get("ComponentVerifyTicket")

    componentVerifyTicketData = getCache(cacheName='ticket_cache')(key="component_access_token")
    if not componentVerifyTicketData:
        componentVerifyTicketData = weChatApi.get_component_access_token(verify_ticket)
        expiresIn = componentVerifyTicketData.get("expires_in", 60 * 60 * 1)
        setCache(cacheName='ticket_cache')(key="component_access_token", value=componentVerifyTicketData,
                                           timeout=int(expiresIn))
    component_access_token = componentVerifyTicketData.get("component_access_token")
    return component_access_token

