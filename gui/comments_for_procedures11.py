import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPdfWriter, QPainter
from PyQt5.QtWidgets import QFileDialog
import json

class Ui_DialogProceduresComments(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setFixedSize(500, 400)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        
        self.widget_2 = QtWidgets.QWidget(Dialog)
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(5, 0, 5, 0)

        self.lineEdit = QtWidgets.QLineEdit(self.widget_2)
        self.lineEdit.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit.setReadOnly(True)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setFixedSize(440, 40)
        self.horizontalLayout_2.addWidget(self.lineEdit)

        self.toolButton_6 = QtWidgets.QToolButton(self.widget_2)
        self.toolButton_6.setFixedSize(40, 40)
        self.toolButton_6.setStyleSheet("background-color: rgb(255, 255, 255);")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("C:/Users/yumna/project11/semester_thesis/src/gui/resources/icon_images/download_bluee.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_6.setIcon(icon)
        self.toolButton_6.setObjectName("toolButton_6")
        self.horizontalLayout_2.addWidget(self.toolButton_6)
        self.verticalLayout_2.addWidget(self.widget_2)

        self.widget_5 = QtWidgets.QWidget(Dialog)
        self.widget_5.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.widget_5.setObjectName("widget_5")
        self.widget_5.setMinimumSize(450, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget_5)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)

        self.textEdit_9 = QtWidgets.QTextEdit(self.widget_5)
        self.textEdit_9.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.textEdit_9.setObjectName("textEdit_9")
        self.verticalLayout.addWidget(self.textEdit_9)
        self.verticalLayout_2.addWidget(self.widget_5)

        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.pushButton_3 = QtWidgets.QPushButton(self.widget)
        self.pushButton_3.setStyleSheet("\n"
            "background-color: rgb(255, 255, 255);color: rgb(52, 152, 219)")
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout.addWidget(self.pushButton_3)

        self.pushButton_4 = QtWidgets.QPushButton(self.widget)
        self.pushButton_4.setStyleSheet("background-color: rgb(255, 255, 255);\n"
            "color: rgb(184, 56, 31);")
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout.addWidget(self.pushButton_4)
        self.verticalLayout_2.addWidget(self.widget)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        # Set the path for saving and loading the file
        self.file_path = "saved_data.json"

        # Connect button click to PDF generation function
        self.toolButton_6.clicked.connect(self.generate_pdf)
        
        # Connect button click to save functionality
        self.pushButton_3.clicked.connect(self.save_text_to_file)
        
        # Connect pushButton_4 to close the dialog
        self.pushButton_4.clicked.connect(Dialog.reject)

        # Load the saved text when the dialog is opened
        self.load_saved_text()

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.lineEdit.setText(_translate("Dialog", "Comments for Procedure"))
        self.toolButton_6.setText(_translate("Dialog", "..."))
        self.pushButton_3.setText(_translate("Dialog", "Save"))
        self.pushButton_4.setText(_translate("Dialog", "Cancel"))

    def generate_pdf(self):
        # Open a dialog to save the file
        file_path, _ = QFileDialog.getSaveFileName(None, "Save PDF", "", "PDF Files (*.pdf);;All Files (*)")

        if file_path:
            # Create a QPdfWriter object
            pdf_writer = QPdfWriter(file_path)
            pdf_writer.setPageSize(QtGui.QPageSize.A4)
            pdf_writer.setResolution(300)

            # Create a QPainter to write text
            painter = QPainter(pdf_writer)

            # Set font for PDF
            painter.setFont(QtGui.QFont("Arial", 12))

            # Write text from lineEdit and textEdit to the PDF
            painter.drawText(100, 100, "Comments for Procedure:")
            painter.drawText(100, 150, self.lineEdit.text())

            # Write the content of textEdit_9
            painter.drawText(100, 200, "Details:")
            painter.drawText(100, 250, self.textEdit_9.toPlainText())

            # End the painter and save the PDF
            painter.end()

            print("PDF saved to:", file_path)

    def save_text_to_file(self):
        """Save the text from lineEdit and textEdit_9 to a JSON file."""
        data = {
            "line_edit_text": self.lineEdit.text(),
            "text_edit_text": self.textEdit_9.toPlainText()
        }
        with open(self.file_path, 'w') as file:
            json.dump(data, file)

        print(f"Text saved to {self.file_path}")

    def load_saved_text(self):
        """Load the saved text from the JSON file, if it exists."""
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                data = json.load(file)
                self.lineEdit.setText(data.get("line_edit_text", ""))
                self.textEdit_9.setText(data.get("text_edit_text", ""))
                print(f"Text loaded from {self.file_path}")
        else:
            print("No saved text found")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_DialogProceduresComments()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
