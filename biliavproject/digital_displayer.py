
import RPi.GPIO as gpio
import time, random

class DigitalDisplay(object):
    DIN = 0
    CS = 0
    CLK = 0
    HIGH = 1
    LOW = 0
    def __init__ (self, *, DIN, CS, CLK):
        self.DIN = DIN
        self.CS = CS
        self.CLK = CLK
        
        self.write(0x09, 0xFF)  # 译码方式：BCD码
        self.write(0x0a, 0x06)  # 亮度 
        self.write(0x0b, 0x07)  # 扫描界限；8个数码管显示
        self.write(0x0c, 0x01)  # 掉电模式：0，普通模式：1
        self.write(0x0f, 0x00)  # 显示测试：1；测试结束，正常显示：0
        for i in [1, 2, 3, 4, 5, 6, 7, 8]:
            self.write(i, 0xF)
            
    def write_bit(self, bit):
        time.sleep(0.0001)
        gpio.output(self.CLK, self.LOW)
        time.sleep(0.0001)
        gpio.output(self.DIN, bit)
        time.sleep(0.0001)
        gpio.output(self.CLK, self.HIGH)
        time.sleep(0.0001)

    def write_byte(self, DATA):
        gpio.output(self.CS, self.LOW)
        for i in range (0, 8):
                self.write_bit(DATA&0x80)
                DATA = DATA<<1

    def write(self, address, data):
        gpio.output(self.CS, self.LOW)
        self.write_byte(address)  # num
        self.write_byte(data)
        gpio.output(self.CS, self.HIGH)

if __name__ == '__main__':
    gpio.setmode(gpio.BCM)

    gpio.setup([23,24,27], gpio.OUT)

    digit = DigitalDisplay(DIN=23, CS=24, CLK=27)
    ote = [1, 2, 3, 4, 5, 6, 7, 8]

    while True:
        r = random.randint(0, 99999999)
        rs = '{:0>8}'.format(str(r))
        for i in ote:
            digit.write(i, int(rs[-i]))
        time.sleep(0.01)

    gpio.cleanup()
