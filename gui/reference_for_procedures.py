import os
import json
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPdfWriter, QPainter
from PyQt5.QtWidgets import QFileDialog


class Ui_DialogReferencesProcedure(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setFixedSize(500, 400)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        
        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setContentsMargins(5, 0, 5, 0)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_2.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.lineEdit_2.setReadOnly(True)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setFixedSize(440, 40)
        self.horizontalLayout.addWidget(self.lineEdit_2)
        
        self.toolButton_13 = QtWidgets.QToolButton(self.widget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("C:/Users/yumna/project11/semester_thesis/src/gui/resources/icon_images/download_bluee.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButton_13.setIcon(icon)
        self.toolButton_13.setFixedSize(40, 40)
        self.toolButton_13.setObjectName("toolButton_13")
        self.toolButton_13.clicked.connect(self.generate_pdf)  # Connect button to PDF generation
        self.horizontalLayout.addWidget(self.toolButton_13)
        self.verticalLayout_2.addWidget(self.widget)
        
        self.widget_6 = QtWidgets.QWidget(Dialog)
        self.widget_6.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.widget_6.setObjectName("widget_6")
        self.widget_6.setMinimumSize(450, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget_6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)

        
        self.textEdit_10 = QtWidgets.QTextEdit(self.widget_6)
        self.textEdit_10.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.textEdit_10.setObjectName("textEdit_10")
        self.verticalLayout.addWidget(self.textEdit_10)
        self.verticalLayout_2.addWidget(self.widget_6)
        
        self.widget_2 = QtWidgets.QWidget(Dialog)
        self.widget_2.setObjectName("widget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        
        self.pushButton_5 = QtWidgets.QPushButton(self.widget_2)
        self.pushButton_5.setStyleSheet("color: rgb(52, 152, 219)")
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.clicked.connect(self.save_text_to_file)  # Connect button to save function
        self.horizontalLayout_2.addWidget(self.pushButton_5)
        
        self.pushButton_6 = QtWidgets.QPushButton(self.widget_2)
        self.pushButton_6.setStyleSheet("color: rgb(184, 56, 31);")
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_6.clicked.connect(Dialog.reject)  # Close the dialog on button click
        self.horizontalLayout_2.addWidget(self.pushButton_6)
        self.verticalLayout_2.addWidget(self.widget_2)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        # Initialize the file path to save the data
        self.file_path = "procedure_references_data.json"
        self.load_saved_text()  # Load saved data when the dialog is opened

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.lineEdit_2.setText(_translate("Dialog", "References for Procedure"))
        self.toolButton_13.setText(_translate("Dialog", "..."))
        self.pushButton_5.setText(_translate("Dialog", "Save"))
        self.pushButton_6.setText(_translate("Dialog", "Cancel"))

    def generate_pdf(self):
        """Generate a PDF with the content from lineEdit_2."""
        # Open a dialog to save the PDF
        file_path, _ = QFileDialog.getSaveFileName(None, "Save PDF", "", "PDF Files (*.pdf);;All Files (*)")
        
        if file_path:
            # Create a QPdfWriter object
            pdf_writer = QPdfWriter(file_path)
            pdf_writer.setPageSize(QtGui.QPageSize.A4)
            pdf_writer.setResolution(300)
            
            # Create a QPainter to write the text
            painter = QPainter(pdf_writer)
            
            # Set font for PDF
            painter.setFont(QtGui.QFont("Arial", 12))
            
            # Write the text from lineEdit_2
            painter.drawText(100, 100, "References for Procedure:")
            painter.drawText(100, 150, self.lineEdit_2.text())
            
            # End the painter and save the PDF
            painter.end()
            print(f"PDF saved to: {file_path}")

    def save_text_to_file(self):
        """Save the text from lineEdit_2 and textEdit_10 to a JSON file."""
        data = {
            "line_edit_text": self.lineEdit_2.text(),
            "text_edit_text": self.textEdit_10.toPlainText()
        }
        with open(self.file_path, 'w') as file:
            json.dump(data, file)
        print(f"Text saved to {self.file_path}")

    def load_saved_text(self):
        """Load the saved text from the JSON file, if it exists."""
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as file:
                data = json.load(file)
                self.lineEdit_2.setText(data.get("line_edit_text", ""))
                self.textEdit_10.setText(data.get("text_edit_text", ""))
                print(f"Text loaded from {self.file_path}")
        else:
            print("No saved text found")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_DialogReferencesProcedure()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
