from utils import getUTCtimesmap, getMd5EncodeData


def getRefreshToekn(user_id: int) -> str:
    """生成刷新token"""
    string = str(user_id) + getUTCtimesmap()
    return getMd5EncodeData(string)

