# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'systen_row.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt



class Ui_systemsRows(object):
    def setupUi(self, systemsRows):
        systemsRows.setObjectName("systemsRows")
        systemsRows.resize(580, 50) 
        self.horizontalLayout = QtWidgets.QHBoxLayout(systemsRows)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setContentsMargins(0,0,0,0)
        self.systemColumnRow = QtWidgets.QFrame(systemsRows)
        self.systemColumnRow.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.systemColumnRow.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.systemColumnRow.setFixedSize(575,50)
        self.systemColumnRow.setLineWidth(0)
        self.systemColumnRow.setObjectName("systemColumnRow")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.systemColumnRow)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout.setContentsMargins(0,0,0,0)
        self.systemlabel = QtWidgets.QLabel(self.systemColumnRow)
        self.systemlabel.setObjectName("systemlabel")
        self.systemlabel.setMinimumSize(200,20)
        self.systemlabel.setAlignment(Qt.AlignLeft)


        self.horizontalLayout_2.addWidget(self.systemlabel)

        spacerItem = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.deleteButton = QtWidgets.QPushButton(self.systemColumnRow)
        self.deleteButton.setText("Delete")
        self.deleteButton.setObjectName("deleteButton")
        self.deleteButton.setMinimumSize(35,25)
        self.horizontalLayout_2.addWidget(self.deleteButton)
        spacerItem4 = QtWidgets.QSpacerItem(0, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem4)
        self.ProvidesCheckBox = QtWidgets.QCheckBox(self.systemColumnRow)
        self.ProvidesCheckBox.setText("")
        self.ProvidesCheckBox.setObjectName("ProvidesCheckBox")
        self.horizontalLayout_2.addWidget(self.ProvidesCheckBox)
        spacerItem1 = QtWidgets.QSpacerItem(90, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.requiresCheckBox = QtWidgets.QCheckBox(self.systemColumnRow)
        self.requiresCheckBox.setText("")
        self.requiresCheckBox.setObjectName("requiresCheckBox")
        self.horizontalLayout_2.addWidget(self.requiresCheckBox)
        spacerItem2 = QtWidgets.QSpacerItem(70, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.turnOffCheckBox = QtWidgets.QCheckBox(self.systemColumnRow)
        self.turnOffCheckBox.setText("")
        self.turnOffCheckBox.setObjectName("turnOffCheckBox")
        self.horizontalLayout_2.addWidget(self.turnOffCheckBox)

        spacerItem3 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.horizontalLayout.addWidget(self.systemColumnRow)

        self.retranslateUi(systemsRows)
        QtCore.QMetaObject.connectSlotsByName(systemsRows)

    def retranslateUi(self, systemsRows):
        _translate = QtCore.QCoreApplication.translate
        systemsRows.setWindowTitle(_translate("systemsRows", "Form"))
        self.systemlabel.setText(_translate("systemsRows", "<html><head/><body><p align=\"center\"><span style=\" font-size:9pt;\">Systems</span></p></body></html>"))


#if __name__ == "__main__":
    #import sys
    #app = QtWidgets.QApplication(sys.argv)
    #systemsRows = QtWidgets.QWidget()
    #ui = Ui_systemsRows()
    #ui.setupUi(systemsRows)
    #systemsRows.show()
    #sys.exit(app.exec_())
