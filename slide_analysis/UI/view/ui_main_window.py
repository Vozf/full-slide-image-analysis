# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_layout.ui'
#
# Created by: PyQt5 UI code generator 5.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.topImagesScrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.topImagesScrollArea.setMinimumSize(QtCore.QSize(260, 0))
        self.topImagesScrollArea.setMaximumSize(QtCore.QSize(541, 16777215))
        self.topImagesScrollArea.setWidgetResizable(True)
        self.topImagesScrollArea.setObjectName("topImagesScrollArea")
        self.topImagesScrollAreaWidgetContents = QtWidgets.QWidget()
        self.topImagesScrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 539, 736))
        self.topImagesScrollAreaWidgetContents.setObjectName("topImagesScrollAreaWidgetContents")
        self.topImagesScrollArea.setWidget(self.topImagesScrollAreaWidgetContents)
        self.horizontalLayout.addWidget(self.topImagesScrollArea)
        self.fullslideImageLayout = QtWidgets.QVBoxLayout()
        self.fullslideImageLayout.setContentsMargins(0, -1, -1, -1)
        self.fullslideImageLayout.setObjectName("fullslideImageLayout")
        self.horizontalLayout.addLayout(self.fullslideImageLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

