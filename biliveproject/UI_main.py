# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UI_main.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 480)
        MainWindow.setMinimumSize(QtCore.QSize(800, 480))
        MainWindow.setMaximumSize(QtCore.QSize(800, 480))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        MainWindow.setPalette(palette)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.listView_danmaku = QtWidgets.QListView(self.centralwidget)
        self.listView_danmaku.setGeometry(QtCore.QRect(380, 20, 401, 251))
        self.listView_danmaku.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.listView_danmaku.setObjectName("listView_danmaku")
        self.listView_songlist = QtWidgets.QListView(self.centralwidget)
        self.listView_songlist.setGeometry(QtCore.QRect(380, 360, 411, 111))
        self.listView_songlist.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.listView_songlist.setObjectName("listView_songlist")
        self.label_currentsongname = QtWidgets.QLabel(self.centralwidget)
        self.label_currentsongname.setGeometry(QtCore.QRect(30, 10, 281, 41))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.label_currentsongname.setFont(font)
        self.label_currentsongname.setText("")
        self.label_currentsongname.setObjectName("label_currentsongname")
        self.textBrowser_lyrics = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_lyrics.setGeometry(QtCore.QRect(40, 70, 281, 391))
        self.textBrowser_lyrics.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.textBrowser_lyrics.setObjectName("textBrowser_lyrics")
        self.line_v = QtWidgets.QFrame(self.centralwidget)
        self.line_v.setGeometry(QtCore.QRect(350, 0, 20, 481))
        self.line_v.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_v.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_v.setObjectName("line_v")
        self.line_h = QtWidgets.QFrame(self.centralwidget)
        self.line_h.setGeometry(QtCore.QRect(360, 290, 441, 21))
        self.line_h.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_h.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_h.setObjectName("line_h")
        self.label_tip = QtWidgets.QLabel(self.centralwidget)
        self.label_tip.setGeometry(QtCore.QRect(380, 320, 161, 31))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(65, 131, 197))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(65, 131, 197))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        self.label_tip.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(14)
        self.label_tip.setFont(font)
        self.label_tip.setObjectName("label_tip")
        self.listWidget_danmaku = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget_danmaku.setGeometry(QtCore.QRect(380, 20, 401, 251))
        self.listWidget_danmaku.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.listWidget_danmaku.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.listWidget_danmaku.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.listWidget_danmaku.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.listWidget_danmaku.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.listWidget_danmaku.setTextElideMode(QtCore.Qt.ElideNone)
        self.listWidget_danmaku.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.listWidget_danmaku.setProperty("isWrapping", False)
        self.listWidget_danmaku.setWordWrap(True)
        self.listWidget_danmaku.setObjectName("listWidget_danmaku")
        self.listWidget_songlist = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget_songlist.setGeometry(QtCore.QRect(400, 360, 391, 111))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.listWidget_songlist.setFont(font)
        self.listWidget_songlist.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.listWidget_songlist.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.listWidget_songlist.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.listWidget_songlist.setAutoScroll(False)
        self.listWidget_songlist.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.listWidget_songlist.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.listWidget_songlist.setProperty("isWrapping", True)
        self.listWidget_songlist.setGridSize(QtCore.QSize(400, 35))
        self.listWidget_songlist.setUniformItemSizes(True)
        self.listWidget_songlist.setWordWrap(True)
        self.listWidget_songlist.setObjectName("listWidget_songlist")
        item = QtWidgets.QListWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        brush = QtGui.QBrush(QtGui.QColor(131, 165, 236))
        brush.setStyle(QtCore.Qt.NoBrush)
        item.setForeground(brush)
        self.listWidget_songlist.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_songlist.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.listWidget_songlist.addItem(item)
        self.Slider = QtWidgets.QSlider(self.centralwidget)
        self.Slider.setGeometry(QtCore.QRect(230, 40, 111, 16))
        self.Slider.setOrientation(QtCore.Qt.Horizontal)
        self.Slider.setObjectName("Slider")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.textBrowser_lyrics.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:16px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.label_tip.setText(_translate("MainWindow", "接下来将带来："))
        __sortingEnabled = self.listWidget_songlist.isSortingEnabled()
        self.listWidget_songlist.setSortingEnabled(False)
        self.listWidget_songlist.setSortingEnabled(__sortingEnabled)

