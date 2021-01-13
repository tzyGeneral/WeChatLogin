from weChat.cache.datacache import DataCache
from django.core.cache import caches
from weChat.models import *
from utils import weChatRequest


class OtherAuthUserLoginCache(DataCache):
    """三方用户登陆信息缓存"""
    def __init__(self, model=OtherAuth, cacheName='OtherAuth', timeout=60*60):
        super().__init__(model, cacheName, timeout)
        self.model = model
        self.cache = caches[cacheName]
        self.timeout = timeout

    def getUserInfoData(self, openid, accessToken):
        """从数据库中查询用户信息"""
        auth, is_created = OtherAuth.objects.get_or_create(oauth_id=openid, oauth_name="weiChat")
        if is_created:
            try:
                userInfoData = weChatRequest(
                    url=f'https://api.weixin.qq.com/sns/userinfo?access_token={accessToken}&openid={openid}&lang=zh_CN'
                )
                if userInfoData:
                    auth.user.nickname = userInfoData.get("nickname", "")
                    auth.user.city = userInfoData.get("city", "")
                    auth.user.gender = userInfoData.get("sex", "")
                    auth.user.profileImageUrl = userInfoData.get("headimgurl", "")
                    auth.user.save()
            except Exception:
                return auth.user
        return auth.user

    def getUserInfoFromCache(self, openid, accessToken, useCache=False):
        """从缓存中查询用户信息"""
        if not useCache:
            result = self.getUserInfoData(openid, accessToken)
        else:
            result = self.cache.get(key=openid)
            if not result:
                result = self.getUserInfoData(openid, accessToken)
                self.cache.set(openid, result, self.timeout)
        return result


class UserInfoCache(DataCache):
    """用户对象缓存"""
    def __init__(self, model=UserInfo, cacheName='userInfo', timeout=60*60*24):
        super().__init__(model, cacheName, timeout)
        self.model = model
        self.cache = caches[cacheName]
        self.timeout = timeout

    def getUserObj(self, userId: str):
        userObj = self.cache.get(str(userId))
        if not userObj:
            userObj = self.model.objects.filter(user_id=userId).first()
            self.cache.set(str(userId), userObj, self.timeout)
        return userObj
