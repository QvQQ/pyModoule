# -*- coding: utf-8 -*-

"""
Module implementing win_Main.
"""

from PyQt5.QtCore import pyqtSlot, QCoreApplication, Qt, QThread, pyqtSignal, QUrl
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QApplication, QListWidgetItem, QLayout, QScrollBar
from PyQt5.QtGui import QBrush, QColor, QCursor
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer

from UI_main import Ui_MainWindow
from danmaku import danmaku
from songdl import songdl
from songctl import songctl
import sys, time, re, queue, os

class win_main(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    _signal_textBrowser_lyrics = pyqtSignal(str)
    _signal_listprint = pyqtSignal(str, str)
    _signal_playsong = pyqtSignal(str)

    _signal_stateChanged = pyqtSignal(int)
    _signal_positionChanged = pyqtSignal(int)
    _signal_durationChanged = pyqtSignal(int)

    _signal_p = pyqtSignal(int)
    _signal_d = pyqtSignal(int)
    _signal_s = pyqtSignal(int)

    def __init__(self, parent=None):
        """
        Constructor

        @param parent reference to the parent widget
        @type QWidget
        """
        super(win_main, self).__init__(parent)
        self.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self._signal_textBrowser_lyrics.connect(self.callbacklog)
        self._signal_listprint.connect(self.listprint)
        self._signal_playsong.connect(self.playsong)

        self._signal_durationChanged.connect(self.durationChanged)
        self._signal_positionChanged.connect(self.positionChanged)
        self._signal_stateChanged.connect(self.mediaStateChanged)

        self._signal_p.connect(self.p)
        self._signal_d.connect(self.d)
        self._signal_s.connect(self.s)

        self.duration = 0
        self.sctl = songctl(q, self)

    def p(self, p):
        print('Postion:' + str(p))
        self.Slider.setSliderPosition(p)
        d = self.duration
        #self.textBrowser_lyrics.scrollContentsBy(0, 10)
        m = self.textBrowser_lyrics.verticalScrollBar().maximum()
        if d != 0:
            self.textBrowser_lyrics.verticalScrollBar().setValue(int( (p/d)*m ))

    def d(self, d):
        print('Duration:' + str(d))
        self.duration = d
        self.Slider.setRange(0, d)

    def s(self, s):
        print('State:' + str(s))
        if s == QMediaPlayer.StoppedState:
            if not q.empty():
                song = q.get()
                self.listWidget_songlist.item(0).setText(self.listWidget_songlist.item(1).text())
                self.listWidget_songlist.item(1).setText(self.listWidget_songlist.item(2).text())
                self.listWidget_songlist.item(2).setText('')
                self.label_currentsongname.setText(song['name'])
                self.callbacklog(song['lyrics'])
                self.playsong(song['localpath'])
            else:
                self.listWidget_songlist.item(0).setText('')
                self.listprint('_(:ι」∠)_', '已经播放完所有歌曲啦！再来投喂一点嘛！')

    def playsong(self, localpath):
        self.sctl.play(localpath)

    def mediaStateChanged(self, state):
        self._signal_s.emit(state)
    def positionChanged(self, position):
        self._signal_p.emit(position)
    def durationChanged(self, duration):
        self._signal_d.emit(duration)

    def listprint(self, head, msg):
        print(self.sctl.handleError())
        brush = QBrush(QColor(255, 213, 214))
        brush.setStyle(Qt.SolidPattern)
        item1 = QListWidgetItem()
        item1.setBackground(brush)
        item1.setText(QCoreApplication.translate("Ui_MainWindow", '{}:'.format(head)))

        brush = QBrush(QColor(205, 232, 255))
        brush.setStyle(Qt.SolidPattern)
        item2 = QListWidgetItem()
        item2.setBackground(brush)
        item2.setText(QCoreApplication.translate("Ui_MainWindow", '        {}'.format(msg)))
        self.listWidget_danmaku.addItem(item1)
        self.listWidget_danmaku.addItem(item2)
        self.listWidget_danmaku.addItem('')
        item2.setHidden(False)
        item1.setHidden(False)
        for i in range(2):
            self.listWidget_danmaku.scrollToBottom()
            time.sleep(0.1)

    def callbacklog(self, msg):
        self.textBrowser_lyrics.setHtml(msg)

    def mousePressEvent(self, event):
        if event.button()==Qt.LeftButton:
            self.m_drag=True
            self.m_DragPosition=event.globalPos()-self.pos()
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))
    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_drag:
            self.move(QMouseEvent.globalPos()-self.m_DragPosition)
            QMouseEvent.accept()
    def mouseReleaseEvent(self, QMouseEvent):
        self.m_drag=False
        self.setCursor(QCursor(Qt.ArrowCursor))
#——————————————————————————————————————————————

def listprint(head, msg):
    MainWindow._signal_listprint.emit(head, msg)

def lyricsformat(msg):
    i = 0
    head = '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd"><html><head><meta name="qrichtext" content="1" /><style type="text/css">p, li { white-space: pre-wrap; }</style></head><body style=" font-family:'SimSun'; font-size:9pt; font-weight:400; font-style:normal;">'''
    tail = '''</body></html>'''
    middle = '''<p align="center" style=" margin-top:0px; margin-bottom:16px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;"><span style=" font-family:'Arial,Microsoft YaHei'; font-size:16px; color:#7d7d7d;">{}</span></p>'''
    msgp = re.compile(r'\[.*\]').sub('', msg)
    lines = msgp.split('\n')
    while i < len(lines):
        lines[i] = lines[i].strip()
        if lines[i] == '':
            lines.pop(i)
        else:
            i += 1
    lyrics = head
    for line in lines:
        lyrics += middle.format(line)
    lyrics += tail
    return lyrics

def danmakuprcs(msg):
    if isinstance(msg, danmaku.SEND_GIFT):
        listprint(msg.usr, msg.content)
    elif isinstance(msg, danmaku.DANMU_MSG):
        listprint(msg.name, msg.content)
        msgsp = msg.content.split(' ')
        i = 0
        while i < len(msgsp):
            if msgsp[i] == '':
                msgsp.pop(i)
            else: i += 1
        if len(msgsp) >= 2 and msgsp[0] == '点歌':
            print('开始点歌：{}'.format(msgsp[1]))
            only = False
            if MainWindow.listWidget_songlist.item(0).text() == '':
                item = MainWindow.listWidget_songlist.item(0)
                only = True
            elif MainWindow.listWidget_songlist.item(1).text() == '':
                item = MainWindow.listWidget_songlist.item(1)
            elif MainWindow.listWidget_songlist.item(2).text() == '':
                item = MainWindow.listWidget_songlist.item(2)
            else:  # 无空闲候选歌曲
                item = None
                listprint('QAQ', '当前候选歌曲已满，请稍后尝试，么么扎！')
                return

            if item:
                sdl = songdl()
                if len(msgsp) == 2:
                    item.setText('{} - Searching...'.format(msgsp[1]))
                    item.setHidden(False)  # 实时显示
                    song = sdl.search(songname=msgsp[1])
                    if song is None:
                        listprint(head='QwQ', msg='没有找到这首{}呢！看看是不是打错了w。'.format(msgsp[1]))
                        item.setText('')
                        item.setHidden(False)
                        return
                else:
                    item.setText('{0} {1} - Searching...'.format(msgsp[1], msgsp[2]))
                    item.setHidden(False)  # 实时显示
                    song = sdl.search(songname=msgsp[1], artist=msgsp[2])
                    if song is None:
                        listprint(head='QwQ', msg='没有找到这首{1}的\'{0}\'呢！看看是不是打错了w。'.format(msgsp[1], msgsp[2]))
                        item.setText('')
                        item.setHidden(False)
                        return
                item.setText('{0} {1} - Getting lyrics...'.format(song['name'], song['artist']))
                item.setHidden(False)
                song['lyrics'] = lyricsformat(sdl.getlyrics(song))
                item.setText('{0} {1} - Downloading...'.format(song['name'], song['artist']))
                item.setHidden(False)
                def dlreport(a, b, c):
                    per = 100.0 * a * b / c  # a:已经下载的数据块，b:数据块的大小，c:远程文件的大小
                    if per > 100:
                        per = 100
                    per = int(per)
                    item.setText('{0} {1} - {2}'.format(song['name'], song['artist'], per))
                    item.setHidden(False)
                localpath = sdl.downloadsong(song=song, localdir='/home/pi/Desktop/biliveproject/songs/'.format(os.sep), dlreport=dlreport)
                song['localpath'] = localpath
                item.setText('{0} {1}'.format(song['name'], song['artist']))
                item.setHidden(False)
                song['item'] = item
                if only:
                    MainWindow.label_currentsongname.setText(song['name'])
                    MainWindow._signal_textBrowser_lyrics.emit(song['lyrics'])
                    MainWindow._signal_playsong.emit(localpath)
                else:
                    q.put(song)

    elif isinstance(msg, danmaku.WELCOME):
        listprint(msg.usr, msg.content)
    elif isinstance(msg, danmaku.SYS_MSG):
        listprint(msg.usr, msg.content)
    elif isinstance(msg, danmaku.WELCOME_GUARD()):
        listprint(msg.usr, msg.content)
    else:
        print('Unknown msg!')

if __name__ == "__main__":
    q = queue.Queue()

    app = QApplication(sys.argv)
    MainWindow = win_main()
    MainWindow.show()

    dk = danmaku(roomid=2171135, prt=danmakuprcs)  # 自己的直播间房间号
    dk.connect()
    dk.start()

    tmp = app.exec_()
    MainWindow.destroy()
    sys.exit(tmp)

