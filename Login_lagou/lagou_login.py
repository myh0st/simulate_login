# -*- coding:utf-8 -*-
import hashlib
import requests
import cookielib
import re
import copy
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.3397.16 Safari/537.36',
    # 'X-Anit-Forge-Code': '',
    # 'X-Anit-Forge-Token': '',
    # 'X-Requested-With': 'XMLHttpRequest'
}

session = requests.session()
session.cookies = cookielib.LWPCookieJar('cookies.txt')
try:
    session.cookies.load(ignore_discard=True)
except:
    print 'cookies failed to load!'
else:
    print 'cookies has been loading!'


def encrypt_password(password):
    stable_word = 'veenike'
    first_encrypt = hashlib.md5(password).hexdigest()
    rude = stable_word + first_encrypt + stable_word
    second_encrypt = hashlib.md5(rude).hexdigest()
    print second_encrypt
    return second_encrypt


def get_captcha():
    url = 'https://passport.lagou.com/vcode/create?from=register&refresh={}'.format(str(int(time.time() * 1000)))
    response = session.get(url, headers=headers)
    with open('captcha.jpg', 'wb') as f:
        f.write(response.content)
        f.close()
    from PIL import Image
    try:
        captcha_image = Image.open('captcha.jpg')
        captcha_image.show()
        captcha_image.close()
    except:
        print 'captcha.jpg not found!'
    code = raw_input('please check the captcha code and enter it:')
    return code


def get_anti_Code_Token():
    url = 'https://passport.lagou.com/login/login.html'
    response = session.get(url, headers=headers)
    match_obj = re.match(r".*?Forge_Token = '(.*?)'.*Forge_Code = '(.*?)'.*", response.text, re.DOTALL)
    if match_obj:
        code = match_obj.group(2)
        token = match_obj.group(1)
        return code, token
    else:
        'failed to match code and token!'


def lagou_login(phone_number, password):
    url = 'https://passport.lagou.com/login/login.json'
    post_data = {
        'isValidate': 'true',
        'username': phone_number,
        'password': encrypt_password(password),
        'request_form_verifyCode': get_captcha(),
        'submit': ''
    }
    code_token = get_anti_Code_Token()
    token_headers = copy.copy(headers)
    token_headers['X-Anit-Forge-Code'] = code_token[0]
    token_headers['X-Anit-Forge-Token'] = code_token[1]
    token_headers['X-Requested-With'] = 'XMLHttpRequest'
    token_headers['Referer'] = 'https://passport.lagou.com/login/login.html'

    response = session.post(url, data=post_data, headers=token_headers)
    session.cookies.save()
    pass


def is_login():  # https://www.lagou.com/resume/threestep.html?isBack=1  https://www.lagou.com/mycenter/invitation.html
    url = 'https://www.lagou.com/mycenter/invitation.html'
    response = session.get(url, headers=headers)
    if response.status_code != 200:
        return False
    else:
        return True


lagou_login('账号', '密码')
is_login()
