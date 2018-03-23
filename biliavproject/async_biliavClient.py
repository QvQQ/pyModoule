#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket, time, json, gzip, gc
from msghandler import msghandler
from bs4 import BeautifulSoup
import aiohttp, asyncio
from multiprocessing.managers import BaseManager

starttime = time.time()  # 记录开始时间
server_IP = 
server_port = # 服务端端口
numget = 100  # 每次请求的av数
total = 0  # 记录已完成检索的个数
validnum = 0  # 记录失效av的个数
prt = True  # 是否输出爬取内容
sleeptime = 0
timeout = int((numget/100)*32) + int(numget*sleeptime*3)   # 设置请求超时时间
avshower = False

def excptprcs(e, args):
    if type(e) == socket.timeout:
        print('接收消息超时！')
    print('异常类型:{0}， 异常信息:{1}。'.format(type(e), e.args))

def data_to_dict(*, idd, title, up, rank, summ, danmaku, coins, collections, shares, comments, uploaded, category):
    dic = {'id':idd, 'title':title, 'up':up, 'rank':rank, 'sum':summ, 'danmaku':danmaku, 'coins':coins, 'collections':collections, 'shares':shares, 'comments':comments, 'uploaded':uploaded, 'category':category}
    return dic

async def crawl(av, l, percent, avnum, avq):  # 一次性开太多进程会被封IP
    global total, validnum

    def prtinfo(error=False):
        percent[0] += 1
        if avshower:
            if error: avq.put(0)
            else: avq.put(av)
        if prt and total!=0: print('{:#>48}'.format(' {2}/{3} {0:.2f} {1:.2f}%'.format(  # eg. 5/100 62.94 100.00%
            total / ((time.time() - starttime) / 60),  # 爬取速度：个/分
            ((total - validnum) / total) * 100,  # 有效率
            percent[0],  # 当前爬取进度
            avnum)))  # 爬取总量
    # 获取title, up, uploaded, category
    if prt: print('av{av}:Crawler begins!'.format(av=av))
    if prt: print('av{av}:第一阶段开始！'.format(av=av))

    url = r'https://www.bilibili.com/video/av{av}/'.format(av=av)
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
        'Cookie': 'SESSDATA=; DedeUserID='}
    try:
        time.sleep(sleeptime)
        with aiohttp.Timeout(timeout):
            async with aiohttp.ClientSession() as session:
                async with session.get(url=url, headers=header) as f:
                    assert f.status == 200
                    data = await f.text()
    except BaseException as e:
        print('av{av}:Error {0}:{1}'.format(type(e), e.args, av=av))
        prtinfo(True)
        return

    #soup = BeautifulSoup(data, 'html.parser')  # av13318出错
    soup = BeautifulSoup(data, 'lxml')
    # av失效判断
    error = soup.select_one('div[class="b-page-body"] div[class="error-container"]')
    if error is not None:  # 处理失效的av号
        if prt: print('av{av}:失效！'.format(av=av))
        validnum += 1
        result = data_to_dict(idd=av,
                              title='!!!', up='',
                              rank=0, summ=0, danmaku=0, coins=0, collections=0,
                              shares=0, comments=0,
                              uploaded='', category='invalid')
        l.append(result)
        total += 1
        prtinfo()
        return

    def inspection(i):
        if i is None or hasattr(i, 'string') != True or i.string == None:
            return '!!!'
        else:
            return i.string
    uploaded = inspection(soup.select_one('time[itemprop="startDate"] i'))
    title = inspection(soup.select_one('div[class="v-title"] h1'))
    category = '>'.join([inspection(x) for x in soup.select('a[property="v:title"]') if hasattr(x, 'string') == True and x.string != None])
    up = inspection(soup.select_one('div[class="usname"] a'))
    if prt:
        print('av{av}:上传时间:'.format(av=av), uploaded)
        print('av{av}:标题:'.format(av=av), title)
        print('av{av}:分区:'.format(av=av), category)
        print('av{av}:up主:'.format(av=av), up)

    # 获取sum, danmaku, collections, coins, shares, rank
    if prt: print('av{av}:第二阶段开始！'.format(av=av))

    url = 'https://api.bilibili.com/x/web-interface/archive/stat?aid={av}'.format(av=av)
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
        'Cookie': 'SESSDATA=; DedeUserID='}
    try:
        time.sleep(sleeptime)
        with aiohttp.Timeout(timeout):
            async with aiohttp.ClientSession() as session:
                async with session.get(url=url, headers=header) as f:
                    assert f.status == 200
                    data = await f.text()
    except BaseException as e:
        print('av{av}:Error in 2.1 {0}:{1}'.format(type(e), e.args, av=av))
        prtinfo(True)
        return

    try:
        datadict = json.loads(data)['data']
        summ = datadict['view']
        danmaku = datadict['danmaku']
        collections = datadict['favorite']
        coins = datadict['coin']
        shares = datadict['share']
        rank = datadict['his_rank']
    except BaseException as e:
        print('av{av}:Error in 2.2 {0}:{1}'.format(type(e), e.args, av=av))
        prtinfo()
        return
    if prt:
        print('av{av}:播放量:'.format(av=av), summ)
        print('av{av}:弹幕数:'.format(av=av), danmaku)
        print('av{av}:收藏量:'.format(av=av), collections)
        print('av{av}:硬币数:'.format(av=av), coins)
        print('av{av}:分享数:'.format(av=av), shares)
        print('av{av}:最高日排行:'.format(av=av), rank)
    # 获取comments
    if prt: print('av{av}:第三阶段开始！'.format(av=av))

    url = 'https://api.bilibili.com/x/v2/reply?type=1&oid={av}'.format(av=av)
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
        'Cookie': 'SESSDATA=; DedeUserID='}
    try:
        time.sleep(sleeptime)
        with aiohttp.Timeout(timeout):
            async with aiohttp.ClientSession() as session:
                async with session.get(url=url, headers=header) as f:
                    assert f.status == 200
                    data = await f.text()
        datadict = json.loads(data)
    except BaseException as e:
        print('av{av}:Error in 3 {0}:{1}'.format(type(e), e.args, av=av))
        prtinfo(True)
        return

    if 'data' in datadict:
        comments = datadict['data']['page']['acount']
    else:
        comments = -1
    if prt: print('av{av}:评论数:'.format(av=av), comments)

    result = data_to_dict(idd=av,
                          title=title, up=up,
                          rank=rank, summ=summ, danmaku=danmaku, coins=coins, collections=collections, shares=shares, comments=comments,
                          uploaded=uploaded, category=category)

    l.append(result)
    total += 1
    prtinfo()
    return
#------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------
if __name__ == '__main__':
        
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    msg = clientsocket.connect_ex((server_IP, server_port))
    BaseManager.register('getavq')

    if msg != 0:
        print('连接失败！msg=' + str(msg))
        exit()

    if avshower:
        m = BaseManager(address=('127.0.0.1', 3030), authkey=b'abc')
        m.connect()
        avq = m.getavq()
    else: avq = None
    
    conn = msghandler(sock=clientsocket, excpt=excptprcs, timeout=60)

    while True:  # socket: 不保证到达，不保证按顺序到达。
        listt = []
        avs = 0
        dictt_get = {'category': 'get', 'dict': {'num': numget}}
        try:
            conn.send(json.dumps(dictt_get))
        except:
            print('')
        print('Getting...')
        #——————————————————————————————————
        try:  # 超时异常捕获
            tmp = conn.pickone()
        except socket.timeout:
            print('Timeout!')
            tmp = 'error'
        if tmp == 'error':  # 到循环尾
            print('continue')
            continue
        try:  # 断网异常捕获
            avs = json.loads(tmp)  # 获取要爬取的av号
        except BaseException:
            print('Reconnecting...')
            conn.close()
            time.sleep(60)
            clientsocket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            while clientsocket1.connect_ex((server_IP, server_port)) != 0:
                time.sleep(5)
            conn = msghandler(sock=clientsocket1, excpt=excptprcs, timeout=60)
            tmp = 'error'
        if tmp == 'error':  # 到循环尾
            print('continue')
            continue
        #——————————————————————————————————
        # 爬取数据并填充
        percent = [0,]
        print('Crawling...')

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        tasks = [crawl(av, listt, percent, len(avs), avq) for av in avs]  # 对获取到的av号逐个爬取
        loop.run_until_complete(asyncio.wait(tasks))  # 包含两个元素为futures的set; 一个done， 一个pending
        loop.close()

        dictt_post = {'category': 'post', 'dict': {'items': listt}}
        print('Sending...')
        conn.send(json.dumps(dictt_post))
        print('Sent.')
        if not prt and total != 0: print('{:#>48}'.format(' {0:.2f} {1:.2f}%'.format(  # eg. 5/100 62.94 100.00%
                                                total / ((time.time() - starttime) / 60),  # 爬取速度：个/分
                                                ((total - validnum) / total) * 100)))  # 有效率
        time.sleep(2)
