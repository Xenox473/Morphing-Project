# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MorphingGUI.ui'
#
# Created: Thu Apr 19 17:15:42 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(744, 644)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.LoadStartBtn = QtGui.QPushButton(self.centralwidget)
        self.LoadStartBtn.setGeometry(QtCore.QRect(60, 20, 161, 27))
        self.LoadStartBtn.setObjectName("LoadStartBtn")
        self.LoadEndBtn = QtGui.QPushButton(self.centralwidget)
        self.LoadEndBtn.setGeometry(QtCore.QRect(440, 20, 161, 27))
        self.LoadEndBtn.setObjectName("LoadEndBtn")
        self.horizontalSlider = QtGui.QSlider(self.centralwidget)
        self.horizontalSlider.setGeometry(QtCore.QRect(90, 290, 541, 20))
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.StartingImage = QtGui.QGraphicsView(self.centralwidget)
        self.StartingImage.setGeometry(QtCore.QRect(60, 60, 256, 192))
        self.StartingImage.setObjectName("StartingImage")
        self.EndingImage = QtGui.QGraphicsView(self.centralwidget)
        self.EndingImage.setGeometry(QtCore.QRect(440, 60, 256, 192))
        self.EndingImage.setObjectName("EndingImage")
        self.BlendResult = QtGui.QGraphicsView(self.centralwidget)
        self.BlendResult.setGeometry(QtCore.QRect(250, 330, 256, 192))
        self.BlendResult.setObjectName("BlendResult")
        self.BlendBtn = QtGui.QPushButton(self.centralwidget)
        self.BlendBtn.setGeometry(QtCore.QRect(330, 560, 92, 27))
        self.BlendBtn.setObjectName("BlendBtn")
        self.StartingImagetxt = QtGui.QLabel(self.centralwidget)
        self.StartingImagetxt.setGeometry(QtCore.QRect(130, 260, 111, 17))
        self.StartingImagetxt.setObjectName("StartingImagetxt")
        self.EndingImagetxt = QtGui.QLabel(self.centralwidget)
        self.EndingImagetxt.setGeometry(QtCore.QRect(510, 260, 111, 20))
        self.EndingImagetxt.setObjectName("EndingImagetxt")
        self.Blendingtxt = QtGui.QLabel(self.centralwidget)
        self.Blendingtxt.setGeometry(QtCore.QRect(330, 530, 111, 20))
        self.Blendingtxt.setObjectName("Blendingtxt")
        self.Alphatxt = QtGui.QLabel(self.centralwidget)
        self.Alphatxt.setGeometry(QtCore.QRect(50, 290, 41, 17))
        self.Alphatxt.setObjectName("Alphatxt")
        self.SlidertxtBox = QtGui.QLineEdit(self.centralwidget)
        self.SlidertxtBox.setGeometry(QtCore.QRect(640, 290, 51, 27))
        self.SlidertxtBox.setObjectName("SlidertxtBox")
        self.label_5 = QtGui.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(90, 310, 62, 17))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtGui.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(610, 310, 62, 17))
        self.label_6.setObjectName("label_6")
        self.checkBox = QtGui.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(320, 260, 131, 22))
        self.checkBox.setObjectName("checkBox")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 744, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.LoadStartBtn.setText(QtGui.QApplication.translate("MainWindow", "Load Starting Image ...", None, QtGui.QApplication.UnicodeUTF8))
        self.LoadEndBtn.setText(QtGui.QApplication.translate("MainWindow", "Load Ending Image ...", None, QtGui.QApplication.UnicodeUTF8))
        self.BlendBtn.setText(QtGui.QApplication.translate("MainWindow", "Blend", None, QtGui.QApplication.UnicodeUTF8))
        self.StartingImagetxt.setText(QtGui.QApplication.translate("MainWindow", "Starting Image", None, QtGui.QApplication.UnicodeUTF8))
        self.EndingImagetxt.setText(QtGui.QApplication.translate("MainWindow", "Ending Image", None, QtGui.QApplication.UnicodeUTF8))
        self.Blendingtxt.setText(QtGui.QApplication.translate("MainWindow", "Blending Result", None, QtGui.QApplication.UnicodeUTF8))
        self.Alphatxt.setText(QtGui.QApplication.translate("MainWindow", "Alpha", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("MainWindow", "0.0", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("MainWindow", "1.0", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox.setText(QtGui.QApplication.translate("MainWindow", "Show Triangles", None, QtGui.QApplication.UnicodeUTF8))

