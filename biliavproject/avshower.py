#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random, time, queue, threading
import RPi.GPIO as gpio
from multiprocessing.managers import BaseManager
from digital_displayer import DigitalDisplay

avqueue = queue.Queue()
num = 0

def uuu():
    return avqueue

def show():
    ote = [1, 2, 3, 4, 5, 6, 7, 8]
    digitnum = 0
    while True:
        if num != digitnum:
            print('av{}'.format(num))
            ns = str(num)
            for i in ote[:len(ns)]:
                digit.write(i, int(ns[-i]))

        digitnum = num
        time.sleep(0.01)

if __name__ == '__main__':
    
    BaseManager.register('getavq', callable=uuu)
    m = BaseManager(address=('127.0.0.1', 3030), authkey=b'abc')

    m.start()
    print('Started.')
    avqueue = m.getavq()

    gpio.setmode(gpio.BCM)
    gpio.setup([23, 24, 27], gpio.OUT)
    digit = DigitalDisplay(DIN=23, CS=24, CLK=27)
    
    shower = threading.Thread(target=show)
    shower.setDaemon(True)
    shower.start()
    
    while True:
        try:
            #i = avqueue.get(timeout=1)
            num = random.randint(0, 100000000)#i#max(num, i)
        except:
            time.sleep(0.1)
            
    gpio.cleanup()
    m.shutdown()

