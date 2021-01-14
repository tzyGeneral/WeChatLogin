# WeChatLogin
微信扫码登陆在Django上的实现

## 登录功能
集成了网页上微信扫码登录，账号密码注册、登录功能。
简单实现了JWT的签发，装饰器验证，通过refrashToken对令牌刷新功能。

微信扫码登录功能，对接微信api，获取登录二维码，扫码后登录。

## 微信第三方功能
集成了微信第三方的扫码授权登录功能
通过api获取到授权二维码链接，用户扫码后获取公众号素材内容
