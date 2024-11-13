# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'enter_procedure.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_newProcedure(object):
    def setupUi(self, newProcedure):
        newProcedure.setObjectName("newProcedure")
        newProcedure.resize(500, 300)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(newProcedure)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.Procedurewidget = QtWidgets.QWidget(newProcedure)
        self.Procedurewidget.setMaximumSize(500,300)
        self.Procedurewidget.setObjectName("Procedurewidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.Procedurewidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(0,0,0,0)
        self.title = QtWidgets.QLabel(self.Procedurewidget)
        self.title.setObjectName("title")
        self.verticalLayout.addWidget(self.title)
        self.selectOperationTypeBox = QtWidgets.QWidget(self.Procedurewidget)
        self.selectOperationTypeBox.setObjectName("selectOperationTypeBox")

        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.selectOperationTypeBox)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0,0,0,0)
        self.label_2 = QtWidgets.QLabel(self.selectOperationTypeBox)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.operationComboBox = QtWidgets.QComboBox(self.selectOperationTypeBox)

        self.operationComboBox.setObjectName("operationComboBox")
        self.operationComboBox.setMaximumSize(250,30)
        self.horizontalLayout_3.addWidget(self.operationComboBox)
        self.verticalLayout.addWidget(self.selectOperationTypeBox)
        self.selectFlightPhaseBox = QtWidgets.QWidget(self.Procedurewidget)
        self.selectFlightPhaseBox.setObjectName("selectFlightPhaseBox")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.selectFlightPhaseBox)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_3 = QtWidgets.QLabel(self.selectFlightPhaseBox)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.phaseComboBox = QtWidgets.QComboBox(self.selectFlightPhaseBox)
        self.phaseComboBox.setEditable(False)
        self.phaseComboBox.setCurrentText("")
        self.phaseComboBox.setObjectName("phaseComboBox")
        self.phaseComboBox.setMaximumSize(250,30)
        self.horizontalLayout_2.addWidget(self.phaseComboBox)
        self.horizontalLayout_2.setContentsMargins(0,0,0,0)
        self.verticalLayout.addWidget(self.selectFlightPhaseBox)
        self.enterProcedureBox = QtWidgets.QWidget(self.Procedurewidget)
        self.enterProcedureBox.setObjectName("enterProcedureBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.enterProcedureBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setContentsMargins(0,0,0,0)
        self.enterProcedureLabel = QtWidgets.QLabel(self.enterProcedureBox)
        self.enterProcedureLabel.setObjectName("enterProcedureLabel")
        self.horizontalLayout.addWidget(self.enterProcedureLabel)
        self.procedurelineEdit = QtWidgets.QLineEdit(self.enterProcedureBox)
        self.procedurelineEdit.setMaximumSize(300,35)
        self.procedurelineEdit.setObjectName("procedurelineEdit")
        self.horizontalLayout.addWidget(self.procedurelineEdit)
        self.verticalLayout.addWidget(self.enterProcedureBox)
        self.procedurebuttonBox = QtWidgets.QDialogButtonBox(self.Procedurewidget)
        self.procedurebuttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.procedurebuttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.procedurebuttonBox.setObjectName("procedurebuttonBox")
        self.verticalLayout.addWidget(self.procedurebuttonBox)
        self.verticalLayout_2.addWidget(self.Procedurewidget)

        self.retranslateUi(newProcedure)
        self.phaseComboBox.setCurrentIndex(-1)
        #self.procedurebuttonBox.accepted.connect(newProcedure.accept) # type: ignore
        #self.procedurebuttonBox.rejected.connect(newProcedure.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(newProcedure)

    def retranslateUi(self, newProcedure):
        _translate = QtCore.QCoreApplication.translate
        newProcedure.setWindowTitle(_translate("newProcedure", "Dialog"))
        self.title.setText(_translate("newProcedure", "<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">Enter Procedure</span></p></body></html>"))
        self.label_2.setText(_translate("newProcedure", "<html><head/><body><p><span style=\" font-size:9pt; font-weight:600;\">Select type of operation</span></p></body></html>"))
        self.label_3.setText(_translate("newProcedure", "<html><head/><body><p><span style=\" font-size:9pt; font-weight:600;\">Select flight phase</span></p></body></html>"))
        self.enterProcedureLabel.setText(_translate("newProcedure", "<html><head/><body><p><span style=\" font-size:9pt; font-weight:600;\">Enter Procedure</span></p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    newProcedure = QtWidgets.QDialog()
    ui = Ui_newProcedure()
    ui.setupUi(newProcedure)
    newProcedure.show()
    sys.exit(app.exec_())