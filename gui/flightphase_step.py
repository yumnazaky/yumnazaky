# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'flightphase_step.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import sys
import json
import math
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog
from systems_dialog import Ui_DialogSystem
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import pyqtSignal
from comments_dialog import Ui_comments_dialog
from rationale_dialog import Ui_Rationale_Dialog
from systems_dialog import Ui_DialogSystem




class Ui_FlightPhaseStep(QtWidgets.QWidget):  # Inherit from QWidget or QDialog

    

     

  
        

    def setupUi(self, FlightPhaseStep):
        FlightPhaseStep.setObjectName("FlightPhaseStep")
        FlightPhaseStep.setFixedSize(1500, 250)
        FlightPhaseStep.setAutoFillBackground(False)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(FlightPhaseStep)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0,0,0,0)
        self.procedureStep_widget = QtWidgets.QWidget(FlightPhaseStep)
        self.procedureStep_widget.setStyleSheet("\n"
"background-color: rgb(165, 165, 165) \n"
"")
        self.procedureStep_widget.setObjectName("procedureStep_widget")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.procedureStep_widget)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(5,5,5,5)
        self.procedureStep_buttons = QtWidgets.QWidget(self.procedureStep_widget)
        self.procedureStep_buttons.setStyleSheet("background-color: rgb(245, 245, 245);\n"
"QWidget *widget = new QWidget();\n"
"widget->setStyleSheet(\"border: 2px solid rgb(165, 165, 165);\");\n"
"")
        self.procedureStep_buttons.setObjectName("procedureStep_buttons")
        self.procedureStep_buttons.setFixedSize(120,195)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.procedureStep_buttons)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0,3,0,0)
        self.verticalLayout_5.setSpacing(0)
        self.procedureStep_order = QtWidgets.QLineEdit(self.procedureStep_buttons)
        self.procedureStep_order.setObjectName("procedureStep_order")
        self.procedureStep_order.setMaximumSize(50,50)
        self.procedureStep_order.setReadOnly(True)
        self.verticalLayout_5.addWidget(self.procedureStep_order)
        self.horizontalContainer = QtWidgets.QWidget(self.procedureStep_buttons)
        self.horizontalContainer.setObjectName("horizontalContainer")
        self.horizontalContainer.setMinimumSize(120,60)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalContainer)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0,0,0,0)
        self.horizontalLayout_2.setSpacing(25)

        self.upDownContainer = QtWidgets.QWidget(self.horizontalContainer)
        self.upDownContainer.setObjectName("upDownContainer")
        self.upDownContainer.setMinimumSize(60,60)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.upDownContainer)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0,0,0,0)
        self.verticalLayout_3.setSpacing(0)
        self.up_procedureStep = QtWidgets.QToolButton(self.upDownContainer)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("C:/Users/yumna/project11/semester_thesis/src/gui/resources/icon_images/up_blue.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.up_procedureStep.setIcon(icon)
        self.up_procedureStep.setIconSize(QtCore.QSize(25, 25))
        self.up_procedureStep.setStyleSheet("""
    background-color: rgb(255, 255, 255); /* White background */
    
""")
        self.up_procedureStep.setObjectName("up_procedureStep")
        self.verticalLayout_3.addWidget(self.up_procedureStep)
        self.down_procedureStep = QtWidgets.QToolButton(self.upDownContainer)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("C:/Users/yumna/project11/semester_thesis/src/gui/resources/icon_images/down_blue.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.down_procedureStep.setIcon(icon1)
        self.down_procedureStep.setIconSize(QtCore.QSize(25, 25))
        self.down_procedureStep.setObjectName("down_procedureStep")
        self.down_procedureStep.setStyleSheet("""
    background-color: rgb(255, 255, 255); /* White background */
   
""")
        self.verticalLayout_3.addWidget(self.down_procedureStep)
        self.horizontalLayout_2.addWidget(self.upDownContainer)
       
        self.trashChangeContainer = QtWidgets.QWidget(self.horizontalContainer)
        self.trashChangeContainer.setObjectName("trashChangeContainer")
        self.trashChangeContainer.setMinimumSize(60,60)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.trashChangeContainer)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.delete_procedureStep = QtWidgets.QToolButton(self.trashChangeContainer)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("C:/Users/yumna/project11/semester_thesis/src/gui/resources/icon_images/trash_blue.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.delete_procedureStep.setIcon(icon2)
        self.delete_procedureStep.setIconSize(QtCore.QSize(25, 25))
        self.delete_procedureStep.setStyleSheet("""
    background-color: rgb(255, 255, 255); /* White background */
   
""")

        self.delete_procedureStep.setObjectName("delete_procedureStep")
        

        self.verticalLayout_6.addWidget(self.delete_procedureStep)
        self.changeLog = QtWidgets.QToolButton(self.trashChangeContainer)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("C:/Users/yumna/project11/semester_thesis/src/gui/resources/icon_images/change_log.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.changeLog.setIcon(icon3)
        self.changeLog.setIconSize(QtCore.QSize(25, 25))
        self.changeLog.setObjectName("changeLog")
        self.changeLog.setStyleSheet("""
    background-color: rgb(255, 255, 255); /* White background */
   
""")

        self.verticalLayout_6.addWidget(self.changeLog)
        self.horizontalLayout_2.addWidget(self.trashChangeContainer)
        self.verticalLayout_5.addWidget(self.horizontalContainer)
        self.saveCancelContainer = QtWidgets.QWidget(self.procedureStep_buttons)
        self.saveCancelContainer.setObjectName("saveCancelContainer")
        self.saveCancelContainer.setMinimumSize(120,30)
        self.saveCancelContainer.setContentsMargins(0,0,0,0)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.saveCancelContainer)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.saveChanges = QtWidgets.QToolButton(self.saveCancelContainer)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("C:/Users/yumna/project11/semester_thesis/src/gui/resources/icon_images/check_mark.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.saveChanges.setIcon(icon4)
        self.saveChanges.setIconSize(QtCore.QSize(25, 25))
        self.saveChanges.setGeometry(0,0,25,25)
        self.saveChanges.setStyleSheet("""
    background-color: rgb(255, 255, 255); /* White background */
   
""")

        self.saveChanges.setObjectName("saveChanges")
        
        self.horizontalLayout_3.addWidget(self.saveChanges)
        self.horizontalLayout_3.setContentsMargins(0,0,0,0)
        self.horizontalLayout_3.setSpacing(50)
        self.caancel_changes = QtWidgets.QToolButton(self.saveCancelContainer)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("C:/Users/yumna/project11/semester_thesis/src/gui/resources/icon_images/cross.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.caancel_changes.setIcon(icon5)
        self.caancel_changes.setIconSize(QtCore.QSize(25, 25))
        self.caancel_changes.setObjectName("caancel_changes")
        
        self.caancel_changes.setStyleSheet("""
    background-color: rgb(255, 255, 255); /* White background */
   
""")

        self.horizontalLayout_3.addWidget(self.caancel_changes)
        
        self.verticalLayout_5.addWidget(self.saveCancelContainer)
        self.horizontalLayout_4.addWidget(self.procedureStep_buttons)
        self.tableContainer = QtWidgets.QWidget(self.procedureStep_widget)
        self.tableContainer.setObjectName("tableContainer")
        self.tableContainer.setMaximumSize(1200,250)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.tableContainer)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(0,0,0,0)
        self.procedureStep_header = QtWidgets.QWidget(self.tableContainer)
        self.procedureStep_header.setStyleSheet("background: rgb(52, 152, 219)")
        self.procedureStep_header.setObjectName("procedureStep_header")
        self.procedureStep_header.setMaximumSize(1200,50)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.procedureStep_header)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0,0,0,2)
        self.object_header = QtWidgets.QTextEdit(self.procedureStep_header)
        self.object_header.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.object_header.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.object_header.setReadOnly(True)
        
        self.object_header.setObjectName("object_header")
        self.horizontalLayout_5.addWidget(self.object_header)
        self.action_header = QtWidgets.QTextEdit(self.procedureStep_header)
        self.action_header.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.action_header.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.action_header.setReadOnly(True)
        self.action_header.setObjectName("action_header")
        self.horizontalLayout_5.addWidget(self.action_header)
        self.executedBy_header = QtWidgets.QTextEdit(self.procedureStep_header)
        self.executedBy_header.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.executedBy_header.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.executedBy_header.setReadOnly(True)
        self.executedBy_header.setObjectName("executedBy_header")
        self.horizontalLayout_5.addWidget(self.executedBy_header)
        self.physicalFeatures_header = QtWidgets.QTextEdit(self.procedureStep_header)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.physicalFeatures_header.sizePolicy().hasHeightForWidth())
        self.physicalFeatures_header.setSizePolicy(sizePolicy)
        self.physicalFeatures_header.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.physicalFeatures_header.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.physicalFeatures_header.setReadOnly(True)
        self.physicalFeatures_header.setObjectName("physicalFeatures_header")
        self.horizontalLayout_5.addWidget(self.physicalFeatures_header)
        self.outputParameter_header = QtWidgets.QTextEdit(self.procedureStep_header)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.outputParameter_header.sizePolicy().hasHeightForWidth())
        #self.inputStates_header = QtWidgets.QTextEdit(self.procedureStep_header)
        #self.inputStates_header.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        #self.inputStates_header.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        #self.inputStates_header.setReadOnly(True)
        #self.inputStates_header.setObjectName("inputStates_header")
        #self.horizontalLayout_5.addWidget(self.inputStates_header)
        self.outputParameter_header.setSizePolicy(sizePolicy)
        self.outputParameter_header.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.outputParameter_header.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.outputParameter_header.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.outputParameter_header.setReadOnly(True)
        self.outputParameter_header.setObjectName("outputParameter_header")
        self.horizontalLayout_5.addWidget(self.outputParameter_header)
        self.outputParameter_header_2 = QtWidgets.QTextEdit(self.procedureStep_header)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.outputParameter_header_2.sizePolicy().hasHeightForWidth())
        self.outputParameter_header_2.setSizePolicy(sizePolicy)
        self.outputParameter_header_2.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.outputParameter_header_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.outputParameter_header_2.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.outputParameter_header_2.setReadOnly(True)
        self.outputParameter_header_2.setObjectName("outputParameter_header_2")
        self.horizontalLayout_5.addWidget(self.outputParameter_header_2)
        self.verticalLayout.addWidget(self.procedureStep_header)
        self.widget = QtWidgets.QWidget(self.tableContainer)
        self.widget.setObjectName("widget")
        self.widget.setMaximumSize(1200,200)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setContentsMargins(0,0,0,0)
        self.object_plainTextEdit = QtWidgets.QPlainTextEdit(self.widget)
        self.object_plainTextEdit.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.object_plainTextEdit.setObjectName("object_plainTextEdit")
        self.horizontalLayout.addWidget(self.object_plainTextEdit)
        self.action_plainTextEdit = QtWidgets.QPlainTextEdit(self.widget)
        self.action_plainTextEdit.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.action_plainTextEdit.setObjectName("action_plainTextEdit")
        self.horizontalLayout.addWidget(self.action_plainTextEdit)
        self.executedBy_plainTextEdit = QtWidgets.QPlainTextEdit(self.widget)
        self.executedBy_plainTextEdit.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.executedBy_plainTextEdit.setObjectName("executedBy_plainTextEdit")
        self.horizontalLayout.addWidget(self.executedBy_plainTextEdit)
        # Replace executedBy_plainTextEdit with a container for two QPlainTextEdit widgets
        self.physicalFeaturesContainer = QtWidgets.QWidget(self.widget)
        self.physicalFeaturesContainer.setObjectName("physicalFeaturesContainer")
        self.physicalFeaturesContainer.setFixedSize(200, 200)  # Adjust the size as per your need
        self.physicalFeaturesContainer.setStyleSheet("background-color: rgb(165, 165, 165);")
        self.physicalFeaturesLayout = QtWidgets.QVBoxLayout(self.physicalFeaturesContainer)
        self.physicalFeaturesLayout.setObjectName("physicalFeaturesLayout")
        self.physicalFeaturesLayout.setContentsMargins(0, 0, 0, 0)
        
        self.physicalFeaturesContainer.setContentsMargins(0, 0, 0, 0)
        
        # Create two small QPlainTextEdit widgets
        self.physicalFeatures_param = QtWidgets.QPlainTextEdit(self.physicalFeaturesContainer)
        self.physicalFeatures_param.setObjectName("physicalFeatures_param")
        self.physicalFeatures_param.setStyleSheet("background-color: rgb(255 255, 255);")
        self.physicalFeatures_param.setFixedSize(200, 40)  
        #self.physicalFeatures_param.setText("Duration")  
        self.physicalFeatures_param.setStyleSheet("""
    background-color: rgb(255, 255, 255);  /* White background */
    font-weight: bold;  /* Make the text bold */
    font-size: 17px;
    color: rgb(52, 152, 219);  /* Adjust font size */
""")# Adjust the size as per your need
        #self.physicalFeatures_param.setAlignment(QtCore.Qt.AlignCenter)
         

        self.physicalFeatures_value = QtWidgets.QPlainTextEdit(self.physicalFeaturesContainer)
        self.physicalFeatures_value.setObjectName("physicalFeatures_value")
        self.physicalFeatures_value.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.physicalFeatures_value.setFixedSize(200, 160)  # Adjust the size as per your need
        self.physicalFeaturesLayout.setSpacing(2)
        self.physicalFeaturesLayout.addWidget(self.physicalFeatures_value, alignment=Qt.AlignTop)
        # Add the two QPlainTextEdit widgets to the horizontal layout
        self.physicalFeaturesLayout.addWidget(self.physicalFeatures_param)
        self.physicalFeaturesLayout.addWidget(self.physicalFeatures_value)
        #self.physicalFeaturesLayout.setAlignment(Qt.AlignTop)
        
        # Finally, add the entire container (with the horizontal layout) to the main horizontal layout
        self.horizontalLayout.addWidget(self.physicalFeaturesContainer)

        self.horizontalLayout_4.addWidget(self.tableContainer)
        #self.horizontalLayout.addWidget(self.executedBy_plainTextEdit)
        #self.inputStates_listWidget = QtWidgets.QListWidget(self.widget)


        #self.inputStates_listWidget.setStyleSheet("background-color: rgb(255, 255, 255);")
        #self.inputStates_listWidget.setObjectName("inputStates_listWidget")
        #self.horizontalLayout.addWidget(self.inputStates_listWidget)
        self.output_plainTextEdit = QtWidgets.QPlainTextEdit(self.widget)
        self.output_plainTextEdit.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.output_plainTextEdit.setReadOnly(False)
        self.output_plainTextEdit.setObjectName("output_plainTextEdit")
        self.horizontalLayout.addWidget(self.output_plainTextEdit)
        self.rationaleCommentsBox = QtWidgets.QFrame(self.widget)
        self.rationaleCommentsBox.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.rationaleCommentsBox.setFrameShape(QtWidgets.QFrame.Panel)
        self.rationaleCommentsBox.setFrameShadow(QtWidgets.QFrame.Raised)
        self.rationaleCommentsBox.setObjectName("rationaleCommentsBox")
        self.rationaleCommentsBox.setFixedSize(190,200)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.rationaleCommentsBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.rationale_button = QtWidgets.QPushButton(self.rationaleCommentsBox)
        self.rationale_button.setStyleSheet("background-color: rgb(52, 152, 219);\n"
"\n"
"color: rgb(255, 255, 255);\n"
"")
        self.rationale_button.setObjectName("rationale_button")
        self.verticalLayout_2.addWidget(self.rationale_button)
        self.comments_button = QtWidgets.QPushButton(self.rationaleCommentsBox)
        self.comments_button.setStyleSheet("background-color: rgb(52, 152, 219);\n"
"color: rgb(255, 255, 255);\n"
"")
        self.comments_button.setObjectName("comments_button")
        self.verticalLayout_2.addWidget(self.comments_button)
        self.horizontalLayout.addWidget(self.rationaleCommentsBox)
        self.verticalLayout.addWidget(self.widget)
        self.horizontalLayout_4.addWidget(self.tableContainer)
        self.systemContainer = QtWidgets.QWidget(self.procedureStep_widget)
        self.systemContainer.setStyleSheet("background-color: rgb(165, 165, 165);")
        self.systemContainer.setObjectName("systemContainer")
        self.systemContainer.setMinimumSize(130,100)
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.systemContainer)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.systems_pushButton = QtWidgets.QPushButton(self.systemContainer)
        self.systems_pushButton.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color:  rgb(52, 152, 219);")
        self.systems_pushButton.setObjectName("systems_pushButton")

        

        self.systems_pushButton.setMinimumSize(50,30)
        self.verticalLayout_7.addWidget(self.systems_pushButton)
        
        self.verticalLayout_4.addWidget(self.procedureStep_widget)
        
        # Create the add checkpoint button in red
        self.addCheckpoint_pushButton = QtWidgets.QPushButton(self.systemContainer)
        self.addCheckpoint_pushButton.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                            "color: rgb(231, 76, 60);")  # Red text
        self.addCheckpoint_pushButton.setObjectName("addCheckpoint_pushButton")
        self.addCheckpoint_pushButton.setMaximumSize(180, 30)
        self.addCheckpoint_pushButton.setText("Add Checkpoint")  # Set text for the button

        # Add the add checkpoint button to the layout
        self.verticalLayout_7.addWidget(self.addCheckpoint_pushButton)
        self.horizontalLayout_4.addWidget(self.systemContainer)
        # Add the systemContainer to the horizontal layout
        #self.horizontalLayout_4.addWidget(self.systemContainer)

        
        

        self.retranslateUi(FlightPhaseStep)
        QtCore.QMetaObject.connectSlotsByName(FlightPhaseStep)

   
    

    def retranslateUi(self,FlightPhaseStep):
        _translate = QtCore.QCoreApplication.translate
        #Form.setWindowTitle(_translate("Form", "Form"))
        self.up_procedureStep.setText(_translate("Form", "..."))
        self.down_procedureStep.setText(_translate("Form", "..."))
        self.delete_procedureStep.setText(_translate("Form", "..."))
        self.changeLog.setText(_translate("Form", "..."))
        self.saveChanges.setText(_translate("Form", "..."))
        self.caancel_changes.setText(_translate("Form", "..."))
        self.object_header.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600; color:#ffffff;\">Object</span></p></body></html>"))
        self.action_header.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600; color:#ffffff;\">Action</span></p></body></html>"))
        self.executedBy_header.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600; color:#ffffff;\">Executed By</span></p></body></html>"))
        self.physicalFeatures_header.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600; color:#ffffff;\">Physical Features</span></p></body></html>"))
        self.outputParameter_header.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600; color:#ffffff;\">Output Parameters</span></p></body></html>"))
        self.outputParameter_header_2.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600; color:#ffffff;\">Additional Information</span></p></body></html>"))
        self.rationale_button.setText(_translate("Form", "Rationale"))
        self.comments_button.setText(_translate("Form", "Comments"))
        #self.inputStates_header.setHtml(_translate("Form", "<p align=\"center\" style=\"font-weight:600; color:#ffffff;\">Input States</p>"))
        self.systems_pushButton.setText(_translate("Form", "Systems"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    FlightPhaseStep = QtWidgets.QWidget()  # Create the main widget instance
    ui = Ui_FlightPhaseStep()  # Create an instance of the UI class
    ui.setupUi(FlightPhaseStep)  # Set up the UI on the widget
    FlightPhaseStep.show()  # Show the widget with all the elements
    sys.exit(app.exec_())  # Start the event loop
