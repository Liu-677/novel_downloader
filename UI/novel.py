# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'novel.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1468, 985)
        MainWindow.setFixedSize(MainWindow.width(), MainWindow.height())
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.search = QtWidgets.QPushButton(self.centralwidget)
        self.search.setGeometry(QtCore.QRect(830, 40, 91, 41))
        self.search.setAutoFillBackground(False)
        self.search.setFlat(False)
        self.search.setObjectName("search")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(720, 100, 141, 41))
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.novel_list_title = QtWidgets.QLabel(self.centralwidget)
        self.novel_list_title.setGeometry(QtCore.QRect(260, 100, 141, 41))
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(12)
        self.novel_list_title.setFont(font)
        self.novel_list_title.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.novel_list_title.setTextFormat(QtCore.Qt.AutoText)
        self.novel_list_title.setAlignment(QtCore.Qt.AlignCenter)
        self.novel_list_title.setObjectName("novel_list_title")
        self.search_input = QtWidgets.QLineEdit(self.centralwidget)
        self.search_input.setGeometry(QtCore.QRect(540, 40, 281, 41))
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.search_input.setFont(font)
        self.search_input.setAlignment(QtCore.Qt.AlignCenter)
        self.search_input.setDragEnabled(True)
        self.search_input.setClearButtonEnabled(True)
        self.search_input.setObjectName("search_input")
        self.novel_list = QtWidgets.QListWidget(self.centralwidget)
        self.novel_list.setGeometry(QtCore.QRect(170, 150, 330, 761))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.novel_list.setFont(font)
        self.novel_list.setLineWidth(2)
        self.novel_list.setObjectName("novel_list")
        self.novel_img = QtWidgets.QLabel(self.centralwidget)
        self.novel_img.setGeometry(QtCore.QRect(610, 170, 180, 240))
        self.novel_img.setText("")
        self.novel_img.setObjectName("novel_img")
        self.novel_info = QtWidgets.QTextBrowser(self.centralwidget)
        self.novel_info.setGeometry(QtCore.QRect(800, 170, 421, 251))
        self.novel_info.setObjectName("novel_info")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(610, 460, 141, 41))
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.chapter_list = QtWidgets.QListWidget(self.centralwidget)
        self.chapter_list.setGeometry(QtCore.QRect(550, 510, 256, 391))
        self.chapter_list.setObjectName("chapter_list")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(840, 560, 131, 41))
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(840, 510, 131, 41))
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(980, 490, 72, 15))
        self.label_5.setText("")
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(1040, 460, 141, 41))
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(12)
        self.label_6.setFont(font)
        self.label_6.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.start = QtWidgets.QSpinBox(self.centralwidget)
        self.start.setGeometry(QtCore.QRect(970, 510, 71, 31))
        self.start.setMaximum(10000)
        self.start.setObjectName("start")
        self.end = QtWidgets.QSpinBox(self.centralwidget)
        self.end.setGeometry(QtCore.QRect(970, 560, 71, 31))
        self.end.setMaximum(10000)
        self.end.setObjectName("end")
        self.downPart_btn = QtWidgets.QPushButton(self.centralwidget)
        self.downPart_btn.setGeometry(QtCore.QRect(1070, 530, 93, 41))
        self.downPart_btn.setObjectName("downPart_btn")
        self.downloadAll_btn = QtWidgets.QPushButton(self.centralwidget)
        self.downloadAll_btn.setGeometry(QtCore.QRect(1210, 530, 93, 41))
        self.downloadAll_btn.setObjectName("downloadAll_btn")
        self.log = QtWidgets.QTextBrowser(self.centralwidget)
        self.log.setGeometry(QtCore.QRect(850, 640, 501, 281))
        self.log.setTabChangesFocus(False)
        self.log.setObjectName("log")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(1050, 600, 141, 41))
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(12)
        self.label_7.setFont(font)
        self.label_7.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setEnabled(True)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1468, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "小说下载器"))
        self.search.setText(_translate("MainWindow", "检索"))
        self.label.setText(_translate("MainWindow", "小说信息"))
        self.novel_list_title.setText(_translate("MainWindow", "小说列表"))
        self.search_input.setText(_translate("MainWindow", "输入小说名称"))
        self.label_2.setText(_translate("MainWindow", "章节列表"))
        self.label_3.setText(_translate("MainWindow", "终止章节："))
        self.label_4.setText(_translate("MainWindow", "起始章节："))
        self.label_6.setText(_translate("MainWindow", "下载"))
        self.downPart_btn.setText(_translate("MainWindow", "下载"))
        self.downloadAll_btn.setText(_translate("MainWindow", "全本下载"))
        self.label_7.setText(_translate("MainWindow", "日志"))
