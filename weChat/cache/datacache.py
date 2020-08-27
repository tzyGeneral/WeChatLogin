from django.core.cache import caches
from django.forms.models import model_to_dict


class DataCache:

    def __init__(self, model, cacheName='default', timeout=60 * 60 * 3):
        self.model = model
        self.cache = caches[cacheName]
        self.timeout = timeout

    def getValue(self, key, keyDbFieldName='key', valueDbFieldName='value'):
        # 强制定制key为字符串
        # key=str(key)
        result = self.cache.get(key)
        if not result:
            getDic = {keyDbFieldName: key}
            qs = self.model.objects.get(**getDic)
            result = model_to_dict(qs)[valueDbFieldName]
            # 修复数据库读取配置转字典bug
            self.cache.set(key, result, self.timeout)
        return result

    def getUser(self, key, keyDbFieldName='key'):
        result = self.cache.get(key)
        if not result:
            getDic = {keyDbFieldName: key}
            result = self.model.objects.filter(**getDic).first()
            self.cache.set(key, result, self.timeout)
        return result

    def setValue(self, key, value, keyDbFieldName='key', valueDbFieldName='value'):
        try:
            self.model.objects.filter(**{keyDbFieldName: key}).update(**{valueDbFieldName: value})
            result = self.cache.set(key, value, self.timeout)
        except Exception as reason:
            result = {'msg': str(reason)}
        return result

    def deleteKey(self, key):
        return self.cache.delete(str(key))

    def deleteKeysList(self, keysList):
        keysList = [str(x) for x in keysList]
        return self.cache.delete_many(keysList)
