# -*- coding:utf-8 -*-
import time
from selenium import webdriver
import requests
import pickle

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.3397.16 Safari/537.36',
}


def taobao_login(username, password):
    driver = webdriver.Chrome(executable_path="C:\Users\Stone\PycharmProjects\Virtualenv\scrapy_1\chromedriver.exe")

    # driver = webdriver.PhantomJS(executable_path="C:/Users/Stone/PycharmProjects/Virtualenv/scrapy_1/phantomjs-2.1.1"
    #                                           "-windows/bin/phantomjs.exe")
    # driver.get('https://login.taobao.com/member/login.jhtml')
    driver.get('https://detail.tmall.com/item.htm?id=545613104853')
    time.sleep(2)  # 等待加载
    print driver.page_source
    driver.find_element_by_css_selector('div.login-switch i#J_Quick2Static').click()
    driver.find_element_by_css_selector('input#TPL_username_1').clear()
    driver.find_element_by_css_selector('input#TPL_password_1').clear()
    driver.find_element_by_css_selector('input#TPL_username_1').send_keys(username)
    driver.find_element_by_css_selector('input#TPL_password_1').send_keys(password)
    driver.find_element_by_css_selector('button#J_SubmitStatic').click()
    driver.delete_all_cookies()
    tb_cookies = driver.get_cookies()
    driver.close()  # 关闭浏览器
    pickle.dump(tb_cookies, open('cookies.pkl', 'wb'))  # 保存cookies
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
    response = session.get('https://i.taobao.com/my_taobao.htm', headers=headers,
                           allow_redirects=False)
    print response.text


taobao_login('账号', '密码')
# is_login()