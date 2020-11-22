# coding = utf-8

import json
import time
import requests
from pyquery import PyQuery as pq
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

class BadmintonCrawler:

    def __init__(self):
        self.url = "https://elife.fudan.edu.cn/public/front/toResourceFrame.htm?contentId=8aecc6ce749544fd01749a31a04332c2"
        self.__login()

    def __login(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome("/usr/local/bin/chromedriver", options=options)
        url = "https://uis.fudan.edu.cn/authserver/login"
        driver.get(url)
        driver.find_element_by_id("username").send_keys("xx")
        driver.find_element_by_id("password").send_keys("xx")
        driver.find_element_by_id("idcheckloginbtn").click()
        # 显示等待
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "auth_content_iframe"))
            )
        finally:
            cookies = driver.get_cookies()
            self.__getCookies(cookies)
            driver.close()

    def __getCookies(self,cookies):
        coo = {}
        coo['JSESSIONID'] = cookies[1]['value']
        coo['iPlanetDirectoryPro'] = cookies[2]['value']
        self.cookies = coo

    def __getDoc(self):
        try:
            r = requests.get(self.url,cookies=self.cookies)
            r.raise_for_status()  # 若请求不成功,抛出HTTPError 异常
            doc = pq(r.text)
            return doc
        except Exception as e:
            print(e)

    def sendMail(self,times):
        import smtplib
        from email.mime.text import MIMEText
        from email.header import Header

        # 第三方 SMTP 服务
        mail_host = "smtp.163.com"
        mail_user = "ltobenull"
        mail_pass = "lsbssg327137362"

        sender = 'ltobenull@163.com'
        receivers = 'ltobenull@qq.com'
        mail_msg = f"""
        <p>羽毛球有以下时间段空场</p>
        <p>{times}</p>
        """
        message = MIMEText(mail_msg, 'html', 'utf-8')
        message['From'] = sender
        message['To'] = receivers

        subject = '羽毛球空场预定'
        message['Subject'] = Header(subject, 'utf-8')

        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect(mail_host, 25)
            smtpObj.login(mail_user, mail_pass)
            smtpObj.sendmail(sender, [receivers], message.as_string())
            print("邮件发送成功")
        except smtplib.SMTPException as e:
            print(f"无法发送邮件{e}")

    def checkEmpty(self,doc):
        times = []
        trList = doc(".site_table .site_tr")
        for tr in trList.items():
            imgSrc = str(tr("td[align='right'] img").attr('src'))
            if 'reserve.gif' in imgSrc:
                times += [tr('.site_td1:first-child font').text()]
        return times

    def run(self):
        doc = self.__getDoc()
        times = self.checkEmpty(doc)
        if times:
            self.sendMail(times)


if __name__ == '__main__':
    bc = BadmintonCrawler()
    bc.run()
    print(f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())} done!')