import requests
from selenium import webdriver
from fake_useragent import UserAgent
import time

def login_request():
    ua = UserAgent(verify_ssl=False)
    headers = {
        'User-Agemt': ua.random, 
        'Referer': 'https://shimo.im/login?from=home'
    }
    sess = requests.session()
    login_url ='https://shimo.im/lizard-api/auth/password/login'
    form_data = {
        'Email': 'ming.zinnia@gmail.com', 
        'password': '52MingMing-'
    }
    response = sess.post(login_url, data=form_data, headers=headers, cookies=sess.cookies)
    print(response.cookies)
    profile_url = 'https://shimo.im/dashboard/used'
    content = sess.get(profile_url, headers=headers, cookies=sess.cookies)
    print(content.text)

def login_webdriver():
    try:
        browser = webdriver.Chrome()
        browser.get('https://shimo.im/login?from=home')
        time.sleep(2)

        browser.find_element_by_xpath('//input[@name="mobileOrEmail"]').send_keys('ming.zinnia@gmail.com')
        browser.find_element_by_xpath('//input[@name="password"]').send_keys('52MingMing-')
        browser.find_element_by_xpath('//button[text()="立即登录"]').click()
        time.sleep(5)
    except Exception as e:
        print(e)
    finally:
        browser.close()




if __name__ == '__main__':
    # login_request()
    login_webdriver()
