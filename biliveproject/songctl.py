#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from PyQt5.QtCore import QUrl, pyqtSignal
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer

class songctl(object):

    def __init__(self, queue, signals):
        self.queue = queue
        self.signals =signals
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.mediaPlayer.stateChanged.connect(signals._signal_stateChanged.emit)
        self.mediaPlayer.positionChanged.connect(signals._signal_positionChanged.emit)
        self.mediaPlayer.durationChanged.connect(signals._signal_durationChanged.emit)
        #self.mediaPlayer.error.connect(self.handleError)

    def handleError(self):
        return self.mediaPlayer.errorString()

    def play(self, localpath):
        print('localpath:{}'.format(localpath))
        self.mediaPlayer.stop()
        self.mediaPlayer.setMedia(
            QMediaContent(
                QUrl.fromLocalFile(localpath)))
        self.mediaPlayer.play()
        print('开始播放{}'.format('23333'))
