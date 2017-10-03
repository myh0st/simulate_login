# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import cookielib
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.3397.16 Safari/537.36',
}

session = requests.session()
session.cookies = cookielib.LWPCookieJar('cookies.txt')
try:  # 尝试加载cookies
    session.cookies.load(ignore_discard=True)
except:
    print 'cookies failed to load!'
else:
    print 'cookies has been loading!'


def get_csrf_captcha_rand(url):  # 在页面中找到csrf_token和captcha_rand
    response = session.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    csrf_token = soup.select('input#csrf_token')[0]
    captcha_rand = soup.select('input#captchaRand')[0]
    match_cs = re.findall(r'.*?value="(.*)".*', str(csrf_token))[0]
    match_rand = re.findall(r'.*?value="(.*?)".*', str(captcha_rand))[0]
    return match_cs, match_rand


def get_captcha(rand): # 保存captcha.png图片
    import time
    time = str(int(time.time() * 1000))
    captcha_url = 'https://account.guokr.com/captcha/{}/?v={}'.format(rand, time)
    response = session.get(captcha_url, headers=headers)
    with open('captcha.png', 'wb') as f:
        f.write(response.content)
        f.close()
    from PIL import Image
    try:
        captcha_image = Image.open('captcha.png')
        captcha_image.show()
        captcha_image.close()
    except:
        print 'captcha.png not found!'
    code = raw_input('please check the captcha code and enter it:')
    return code


def guokr_login(account, password):  # 正式登录
    url = 'https://account.guokr.com/sign_in/'
    csrf_captcha_rand = get_csrf_captcha_rand(url)
    post_data = {
        'csrf_token': csrf_captcha_rand[0],
        'username': account,
        'password': password,
        'captcha': get_captcha(csrf_captcha_rand[1]),
        'captcha_rand': csrf_captcha_rand[1],
        'permanent': 'y'
    }
    response = session.post(url, data=post_data, headers=headers)
    session.cookies.save()  # 保存cookies


def is_login():  # 判断是否为登录状态   http://www.guokr.com/i/0890827117/ allow_redirects=False
    personal_url = 'http://www.guokr.com/user/feeds/'
    response = session.get(personal_url, headers=headers)
    if response.status_code != 200:
        return False
    else:
        return True


# guokr_login('账号', '密码')
is_login()
