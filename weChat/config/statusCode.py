
SUCCESS = 0

# 客户端错误类型
NOT_AUTHENTICATE = 40000  # 不存在authenticate头

TOKEN_INVALID = 40001  # Token无效，过期等

PARAMS_MISS = 40002  # 缺失参数
PARAMS_ERR = 40003  # 参数有误
LOGIN_ERR = 40004  # 不支持登录类型

SIGN_ERR = 40005  # 签名错误

# 服务器错误类型
SERVER_ERR = 50001  # 服务器错误
