# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Email_sender.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot
import model



class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Automatic Email Sender")
        Form.resize(759, 434)
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 10, 311, 51))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.CurrentList = QtWidgets.QLineEdit(Form)
        self.CurrentList.setGeometry(QtCore.QRect(350, 20, 351, 25))
        self.CurrentList.setObjectName("CurrentList")
        self.MasterList = QtWidgets.QLineEdit(Form)
        self.MasterList.setGeometry(QtCore.QRect(350, 60, 351, 25))
        self.MasterList.setObjectName("MasterList")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(10, 50, 311, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(10, 90, 311, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.CurrentList_3 = QtWidgets.QLineEdit(Form)
        self.CurrentList_3.setGeometry(QtCore.QRect(532, 110, 171, 25))
        self.CurrentList_3.setObjectName("CurrentList_3")
        self.loadtemplate = QtWidgets.QPushButton(Form)
        self.loadtemplate.setGeometry(QtCore.QRect(360, 110, 89, 25))
        self.loadtemplate.setObjectName("loadtemplate")
        self.loadtemplate.clicked.connect(self.load_email_template)
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(10, 140, 311, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.CurrentList_4 = QtWidgets.QLineEdit(Form)
        self.CurrentList_4.setGeometry(QtCore.QRect(532, 160, 171, 25))
        self.CurrentList_4.setText("")
        self.CurrentList_4.setObjectName("CurrentList_4")
        self.loadprivate = QtWidgets.QPushButton(Form)
        self.loadprivate.setGeometry(QtCore.QRect(360, 160, 89, 25))
        self.loadprivate.setObjectName("loadprivate")
        self.loadprivate.clicked.connect(self.load_email_private_template)
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(10, 180, 311, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.PiName = QtWidgets.QLineEdit(Form)
        self.PiName.setGeometry(QtCore.QRect(352, 200, 351, 25))
        self.PiName.setText("")
        self.PiName.setObjectName("PiName")
        self.Desc = QtWidgets.QLineEdit(Form)
        self.Desc.setGeometry(QtCore.QRect(352, 240, 351, 25))
        self.Desc.setText("")
        self.Desc.setObjectName("Desc")
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setGeometry(QtCore.QRect(10, 220, 311, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.email_subject = QtWidgets.QLineEdit(Form)
        self.email_subject.setGeometry(QtCore.QRect(352, 290, 351, 25))
        self.email_subject.setText("")
        self.email_subject.setObjectName("email_subject")
        self.label_7 = QtWidgets.QLabel(Form)
        self.label_7.setGeometry(QtCore.QRect(10, 270, 311, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(Form)
        self.label_8.setGeometry(QtCore.QRect(10, 320, 311, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.CurrentList_8 = QtWidgets.QLineEdit(Form)
        self.CurrentList_8.setGeometry(QtCore.QRect(532, 340, 171, 25))
        self.CurrentList_8.setText("")
        self.CurrentList_8.setObjectName("CurrentList_8")
        self.loadattachments = QtWidgets.QPushButton(Form)
        self.loadattachments.setGeometry(QtCore.QRect(360, 340, 89, 25))
        self.loadattachments.setObjectName("loadtemplate_3")
        self.loadattachments.clicked.connect(self.load_attachments)
        self.label_9 = QtWidgets.QLabel(Form)
        self.label_9.setGeometry(QtCore.QRect(10, 370, 311, 51))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.checkBox = QtWidgets.QCheckBox(Form)
        self.checkBox.setGeometry(QtCore.QRect(360, 390, 61, 21))
        self.checkBox.setText("")
        self.checkBox.setObjectName("checkBox")
        self.SubmitForm = QtWidgets.QCommandLinkButton(Form)
        self.SubmitForm.setGeometry(QtCore.QRect(666, 390, 91, 41))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.SubmitForm.setFont(font)
        self.SubmitForm.setObjectName("SubmitForm")
        self.label_10 = QtWidgets.QLabel(Form)
        self.label_10.setGeometry(QtCore.QRect(160, 280, 191, 141))
        self.label_10.setObjectName("label_10")
        self.SubmitForm.clicked.connect(self.submit_form)
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
        self.cc = QtWidgets.QLineEdit(Form)
        self.bcc = QtWidgets.QLineEdit(Form)
        self.cc.setText("")
        self.cc.setGeometry(QtCore.QRect(1, 1, 1, 1))
        self.bcc.setText("")
        self.bcc.setGeometry(QtCore.QRect(1, 1, 1, 1))




    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Automatic Email Sender"))
        self.label.setText(_translate("Form", "Current campaign google sheet"))
        self.label_2.setText(_translate("Form", "Master list google sheet"))
        self.label_3.setText(_translate("Form", "Email template File"))
        self.loadtemplate.setText(_translate("Form", "Load file"))
        self.label_4.setText(_translate("Form", "Private Email template File"))
        self.loadprivate.setText(_translate("Form", "Load file"))
        self.label_5.setText(_translate("Form", "PI name"))
        self.label_6.setText(_translate("Form", "Technology Description"))
        self.label_7.setText(_translate("Form", "Email Subject"))
        self.label_8.setText(_translate("Form", "Attachments"))
        self.loadattachments.setText(_translate("Form", "Load file"))
        self.label_9.setText(_translate("Form", "Save as draft"))
        self.SubmitForm.setText(_translate("Form", "Run"))
        self.label_10.setText(
            _translate("Form", "<html><head/><body><p><img src=\":/thumb/yeda_thumb.png\"/></p></body></html>"))

import thumb


