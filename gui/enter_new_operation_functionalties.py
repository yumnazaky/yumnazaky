
import sys, os
import traceback
import math
import json 
import sqlite3, sqlalchemy
from sqlalchemy.orm import subqueryload
from sqlalchemy.orm import sessionmaker
# get the current directory
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# get the directory of GUI (which is in a sibling folder)
module_path = os.path.join(current_dir, "modules")
GUI_path = os.path.join(current_dir, "gui")
# add GUI path to the system path
sys.path.append(GUI_path)
# add GUI path to the system path
sys.path.append(module_path)

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QDialog, QVBoxLayout, QLabel
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
from update_databases import update_lists
from define_object_classes import TypeOfOperationObject
from Database1 import Database, TypeOfOperation
from enter_new_operation_dialog_ui import Ui_New_operation_type

class NewOperationTypeDialog(QDialog, Ui_New_operation_type):
    operation_added = pyqtSignal()  # Create a custom signal

    def __init__(self, parent=None):
        super(NewOperationTypeDialog, self).__init__(parent)
        self.setupUi(self)
        self.new_operation_buttonBox.accepted.connect(self.on_accept)

    def on_accept(self):
        # Get the new operation name from the input field
        new_operation = self.enter_new_operation_lineEdit.text().strip()

        if new_operation:
            try:
                # Step 1: Save the operation to the in-memory list
                operation_id = len(self.parent().type_of_operation_list) + 1  # Assuming unique ID generation
                new_operation_obj = TypeOfOperationObject(
                    ID=operation_id,
                    TypeOfOperation=new_operation,
                    TypeOfMission="",  # Default empty values for other fields
                    References="",
                    Comments=""
                )
                self.parent().type_of_operation_list.append(new_operation_obj)  # Update in-memory list

                # Step 2: Save the operation to the database
                #session = Database.get_session()  # Assuming you have a Database session management
                #session.add(new_operation_obj)
                #session.commit()

                # Step 3: Emit the signal to notify the main window to update its UI
                self.operation_added.emit()

                # Step 4: Close the dialog after successful addition
                self.accept()

            except Exception as e:
                #session.rollback()
                QtWidgets.QMessageBox.critical(self, "Error", f"Failed to save operation to the database: {e}")

            finally:
                session.close()

        else:
            QtWidgets.QMessageBox.warning(self, "Warning", "Please enter a valid operation type.")