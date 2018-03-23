#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time, threading, socket
from collections import deque

class msghandler(object):
    __FLAG_END = b'[##]'  # 数据结尾标志

    def __init__(self, *, sock, excpt=None, excptarg=None, timeout=None):
        self.__sock = sock
        self.__timeout = timeout
        self._peername = sock.getpeername()
        self._sockname = sock.getsockname()
        self.__datalist = deque([])
        if excpt == None:
            self.__excpt = self.__exception
        else:
            self.__excpt = excpt
        self.__excptarg = excptarg
        self.__closed = False
        self.__recvthread = threading.Thread(target=self.__recv)
        self.__recvthread.setDaemon(True)
        self.__recvthread.start()

    def __recv(self):  # 接收消息队列的线程
        while not self.__closed:
            t = b''
            while len(t.split(self.__FLAG_END)) == 1:
                try:
                    tmp = self.__sock.recv(128)
                    if tmp == b'':
                        raise ConnectionResetError
                    t = t + tmp
                except BaseException as e:
                    self.__excpt(e, self.__excptarg)
                    self.close()
                    break
            a = t.split(self.__FLAG_END, 1)
            self.__datalist.append(a[0].decode('utf-8'))
        print('__recv thread finished.')

    def send(self, *text):  # 发送编码后的数据
        dd = b''
        for a in text:
            dd = dd + a.encode('utf-8') + self.__FLAG_END
        try:
            self.__sock.send(dd)
        except BaseException as e:
            self.__excpt(e, self.__excptarg)

    def pickone(self):  # 从消息队列中拾取一条消息并返回
        t = 0
        while len(self.__datalist) == 0:
            time.sleep(0.5)
            t += 0.5
            if self.__timeout and t > self.__timeout:
                raise socket.timeout
        return self.__datalist.popleft()

    def close(self):
        self.__closed = True
        self.__sock.close()

    def __exception(self, exception, excptarg):  # 默认异常处理函数
        print('异常类型：{0}， 异常信息：{1}。'.format(type(exception), exception.args))
        print('Thread will be stopped.')
        print('The remote end %s:%s disconnected!' % self._peername)
        self.close()
