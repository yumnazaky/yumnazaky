import sys, os
import traceback
import math

# get the current directory
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# get the directory of GUI (which is in a sibling folder)
GUI_path = os.path.join(current_dir, "gui")
# add GUI path to the system path
sys.path.append(GUI_path)





import sys
import os
import json
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QDialog, QMessageBox
from modules.update_databases import update_lists
from define_object_classes import PhaseObject, TypeOfOperationObject  # Assuming these are the object classes
from enter_new_flight_phase_ui import Ui_Dialog  # Assuming you have a UI file for this dialog
from Databases1 import Database as Db  # Assuming Database interaction is handled by this class

class Db:
    @staticmethod
    def save_phase(phase_name, type_of_operation_id, order_number):
        """Example database save operation for phase (needs proper implementation)."""
        print(f"Saving phase: {phase_name}, Operation ID: {type_of_operation_id}, Order: {order_number}")
        # Add your database save logic here

class EnterNewPhaseDialog(QDialog, Ui_EnterNewPhaseDialog):
    phase_selected_signal = QtCore.pyqtSignal(str)
    phases_file = "phases.json"  # File to store phases persistently

    def __init__(self, parent=None):
        super(EnterNewPhaseDialog, self).__init__(parent)
        self.setupUi(self)

        # Load existing phases and operation types from files or database
        self.phases = self.load_phases()
        self.operation_types = TypeOfOperationObject.type_of_operation_list  # Assuming it's already populated

        # Fill the combo boxes with operation types and existing phases
        self.fill_operation_combobox()
        self.fill_phase_position_combobox()

        # Connect buttons to corresponding slots
        self.select_phase_button.clicked.connect(self.load_phase)
        self.enter_new_phase_button.clicked.connect(self.enter_new_phase)

    def load_phases(self):
        """Load phases from a file."""
        if os.path.exists(self.phases_file):
            with open(self.phases_file, "r") as file:
                return json.load(file)
        else:
            return []

    def fill_operation_combobox(self):
        """Fills the combo box with operation types from TypeOfOperationObject."""
        self.corresponding_operation_comboBox.clear()
        for operation in self.operation_types:
            self.corresponding_operation_comboBox.addItem(operation.type_of_operation, operation.id)
        self.corresponding_operation_comboBox.setCurrentIndex(-1)

    def fill_phase_position_combobox(self):
        """Fills the phase position combo box with existing phases."""
        self.position_comboBox.clear()
        self.position_comboBox.addItem("First Position", 0)  # Default first position

        # Sort and add existing phases to the combo box
        sorted_phases = sorted(self.phases, key=lambda x: x.get("order_number", 0))
        for phase in sorted_phases:
            self.position_comboBox.addItem(phase["name"], phase["id"])
        self.position_comboBox.setCurrentIndex(-1)

    def save_phase(self, phase_name, type_of_operation_id, order_number):
        """Save new phase to file and update JSON."""
        new_phase = {"name": phase_name, "type_of_operation_id": type_of_operation_id, "order_number": order_number}

        # Add the new phase to the phases list
        self.phases.append(new_phase)

        # Save the updated phases list to the JSON file
        with open(self.phases_file, "w") as file:
            json.dump(self.phases, file)

        # Update the database
        Db.save_phase(phase_name, type_of_operation_id, order_number)

        # Re-populate the combo boxes
        self.fill_phase_position_combobox()

    def load_phase(self):
        """Loads the selected phase and operation."""
        if self.corresponding_operation_comboBox.currentIndex() != -1:
            phase_name = self.position_comboBox.currentText()
            operation_type_id = self.corresponding_operation_comboBox.itemData(self.corresponding_operation_comboBox.currentIndex())

            # Save the phase and operation details to the database
            Db.save_phase(phase_name, operation_type_id, order_number=1)

            # Emit signal and open the flight flow window (for later navigation)
            self.phase_selected_signal.emit(phase_name)
            self.open_flight_flow_window()
        else:
            self.corresponding_operation_comboBox.setStyleSheet("border: 1px solid red;")

    def enter_new_phase(self):
        """Handles custom user input for a new phase."""
        new_phase_name = self.enter_new_phase_lineEdit.text()
        operation_type_id = self.corresponding_operation_comboBox.itemData(self.corresponding_operation_comboBox.currentIndex())

        if new_phase_name == "":
            self.enter_new_phase_lineEdit.setStyleSheet("border: 1px solid red;")
            return

        # Determine the order number for the new phase
        if self.position_comboBox.currentIndex() == 0:
            order_number = 1
        else:
            last_phase_id = self.position_comboBox.itemData(self.position_comboBox.currentIndex())
            last_phase = PhaseObject.return_phase(last_phase_id)
            order_number = last_phase.order_number + 1 if last_phase else 1

        # Save the new phase in the combo box and file
        self.save_phase(new_phase_name, operation_type_id, order_number)

        # Save the new phase to the database
        Db.save_phase(new_phase_name, operation_type_id, order_number)

        # Emit signal and open the flight flow window
        self.phase_selected_signal.emit(new_phase_name)
        self.open_flight_flow_window()

    def open_flight_flow_window(self):
        """Opens the main flight flow window."""
        QMessageBox.information(self, "Flight Flow", "Opening Flight Flow Main Window.")
        self.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dialog = EnterNewPhaseDialog()
    dialog.show()
    sys.exit(app.exec_())