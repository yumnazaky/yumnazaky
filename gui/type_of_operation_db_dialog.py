# Ensure this block is included at the top of your script
import sys
import os
import json

# get the SRC directory
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add 'modules' folder to the system path
modules_path = os.path.join(current_dir, "modules")
sys.path.append(modules_path)

# Now try importing


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QDialog, QMessageBox
from type_of_operation import Ui_TypeOfOperationDialog
from define_object_classes import ProcedureStepObject, TypeOfOperationObject, PhaseObject 
from Database1 import Database as Db
from Database1 import TypeOfOperation 


class Db:
    @staticmethod
    def save_operation(operation_type, mission_type, session=None):
        """Example database save operation with session management."""
        if session is None:
            session = Database.get_session()
        try:
            # Perform the save operation
            print(f"Saving operation: {operation_type}, Mission: {mission_type}")
            # Add your database logic here
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()


class TypeOfOperationDialog(QDialog, Ui_TypeOfOperationDialog):
    operation_selected_signal = pyqtSignal(str)
    operations_file = "operations.json"  # File to store operations persistently

    def __init__(self, parent=None):
        super(TypeOfOperationDialog, self).__init__(parent)
        self.setupUi(self)

        # Load operations from file (persistent storage)
        self.operations = self.load_operations()

        # Fill combo box with predefined and saved operation types
        self.fill_operation_combobox()

        # Connect buttons to corresponding slots
        self.select_operation.clicked.connect(self.load_operation)
        self.select_operation_2.clicked.connect(self.enter_new_operation)

    def load_operations(self):
        """Load operations from a file."""
        if os.path.exists(self.operations_file):
            with open(self.operations_file, "r") as file:
                return json.load(file)
        else:
            return ["Normal Procedures", "Abnormal and Emergency Procedures"]

    def fill_operation_combobox(self):
        """Fills the combo box with predefined operation types."""
        self.operation_select.clear()  # Clear existing items
        self.operation_select.addItems(self.operations)

    def save_operations(self, operation_type):
        """Save new operation to file, update JSON, and database."""
       # Add the new operation type to the operations list (if not already present)
        if operation_type not in self.operations:
            self.operations.append(operation_type)

           # Save the updated operations list to the JSON file
            with open(self.operations_file, "w") as file:
                json.dump(self.operations, file)

         # Save the operation type to the database
            mission_type = self.missionLineEdit.text() or "Not provided"
            Db.save_operation(operation_type, mission_type)

         # **Call update_lists() to refresh the in-memory state**
            updated_lists = update_lists()

         # Extract updated type of operation list
            self.operations = [op.TypeOfOperation for op in updated_lists[3]]  # index 3 corresponds to type_of_operation_list

         # Re-populate the combo box with updated values
            self.fill_operation_combobox()


    def load_operation(self):
        """Loads the selected operation and opens the flight flow window."""
        if self.operation_select.currentIndex() != -1:
            operation_type = self.operation_select.currentText()
            mission_type = self.missionLineEdit.text() or "Not provided"

            Db.save_operation(operation_type, mission_type)

            # Emit signal and open the flight flow window
            self.operation_selected_signal.emit(operation_type)
            self.open_flight_flow_window()
        else:
            self.operation_select.setStyleSheet("border: 1px solid red;")

    def enter_new_operation(self):
        """Handles custom user input for a new operation type and opens the flight flow window."""
        new_operation_type = self.operation_enter.text()
        mission_type = self.missionLineEdit.text() or "Not provided"

        if new_operation_type == "":
            self.operation_enter.setStyleSheet("border: 1px solid red;")
            return

        # Save the new operation type in the combo box and file
        self.save_operations(new_operation_type)

        # Save the new operation type in the database
        Db.save_operation(new_operation_type, mission_type)

        # Emit signal and open the flight flow window
        self.operation_selected_signal.emit(new_operation_type)
        self.open_flight_flow_window()

    def open_flight_flow_window(self):
        """Opens the main flight flow window."""
        QMessageBox.information(self, "Flight Flow", "Opening Flight Flow Main Window.")
        self.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dialog = TypeOfOperationDialog()
    dialog.show()
    sys.exit(app.exec_())
