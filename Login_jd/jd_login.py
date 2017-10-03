# -*- coding:utf-8 -*-
import time
from selenium import webdriver
import requests
import pickle

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.3397.16 Safari/537.36',
}


def jd_login(username, password):
    driver = webdriver.Chrome(executable_path="C:\Users\Stone\PycharmProjects\Virtualenv\scrapy_1\chromedriver.exe")
    driver.get('https://passport.jd.com/new/login.aspx')  # JD 登录页面
    time.sleep(2)  # 等待加载
    driver.find_element_by_css_selector('div.login-tab-r a').click()
    driver.find_element_by_css_selector('input#loginname').send_keys(username)
    driver.find_element_by_css_selector('input#nloginpwd').send_keys(password)
    driver.find_element_by_css_selector('a#loginsubmit').click()
    driver.delete_all_cookies()
    jd_cookies = driver.get_cookies()
    driver.close()  # 关闭浏览器
    pickle.dump(jd_cookies, open('cookies.pkl', 'wb'))  # 保存cookies
    print 'cookies save successfully!'


def is_login():
    try:
        cookies = pickle.load(open('cookies.pkl', 'rb'))  # 加载cookies，传给requests
        print 'cookies loaded successfully '
    except:
        print 'cookies failed to load!'
    session = requests.session()
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])
    response = session.get('http://helper.jd.com/IDPlus/pchtml/size-center.html', headers=headers,
                           allow_redirects=False)
    # http://helper.jd.com/IDPlus/pchtml/size-center.html   https://order.jd.com/center/list.action
    print response.text


jd_login('账号', '密码')
is_login()



'''
未完成的post_data分析，密码加密规则待分析。

eid:7BSPIMJQWNWXNNOZJVN5VQSL44XLYRU4VC4TRAZI2KOWWG3TGNXOYWD5SWTDYW63Y7UKNKOYBT3FSC63F2XJJPA7LY
fp:a1a3b8c1d79127ad71a8b99cde8eb0df
nloginpwd:H/UEhSWakN8Dztg6Bp8PXmKfXRMLDtjXTQL7A8xdUPgW9WkEXMFF7bnaja3yvZ29QxA8aEFfUBp77q9M1FJ9A+pI42QlsMKXhTm+8WN7K1bx+taia9EgcvBoq5ZxJQMqlrtr1Rx5KLjS0gEBip4Gjqmt18HkG8LVqIHnLQD37gg=



以下post_data字段在返回的html中可以直接查找

authcode:
chkRememberMe:
seqSid:646597764442868235    先访问一个js获取改值
_t:_ntqPUHA
loginType:c
loginname:1342417668@qq.com
pubKey:MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDC7kw8r6tq43pwApYvkJ5laljaN9BZb21TAIfT/vexbobzH7Q8SUdP5uDPXEBKzOjx2L28y7Xs1d9v3tdPfKI2LR7PAzWBmDMn8riHrDDNpUpJnlAGUqJG9ooPn8j7YNpcxCa1iybOlc2kEhmJn5uwoanQq+CA6agNkqly2H4j6wIDAQAB
sa_token:B68C442BE645754F33277E701208059080DD726A94A73F76DEC3053A838549C06EB7D3797CE1C5BBE7C2B2EF9CA7D467C4B841002F8A2DEA0DD3ACC5BA959244A539E8B9D2CB176B62FE436B89B8310978A5D9B99A4545B16012582BCDF61F8FC7A8AE9D3A8CC2F220C2541A6395F39025E34AF37F7AC4996E097D59805880B3433423EAC0F6B09DF302DF2D79502CDAA1528E521CF020D4343C933BA246CA2B0A70B561B821FF7A6E9561D0DA9F98E98E4F59F5EEC80806FD0C04F86E88DA2E9328531A1DDB5BC6F6CC99DBD5CA6C50043E98D08F416D7BEC3AEF636CAE8E9D6B784FCE07E8016D208260312D41C9F9AA35766EDF2D20954498A734A7FC72BFD0D28C3C99A68B959851806D27FAC788B919FF6A6E38C5488E84F59BFB99CA0AD7B79A588D5DD1576F7DAF91EE6E0F8472CF654A14021698EA307E69F1F6611B0AFA32824AD07DB223E72626F770EF5DAA10C02E4B1FF060D5EB796873B9013B3E8EB819A42B75A3AA1D21C2CFF5C5D7F98D101ED78891BFC3AA5C37503529158D15F44DAD1E93980293245D0C103A0AC586379B45B53CA91E4DDA1CD2EF2C7EE9E6505E4A8A62027D6ED61EF834368E
uuid:40dcc154-50ad-41c2-a0d3-f36752e64fbe


以下判断是否需要验证码，返回False则不用，返回True则要访问验证url对图片进行处理

https://authcode.jd.com/verify/image?a=1&acid=1d4e504b-fe9e-4b3c-993e-ff6fb1ba0b1d&uid=1d4e504b-fe9e-4b3c-993e-ff6fb1ba0b1d&yys=1504072237292   验证码
https://passport.jd.com/uc/showAuthCode?r=0.9892351007150157&version=2015 判断返回是否需要验证码
'''
