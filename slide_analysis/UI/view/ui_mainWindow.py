# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'slide_analysis/UI/view/main_layout.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.topImagesScrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.topImagesScrollArea.setMaximumSize(QtCore.QSize(260, 16777215))
        self.topImagesScrollArea.setWidgetResizable(True)
        self.topImagesScrollArea.setObjectName("topImagesScrollArea")
        self.topImagesScrollAreaWidgetContents = QtWidgets.QWidget()
        self.topImagesScrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 258, 736))
        self.topImagesScrollAreaWidgetContents.setObjectName("topImagesScrollAreaWidgetContents")
        self.topImagesScrollArea.setWidget(self.topImagesScrollAreaWidgetContents)
        self.gridLayout.addWidget(self.topImagesScrollArea, 0, 0, 1, 1)
        self.fullSlideImageGraphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.fullSlideImageGraphicsView.setObjectName("fullSlideImageGraphicsView")
        self.gridLayout.addWidget(self.fullSlideImageGraphicsView, 0, 1, 1, 1)
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

