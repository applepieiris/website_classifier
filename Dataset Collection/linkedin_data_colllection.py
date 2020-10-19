import requests
import re
import json
from lxml import etree
import urllib
import time
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

session = requests.session()

def login(name, password):
    session.headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
        }
    url = 'https://www.linkedin.com/'
    login_url = 'https://www.linkedin.com/uas/login-submit?' \
                'loginSubmitSource=GUEST_HOME'
    page = session.get(url)
    rp = etree.HTML(page.text)
    loginCsrfParam = rp.xpath('//*[@name="loginCsrfParam"]/@value')[0]

    form_data = {
        'session_key': name,
        'session_password': password,
        'loginCsrfParam': loginCsrfParam,
        'isJsEnabled': 'false'
    }
    page_login = session.post(login_url, data=form_data
                              )

    login_rp = etree.HTML(page_login.text)
    verify_url = 'https://www.linkedin.com/checkpoint/challenge/verify'
    csrfToken = login_rp.xpath('//*[@name="csrfToken"]/@value')[0]
    pageInstance = login_rp.xpath('//*[@name="pageInstance"]/@value')[0]
    resendUrl = login_rp.xpath('//*[@name="resendUrl"]/@value')[0]
    challengeId = login_rp.xpath('//*[@name="challengeId"]/@value')[0]
    language = 'zh-CN'
    displayTime = login_rp.xpath('//*[@name="displayTime"]/@value')[0]
    challengeSource = login_rp.xpath('//*[@name="challengeSource"]/@value')[0]
    requestSubmissionId = login_rp.xpath('//*[@name="requestSubmissionId"]/@value')[0]
    challengeType = login_rp.xpath('//*[@name="challengeType"]/@value')[0]
    challengeData = login_rp.xpath('//*[@name="challengeData"]/@value')[0]
    failureRedirectUri = login_rp.xpath('//*[@name="failureRedirectUri"]/@value')[0]
    pin = input('请输入验证码')
    verify_data = {
        'csrfToken': csrfToken,
        'pageInstance': pageInstance,
        'resendUrl': resendUrl,
        'challengeId': challengeId,
        'language': language,
        'displayTime': displayTime,
        'challengeSource': challengeSource,
        'requestSubmissionId': requestSubmissionId,
        'challengeType': challengeType,
        'challengeData': challengeData,
        'failureRedirectUri': failureRedirectUri,
        'pin': pin,
    }
    verify_post = session.post(verify_url, data=verify_data)
    print(verify_post.status_code)

    soup = BeautifulSoup(verify_post.text,'lxml')
    print(soup.prettify())

def login2(username,password):
    session.headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,fr;q=0.6",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        }

    login_get_url = "https://www.linkedin.com/uas/login"

    page = session.get(login_get_url)
    rp = etree.HTML(page.text)

    soup = BeautifulSoup(page.text,'lxml')
    #print(soup.prettify())

    csrf_param = rp.xpath('//*[@name="loginCsrfParam"]/@value')[0]
    csrf_token = rp.xpath('//*[@name="csrfToken"]/@value')[0]

    ac = soup.find(attrs={'name':'ac'})['value']
    parentPageKey =soup.find(attrs={'name':'parentPageKey'})['value']
    sIdString = soup.find(attrs ={'name':'sIdString'})['value']
    #pageInstance = soup.find(attrs ={'name':'pageInstance'})['value']

    payload = {
        'csrf_token':csrf_token,
        'session_key': username,
        'ac':ac,
        'sIdString': sIdString,
        'parentPageKey': parentPageKey,
        'pageInstance': 'urn:li:page:d_checkpoint_lg_consumerLogin;rnG8RkwmS/qgUQKpsGp5Xw==',
        'session_password': password,
        'trk': '',
        'loginCsrfParam': csrf_param,
        'fp_data': 'default',
        '_d':'d',
        'showGoogleOneTapLogin':'true',
        'controlId':'d_checkpoint_lg_consumerLogin-login_submit_button',
        'loginFlow':'REMEMBER_ME_OPTIN',
    }
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    login_post_url = "https://www.linkedin.com/uas/login-submit"
    #sessionCookies = session.cookies
    login_post = session.post(login_post_url, data=payload, headers=headers).text
    soup = BeautifulSoup(login_post)
    print(soup.prettify())

def simulation_login(browser,username,pw):
    login_get_url = "https://www.linkedin.com/uas/login"

    browser.get(login_get_url)
    wait = WebDriverWait(browser,10)
    input = wait.until(EC.presence_of_element_located((By.ID,'username')))

    user = browser.find_element_by_name('session_key')
    user.send_keys(username)

    password = browser.find_element_by_name('session_password')
    password.send_keys(pw)

    browser.find_element_by_xpath('//button[@type="submit"]').send_keys(Keys.ENTER)

    browser.implicitly_wait(3)

def get_company_link(browser):
    ul = browser.find_element_by_tag_name('ul')
    ul.send_keys(Keys.DOWN)
    soup = BeautifulSoup(browser.page_source,'lxml')
    #print(soup.prettify())
    names = soup.find_all(attrs={"data-control-name":"job_card_company_link"})

    print(names)

def index_page(browser,page):
    print("正在爬取第",page,"页")
    try:
        if page > 1 :
            index = (page - 1) * 25
            url  = "https://www.linkedin.com/jobs/search/?" + "&start=" + index
        else:
            url = "https://www.linkedin.com/jobs/search/?"
        browser.get(url)

        wait = WebDriverWait(browser,10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME,'ul')))
        browser.implicitly_wait(3)
        get_company_link(browser)
    except TimeoutError:
        index_page(browser,page)

if __name__ == '__main__':
   # chrome_options = Options()
   # chrome_options.add_argument('--headless')
   browser = webdriver.Chrome()
   simulation_login(browser,"usrnamme",'password')
   index_page(browser,1)