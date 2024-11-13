# Ensure this block is included at the top of your script
import sys
import os
import json

# get the SRC directory
# get the SRC directory
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# get the directory of GUI (which is in a sibling folder)
DB_path = os.path.join(current_dir, "databases1")
# add GUI path to the system path
sys.path.append(DB_path)
# get the current directory
GUI_path = os.path.join(current_dir, "gui")
module_path = os.path.join(current_dir,"modules")# add GUI path to the system path
sys.path.append(GUI_path) 
sys.path.append(module_path)

# Now try importing


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QDialog, QMessageBox
from type_of_operation import Ui_TypeOfOperationDialog
from define_object_classes import ProcedureStepObject, TypeOfOperationObject, PhaseObject 
from Database1 import Database as Db
from Database1 import TypeOfOperation 
from PyQt5.QtCore import pyqtSignal  # Ensure pyqtSignal is imported

class TypeOfOperationDialog(QDialog, Ui_TypeOfOperationDialog):
    change_signal_delete = pyqtSignal()
    database_selected = pyqtSignal(str)
    databases_dir = os.path.join(os.path.dirname(__file__), "databases1") 
    def __init__(self, PSI, parent=None):
        super(TypeOfOperationDialog, self).__init__(parent)
        self.setupUi(self)
        os.makedirs(self.databases_dir, exist_ok=True)
        self.fill_operation_combobox(DB_path)

        # Connect buttons to corresponding slots
        self.select_operation.clicked.connect(self.load_db)
        self.select_operation_2.clicked.connect(self.new_db)
        self.selectMission.clicked.connect(self.save_mission)

    def fill_operation_combobox(self, folder_path):
        files = os.listdir(folder_path)
        db_files = [file for file in files if file.endswith(".db")]
        db_files = [file[:-3] for file in db_files]  # Strip .db extension
        self.operation_select.addItems(db_files)

    def load_db(self):
        if self.operation_select.currentIndex() != -1:
            db_name = self.operation_select.currentText() + ".db"
            Db.modify_db_config(db_name)
            self.database_selected.emit(db_name)
            self.accept()  # Close with accepted status
        else:
            self.operation_select.setStyleSheet("border: 1px solid red;")

    def new_db(self):
        db_name = self.operation_enter.text()
        if db_name:
            db_name = db_name + ".db"
            DB_path = os.path.join(self.databases_dir, db_name)  # Define DB_path correctly here
            Db.modify_db_config(db_name)
            if not os.path.exists(DB_path):  # Use DB_path instead of db_path
                Db.create_new_database(db_name)  # Ensure database creation with structure
                Db.modify_db_config(db_name)  # Apply new database config
                self.accept()  # Close with accepted status
            else:
                QtWidgets.QMessageBox.warning(self, "Error", f"Database '{db_name}' already exists.")
        else:
            self.operation_enter.setStyleSheet("border: 1px solid red;")
    def save_mission(self):
        """
        Saves the text from missionLineEdit into a TypeOfOperationObject instance.
        """
        # Get the mission text from the line edit
        mission_text = self.missionLineEdit.text().strip() or ""  # Default to an empty string if no input
        
        # Create a new TypeOfOperationObject or update an existing one
        new_operation = TypeOfOperationObject(TypeOfMission=mission_text)
        
        # Add it to the list if this is a new operation
        TypeOfOperationObject.type_of_operation_list.append(new_operation)
        print(f"Mission '{mission_text}' saved to TypeOfOperationObject.")      
