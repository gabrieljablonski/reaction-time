# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'open_files.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import os

class RTFilesWindow(QtWidgets.QDialog):
    def __init__(self, files):
        super().__init__()

        self.setObjectName("Dialog")
        self.resize(312, 169)
        self.setMinimumSize(QtCore.QSize(312, 169))
        self.setMaximumSize(QtCore.QSize(312, 169))
        self.linePre = QtWidgets.QLineEdit(self)
        self.linePre.setGeometry(QtCore.QRect(90, 10, 161, 20))
        self.linePre.setObjectName("linePre")
        self.linePos = QtWidgets.QLineEdit(self)
        self.linePos.setGeometry(QtCore.QRect(90, 40, 161, 20))
        self.linePos.setObjectName("linePos")
        self.lineRet = QtWidgets.QLineEdit(self)
        self.lineRet.setGeometry(QtCore.QRect(90, 70, 161, 20))
        self.lineRet.setObjectName("lineRet")
        self.linePosOb = QtWidgets.QLineEdit(self)
        self.linePosOb.setGeometry(QtCore.QRect(90, 100, 161, 20))
        self.linePosOb.setObjectName("linePosOb")
        self.btnOpenPre = QtWidgets.QPushButton(self)
        self.btnOpenPre.setGeometry(QtCore.QRect(260, 10, 41, 23))
        self.btnOpenPre.setObjectName("btnOpenPre")
        self.btnOpenPos = QtWidgets.QPushButton(self)
        self.btnOpenPos.setGeometry(QtCore.QRect(260, 40, 41, 23))
        self.btnOpenPos.setObjectName("btnOpenPos")
        self.btnOpenRet = QtWidgets.QPushButton(self)
        self.btnOpenRet.setGeometry(QtCore.QRect(260, 70, 41, 23))
        self.btnOpenRet.setObjectName("btnOpenRet")
        self.btnOpenPosOb = QtWidgets.QPushButton(self)
        self.btnOpenPosOb.setGeometry(QtCore.QRect(260, 100, 41, 23))
        self.btnOpenPosOb.setObjectName("btnOpenPosOb")
        self.btnConfirm = QtWidgets.QPushButton(self)
        self.btnConfirm.setGeometry(QtCore.QRect(90, 130, 101, 31))
        self.btnConfirm.setObjectName("btnConfirm")
        self.btnCancel = QtWidgets.QPushButton(self)
        self.btnCancel.setGeometry(QtCore.QRect(200, 130, 101, 31))
        self.btnCancel.setObjectName("btnCancel")
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(70, 10, 47, 20))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(70, 40, 47, 20))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self)
        self.label_3.setGeometry(QtCore.QRect(40, 70, 47, 20))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self)
        self.label_4.setGeometry(QtCore.QRect(10, 100, 81, 20))
        self.label_4.setObjectName("label_4")

        self.setup_files(files)

        self.btnCancel.clicked.connect(self.close)

        self.btnOpenPre.clicked.connect(lambda: self.select_file(self.linePre))
        self.btnOpenPos.clicked.connect(lambda: self.select_file(self.linePos))
        self.btnOpenRet.clicked.connect(lambda: self.select_file(self.lineRet))
        self.btnOpenPosOb.clicked.connect(lambda: self.select_file(self.linePosOb))

        self.btnConfirm.clicked.connect(self.confirm_files)

        self.files = {
            "pre": "",
            "pos": "",
            "ret": "",
            "posob": ""
        }

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)


    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Abrir arquivos"))
        self.btnOpenPre.setText(_translate("Dialog", "Abrir"))
        self.btnOpenPos.setText(_translate("Dialog", "Abrir"))
        self.btnOpenRet.setText(_translate("Dialog", "Abrir"))
        self.btnOpenPosOb.setText(_translate("Dialog", "Abrir"))
        self.btnConfirm.setText(_translate("Dialog", "Confirmar"))
        self.btnCancel.setText(_translate("Dialog", "Cancelar"))
        self.label.setText(_translate("Dialog", "Pré"))
        self.label_2.setText(_translate("Dialog", "Pós"))
        self.label_3.setText(_translate("Dialog", "Retenção"))
        self.label_4.setText(_translate("Dialog", "Pós-observação"))

    def setup_files(self, files):
        for file in files:
            if "pre" in os.path.split(file)[1] or "PRE" in os.path.split(file)[1]:
                self.linePre.setText(file)
            elif "posob" in os.path.split(file)[1] or "POSOB" in os.path.split(file)[1]:
                self.linePosOb.setText(file)
            elif "pos" in os.path.split(file)[1] or "POS" in os.path.split(file)[1]:
                self.linePos.setText(file)
            elif "ret" in os.path.split(file)[1] or "RET" in os.path.split(file)[1]:
                self.lineRet.setText(file)

    def select_file(self, line):
        file = QtWidgets.QFileDialog.getOpenFileNames(QtWidgets.QFileDialog(), caption="Carrega arquivos",
                                                      filter="Text files (*.txt)")
        if file[0]:
            line.setText(file[0][0])

    def confirm_files(self):
        self.files["pre"] = self.linePre.text()
        self.files["pos"] = self.linePos.text()
        self.files["ret"] = self.lineRet.text()
        self.files["posob"] = self.linePosOb.text()
        self.close()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = RTFilesWindow()
    ui.show()
    sys.exit(app.exec_())

