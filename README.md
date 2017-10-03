#### 用 python 进行模拟登录

1、果壳登录

- 使用 requests、BeautifulSoup、cookielib 库
- 密码没有经过加密、获取验证码图片即可完成模拟登录

2、拉勾登录

- 使用 requests、BeautifulSoup、cookielib 库
- 密码字段经过 md5 加密、获取验证码图片

3、京东登录、淘宝登录

- 密码等几个字段加密复杂，暂时没能用 requests 库完成模拟登录
- 使用 selenium 进行模拟登录，模拟浏览器进行自动化测试

