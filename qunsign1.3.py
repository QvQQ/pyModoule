#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request, urllib.parse, gzip
from io import BytesIO
import time, base64, re, random
from selenium import webdriver
from apscheduler.schedulers.blocking import BlockingScheduler

class qunsign(object):
    def __init__(self, qnum, pwd):
        self.sched = BlockingScheduler()
        self.task = {}
        self.qnum = qnum
        self.pwd = pwd

    def addtask(self, qunnum, text, poi='', *, hour, minute):
        if minute == 0:
            m = 59
            phour = True
            if hour == 0:
                pday = True
                h = 23
            else:
                pday = False
                h = hour - 1
        else:
            pday = False
            phour = False
            m = minute - 1
            h = hour
        print('Task will execute at {2}:{3}({0}:{1})'.format(h, m, hour, minute))
        key = '{0}:{1}'.format(h, m)
        if key not in self.task:
            self.sched.add_job(self.init, 'cron', hour=h, minute=m)
            self.task[key] = {'pd':pday, 'ph':phour, 'qs':[]}
        self.task[key]['qs'].append([qunnum, text, poi])

    def start(self):
        print('Starting!')
        self.sched.start()

    def init(self):
        print('begin!')
        ltime = time.localtime()
        task = self.task['{0}:{1}'.format(ltime[3], ltime[4])]
        skey = self.login(qnum=self.qnum, pwd=self.pwd)
        deviation = self.getdeviation()
        ltime = time.localtime()
        if task['pd']:  # pday
            day = ltime[2] + 1
            h = 0
            m = 0
        elif task['ph']:  # phour
            day = ltime[2]
            h = ltime[3] + 1
            m = 0
        else:  # normal
            day = ltime[2]
            h = ltime[3]
            m = ltime[4] + 1
        timeb = time.mktime(time.strptime('{year}.{mon}.{day} {h}:{m}:00'.format(year=ltime[0], mon=ltime[1], day=day, h=h, m=m), '%Y.%m.%d %H:%M:%S'))
        while time.time() + deviation < timeb:
            time.sleep(0.05)
            print(time.strftime('%H:%M:%S', time.localtime(time.time() + deviation)))
        for i in task['qs']:
            self.qunsign(qunnum=i[0], text=i[1], poi=i[2], skey=skey)  # 657235491

    def login(self, qnum, pwd):
        driver = webdriver.PhantomJS(executable_path=r'/usr/bin/phantomjs')
        #driver = webdriver.PhantomJS(executable_path=r'D:\Downloads\Compressed\phantomjs-2.1.1-windows\bin\phantomjs.exe')
        #driver = webdriver.Chrome(executable_path=r'D:\Downloads\Compressed\chromedriver_win32\chromedriver.exe')
        loginurl = 'https://xui.ptlogin2.qq.com/cgi-bin/xlogin?appid=715030901&daid=73&pt_no_auth=1&s_url=http%3A%2F%2Fqun.qq.com%2F'
        driver.maximize_window()

        driver.get(loginurl)
        driver.find_element_by_id('switcher_plogin').click()
        driver.find_element_by_id('u').clear()
        driver.find_element_by_id('u').send_keys(qnum)
        driver.find_element_by_id('p').clear()
        driver.find_element_by_id('p').send_keys(pwd)
        driver.execute_script("var login=document.getElementById('login_button');login.click();")

        skey = driver.get_cookie('skey')
        while skey is None:
            skey = driver.get_cookie('skey')
            time.sleep(0.5)
        driver.quit()
        print(skey['value'])
        return skey['value']

    def qunsign(self, qunnum, text, poi, skey):
        uin = 'o{}'.format(self.qnum)
        url = 'https://qun.qq.com/cgi-bin/qiandao/sign/publish'
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Origin': 'https://qun.qq.com',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 7.1.1; MI 6 Build/NMF26X; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043409 Safari/537.36 V1_AND_SQ_7.1.0_0_TIM_D TIM2.0/2.0.0.1703 QQ/6.5.5  NetType/WIFI WebP/0.3.0 Pixel/1080',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,en-US;q=0.8',
            'Connection': 'keep-alive',
            'Cookie': 'skey={skey};uin={uin};'.format(skey=skey, uin=uin),
        }
        template_id = random.randint(1, 9)
        postdata = urllib.parse.urlencode({
            'bkn': self.getbkn(skey),
            'template_id': template_id,
            'gc': qunnum,
            'lgt': '180',
            'lat': '90',
            'poi': poi,
            'text': text
        }).encode('utf-8')
        req = urllib.request.Request(url, postdata, headers)
        r = urllib.request.urlopen(req)
        buf = BytesIO(r.read())
        data = gzip.GzipFile(fileobj=buf).read().decode('utf-8')
        print(data, template_id)

    def getdeviation(self):
        sttime = time.time()
        url = 'http://www.beijing-time.org/time15.asp'
        r = urllib.request.urlopen(url)
        timel = re.findall(r'\d{1,4}', r.read().decode())[1:]
        del timel[3]
        itime = time.mktime(time.strptime(' '.join(timel), '%Y %m %d %H %M %S'))

        return itime - sttime + 0.4

    @staticmethod
    def readpwd():
        return base64.b64decode(b'pwdpwdpwd').decode()

    def getbkn(self, skey):
        hashi = 5381
        for i in range(len(skey)):
            hashi += (hashi << 5) + ord(skey[i])
        return hashi & 2147483647

if __name__ == '__main__':
    sign = qunsign(qnum=qq, pwd=qunsign.readpwd())

    sign.addtask(qunnum=, text='早呀！٩(๑`^´๑)۶', hour=6, minute=30)
    sign.addtask(qunnum=, text='早呀！٩(๑`^´๑)۶', hour=6, minute=30)
    sign.addtask(qunnum=, text='早呀！٩(๑`^´๑)۶', hour=6, minute=30)

    sign.addtask(qunnum=, text='第二天了ʕ•̀ω•́ʔ✧', hour=00, minute=00)
    sign.addtask(qunnum=, text='第二天了ʕ•̀ω•́ʔ✧', hour=00, minute=00)
    sign.addtask(qunnum=, text='第二天了•̀ÿ•́ÿʔ✧', hour=00, minute=00)

    sign.start()























