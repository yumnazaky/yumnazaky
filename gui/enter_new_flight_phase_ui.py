# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'enter_new_flight_phase.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import sys
from PyQt5 import QtCore, QtGui, QtWidgets


from PyQt5 import QtCore, QtWidgets
import sys

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 350)

        # Create the main vertical layout for the dialog
        self.mainLayout = QtWidgets.QVBoxLayout(Dialog)

        # Enter New Phase Label and LineEdit
        self.enter_new_phase_label = QtWidgets.QLabel(Dialog)
        self.enter_new_phase_label.setText("Enter New Flight Phase:")
        self.enter_new_phase_label.setMaximumSize(QtCore.QSize(400, 30))

        self.enter_new_phase_lineEdit = QtWidgets.QLineEdit(Dialog)
        self.enter_new_phase_lineEdit.setMaximumSize(QtCore.QSize(400, 30))

        # Add to the layout
        self.mainLayout.addWidget(self.enter_new_phase_label)
        self.mainLayout.addWidget(self.enter_new_phase_lineEdit)

        # Associated Procedure Label and LineEdit
        #self.associated_procedure_label = QtWidgets.QLabel(Dialog)
        #self.associated_procedure_label.setText("<b>Enter Associated Procedure:</b>")
        
        #self.associated_procedure_label.setMaximumSize(QtCore.QSize(400, 30))

        #self.associated_procedure_lineEdit = QtWidgets.QLineEdit(Dialog)
        #self.associated_procedure_lineEdit.setMaximumSize(QtCore.QSize(400, 30))

        # Add to the layout
        #self.mainLayout.addWidget(self.associated_procedure_label)
        #self.mainLayout.addWidget(self.associated_procedure_lineEdit)

        # Corresponding Operation Label and ComboBox
        self.corresponding_operation_label = QtWidgets.QLabel(Dialog)
        self.corresponding_operation_label.setText("Corresponding Operation:")
        self.corresponding_operation_label.setMaximumSize(QtCore.QSize(400, 30))

        self.corresponding_operation_comboBox = QtWidgets.QComboBox(Dialog)
        self.corresponding_operation_comboBox.setMaximumSize(QtCore.QSize(400, 30))

        # Add to the layout
        self.mainLayout.addWidget(self.corresponding_operation_label)
        self.mainLayout.addWidget(self.corresponding_operation_comboBox)

        # Position Label and ComboBox
        self.position_label = QtWidgets.QLabel(Dialog)
        self.position_label.setText("Position:")
        self.position_label.setMaximumSize(QtCore.QSize(400, 30))

        self.position_comboBox = QtWidgets.QComboBox(Dialog)
        self.position_comboBox.setMaximumSize(QtCore.QSize(400, 30))

        # Add to the layout
        self.mainLayout.addWidget(self.position_label)
        self.mainLayout.addWidget(self.position_comboBox)

        # Dialog Button Box for Ok/Cancel
        self.enter_new_phase_buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.enter_new_phase_buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.enter_new_phase_buttonBox.setMaximumSize(QtCore.QSize(400, 40))

        # Add to the layout
        self.mainLayout.addWidget(self.enter_new_phase_buttonBox)

        # Connect the buttons to accept/reject actions
        self.enter_new_phase_buttonBox.accepted.connect(Dialog.accept)
        self.enter_new_phase_buttonBox.rejected.connect(Dialog.reject)

        QtCore.QMetaObject.connectSlotsByName(Dialog)




        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.enter_new_phase_label.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-weight:600;\">Enter New Flight Phase:</span></p></body></html>"))
        self.position_label.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-weight:600;\">Position</span></p></body></html>"))
        self.corresponding_operation_label.setText(_translate("Dialog", "<html><head/><body><p><span style=\" font-weight:600;\">Corresponding Operation </span></p></body></html>"))