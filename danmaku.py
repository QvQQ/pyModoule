# -*- coding: utf-8 -*-

import sys, socket, urllib, threading, struct, random, json, time, os

class danmaku(object):

    brand = { '127-2':'白学大师', '127-1':'自学高手', '126-2':'荷塘月色',
        '126-1':'绚烂夏花', '125-1':'在此饶舌', '124-1':'大队长', '123-2':'执行委员',
        '123-1':'一般社员', '122-1':'岁月如歌', '121-1':'百战雄狮', '120-1':'门庭若市',
        '119-1':'五魁首', '118-1':'冒险家', '117-1':'圣骑士', '116-1':'庇护之光',
        '115-1':'22应援', '114-1':'33应援', '113-1':'小电视应援', '112-1':'旅人',
        '111-1':'bili link', '110-1':'征服王', '109-1':'征服者', '108-2':'武神',
        '108-1':'演武者', '107-1':'神圣_金', '106-1':'骑士_金', '105-1':'神州_金',
        '104-1':'蒸汽_金', '103-1':'神圣_梅红', '102-1':'骑士_紫蓝',
        '101-1':'神州_浅蓝', '100-1':'蒸汽_棕', '99-1':'神谕阐释者', '98-1':'至高骑士',
        '97-1':'无上至尊', '96-1':'神曲终焉', '95-2':'维纳斯', '95-1':'丘比特',
        '94-1':'酋长', '93-1':'注孤生', '92-1':'年兽', '91-1':'灶神',
        '90-1':'财神爷', '89-2':'意大利炮', '89-1':'爆竹', '88-1':'不负初心',
        '87-1':'四季佬', '86-1':'季佬', '85-1':'孜孜不倦', '84-1':'水滴石穿',
        '83-1':'功成名就', '82-3':'桃花御守', '82-2':'满分御守', '82-1':'御守',
        '81-1':'新年快乐', '80-1':'SANTA☆CLAUS', '79-1':'FFF团长',
        '78-1':'FFF团员', '77-1':'Miss·椛', '76-1':'理事长', '75-3':'名誉总督',
        '75-2':'代理提督', '75-1':'见习舰长', '74-1':'SUPER ST☆R_红',
        '73-1':'SUPER ST☆R_蓝绿', '72-1':'SUPER ST☆R_蓝', '71-1':'SUPER '
        'ST☆R_紫', '70-1':'SUPER ST☆R_黄', '69-1':'ST☆R_红',
        '68-1':'ST☆R_蓝绿', '67-1':'ST☆R_蓝', '66-1':'ST☆R_紫',
        '65-1':'ST☆R_黄', '64-1':'22应援', '63-1':'33应援', '62-1':'小电视应援',
        '61-1':'吃瓜群众', '60-1':'百鬼夜行', '59-1':'一本满足', '58-1':'夜空花火',
        '57-1':'金闪闪', '56-4':'秋之回忆', '56-3':'香山黄栌', '56-2':'栖霞红枫',
        '56-1':'红叶祭', '55-1':'全是套路', '54-1':'暖心', '53-1':'神七',
        '52-1':'高手', '51-1':'大神', '50-1':'钻石王老五', '49-1':'绝对零度',
        '48-1':'钻石星辰', '47-1':'King', '46-1':'甘すぎる', '45-1':'砂糖战士',
        '44-1':'甜党', '43-1':'咸鱼皇', '42-1':'咸蛋超人', '41-1':'咸党',
        '40-1':'甜咸无双', '39-1':'7th ANNV', '38-1':'超耐久', '37-1':'久负盛名',
        '36-1':'方得始终', '35-1':'关灯', '34-1':'起来嗨', '33-1':'被窝',
        '32-1':'菠菜', '31-1':'神龙', '30-1':'追云逐月', '29-1':'度年如日',
        '28-1':'姹紫嫣红', '27-1':'唱见精灵', '26-1':'唱见天使', '25-1':'唱见神话',
        '24-1':'甜心精灵', '23-1':'甜心天使', '22-1':'甜心神话', '21-1':'旅人',
        '20-1':'冒险家', '19-1':'圣骑士', '18-1':'庇护之光', '17-1':'月老',
        '16-1':'资深老司机', '15-1':'校长', '14-1':'教导主任', '13-1':'班主任',
        '12-1':'辅导员', '11-1':'雪亲王', '10-1':'圣·尼古拉斯', '9-1':'真·圣诞爸爸',
        '8-1':'圣诞小天使', '7-1':'圣诞青年', '6-1':'圣诞中年人', '5-1':'圣诞老人',
        '4-1':'超·年糕团长', '3-1':'年糕团长', '2-1':'年糕团', '1-1':'糯米粉' }
    class msg(object):
        pass
    class SEND_GIFT(msg):
        def __init__(self, stu):
            self.usr = stu['data']['uname']
            self.content = '{0}了{1}个{2}！'.format(stu['data']['action'], stu['data']['num'], stu['data']['giftName'])
        pass
    class DANMU_MSG(msg):
        def __init__(self, stu):
            name, Lvlevel, title, ULlevel, rank, brand, t, b = '','','','','','','',''
            if len(stu['info'][2]) > 2:
                name = stu['info'][2][1]
            if len(stu['info'][3]) > 2:
                Lvlevel = stu['info'][3][0]
                title = stu['info'][3][1]
            if len(stu['info'][4]) == 4:
                ULlevel = stu['info'][4][0]
                rank = stu['info'][4][3]
            if len(stu['info'][5]) > 1:
                try:
                    brand = danmaku.brand[stu['info'][5][1][6:]]
                except BaseException:
                    brand = 'unknown'
                    with open(r'brand.txt', 'a', encoding='utf-8', errors='ignore') as f:
                        f.write(str(stu['info'][5], 'utf-8', 'ignore') + '\n')

            if title: t='[{0} {1}]'.format(title, Lvlevel)
            if brand: b='[{}]'.format(brand)
            self.usr = '{t}{b}[UL {u}]{name}'.format(t=t,
                                    b=b, u=ULlevel, name=name)
            self.content = stu['info'][1]

            with open(r'stu.txt', 'ab') as f:
                f.write(bytes(json.dumps(stu, ensure_ascii=False, indent=12), encoding='utf-8')  + b'\n')
        pass
    class WELCOME(msg):
        def __init__(self, stu):
            self.usr = stu['data']['uname']
            if 'svip' in stu['data']:
                if stu['data']['svip'] == 1:
                    self.content = '欢迎年费老爷{0}进入直播间！'.format(stu['data']['uname'])
            elif 'vip' in stu['data']:
                if stu['data']['vip'] == 1:
                    self.content = '欢迎月费老爷{0}进入直播间！'.format(stu['data']['uname'])
           else:
                self.content = '欢迎普通的{0}进入直播间！'.format(stu['data']['uname'])
    class WELCOME_GUARD(msg):
        def __init__(self, stu):
            self.usr = stu['data']['username']
            self.content = '欢迎{0}级守卫{1}进入直播间！'.format(stu['data']['guard_level'] , stu['data']['username'])
    class SYS_MSG(msg):
        def __init__(self, stu):
            self.usr = 'System_Msg'
            self.content = stu['msg']

    prtdebug = False
    inroom = b''.fromhex('00 00 00 10 00 10 00 01 00 00 00 08 00 00 00 01')
    msghead = b''.fromhex('00 10 00 00 00 00 00 05 00 00 00 00')
    sumhead = b''.fromhex('00 00 00 14 00 10 00 01 00 00 00 03 00 00 00 01')

    def __init__(self, *, roomid, prt=None):  # recv:接收弹幕回调函数
        self.__oridata = b''
        self.__roomid = roomid
        self.__uid = int(100000000000000.0 + 200000000000000.0*random.random())
        if prt is not None: self.__prt = prt

    def connect(self):
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.connect((self.__get_serveraddr(), 788))
        self.__closed = False
        self.__recvthread = threading.Thread(target=self.__recv)  # 数据接收线程
        self.__recvthread.setDaemon(True)
        self.__recvthread.start()
        self.__prcsthread = threading.Thread(target=self.__prcs)  # 数据处理线程
        self.__prcsthread.setDaemon(True)
        self.__prcsthread.start()
        self.__beatthread = threading.Thread(target=self.__beat)
        self.__beatthread.setDaemon(True)
        self.__beatthread.start()

    def __get_serveraddr(self):
        url = r'http://live.bilibili.com/api/player?id=cid:{}'.format(self.__roomid)
        #pass
        return 'livecmt-1.bilibili.com'

    def send(self, p):
        try:
            self.__sock.send(p)
        except BaseException:
            self.__closed = True
    
    def start(self):
        ddata = {'roomid':self.__roomid, 'uid':self.__uid}
        pdata = bytes(json.dumps(ddata), 'utf-8')
        phead = struct.pack('>iiii', 16 + len(pdata), 0x100001, 0x07, 0x01)
        self.send(phead + pdata)

    def __recv(self):
        n = 0
        while not self.__closed:
            tmp = self.__sock.recv(1024)
            if tmp == b'':
                print('Server disconnected.')
                self.__closed = True
                break
            with open(r'ori.txt', 'ab') as f:
                f.write(tmp + b'\n')
            self.__oridata += tmp  # 将接收到的数据附加于原始数据链上

    def __prcs(self):
        self.__starttime = time.time()
        rs = struct.Struct('>i12s')  # 协议头结构
        while not self.__closed:
            with threading.Lock():
                if len(self.__oridata) < rs.size:  # 包未接收完
                    continue
                header = self.__oridata[:rs.size]  # 截取前16个字节
                self.__oridata = self.__oridata[rs.size:]
                if header == self.inroom:
                    print('进入房间成功！')
                elif header == self.sumhead:  # beat后返回的观看人数
                    rs1 = struct.Struct('>i')
                    summ = self.__oridata[:rs1.size]
                    self.__oridata = self.__oridata[rs1.size:]
                    summ = rs1.unpack_from(summ)
                    #print('当前总人数为:{}'.format(summ[0]))
                else:
                    uheader = rs.unpack_from(header)
                    length = uheader[0] - rs.size
                    if self.msghead == uheader[1]:  # 为一条弹幕消息
                        if self.prtdebug: print('接收到一条消息，处理中...')
                        if len(self.__oridata) < length:  # 包未接收完
                            self.__oridata = header + self.__oridata  # 还原原始数据
                            if not self.__closed:
                                time.sleep(0.1)
                                continue
                            else:
                                print('不会再有后文了。')
                                break
                        packet = self.__oridata[:length]
                        self.__oridata = self.__oridata[length:]
                        stu = json.loads(str(packet, 'utf-8', 'ignore'))
                        cmd = stu['cmd']
                        if cmd == 'SEND_GIFT':  # 发送礼物
                            if self.prtdebug: print('识别为礼物消息。')
                            self.__prt(self.SEND_GIFT(stu))
                        elif cmd == 'DANMU_MSG':  # 发送弹幕
                            if self.prtdebug: print('识别为弹幕消息。')
                            self.__prt(self.DANMU_MSG(stu))
                        elif cmd == 'WELCOME':  # 欢迎进入直播间
                            if self.prtdebug: print('识别为欢迎消息。')
                            self.__prt(self.WELCOME(stu))
                        elif cmd == 'WELCOME_GUARD':
                            if self.prtdebug: print('识别为欢迎guard消息。')
                            self.__prt(self.WELCOME_GUARD(stu))
                        elif cmd == 'SYS_MSG':  # 系统广播消息
                            if self.prtdebug: print('识别为系统广播消息。')
                            self.__prt(self.SYS_MSG(stu))
                        else:
                            #print('-----------------未支持的消息，已记录:' + stu['cmd'])
                            with open(r'usstu.txt', 'a', encoding='utf-8', errors='ignore') as f:
                                f.write(str(packet, 'utf-8', 'ignore') + '\n')
                    else:
                        #print('-----------------未支持的协议头，已记录。')
                        with open(r'pro.txt', 'a', encoding='utf-8', errors='ignore') as f:
                            f.write(str(header, 'utf-8', 'ignore') + '\n')

        print('共计耗时:{0}s'.format(time.time() - self.__starttime))

    def __beat(self):
        while not self.__closed:
            time.sleep(30)
            ddata = {'roomid':self.__roomid, 'uid':self.__uid}
            pdata = bytes(json.dumps(ddata), 'utf-8')
            phead = struct.pack('>iiii', 16 + len(pdata), 0x100001, 0x02, 0x01)
            self.send(phead + pdata)
            #print('-----------------Beated.-----------------')
        print('-----------------Beater finished.-----------------')

    def __prt(self, msg):
        try:
            print('{0}:{1}'.format(msg.usr, msg.content))
        except BaseException:
            pass
            with open(r'error.txt', 'a', encoding='utf-8', errors='ignore') as f:
                f.write('usr:{0}, content:{1}\n'.format(msg.usr, msg.content))
                #print('输出发生错误！已记录。')
        pass

d = danmaku(roomid=5279)#2171135)
d.connect()
d.start()
print('Done.')

while True:
    pass
