import sys
import os
import traceback
import math
import json
import sqlite3, sqlalchemy
from PyQt5 import QtWidgets, QtCore

from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import pyqtSignal

# Get the current directory and paths
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(os.path.dirname(__file__), "config.ini")
modules_path = os.path.join(current_dir, "modules")
GUI_path = os.path.join(current_dir, "gui")
sys.path.append(modules_path)
sys.path.append(GUI_path)

from define_object_classes import PhaseObject, TypeOfOperationObject, ProcedureObject  # Assuming these are the object classes
from enter_new_flight_phase_ui import Ui_Dialog  # UI file for this dialog
from update_databases import update_lists  # For updating in-memory lists
from Database1 import Database, TypeOfOperation, Procedure, Phase


class EnterNewPhaseDialog(QDialog, Ui_Dialog):
    change_signal_phase_dialog = pyqtSignal()  # Signal to notify changes

    def __init__(self, parent=None):
        super(EnterNewPhaseDialog, self).__init__(parent)
        self.setupUi(self)
        self.setModal(True)  
        self.valid_flag = False
        self.phase_id = math.nan
        self.type_of_operation_id = math.nan
        self.type_of_operation_list = []
        self.phase_list = []
        self.procedure_list = []

        # Populate operation and phase lists
        self.update_operation_lists()
        self.fillOperationComboBox()

        # Connect signals and slots
        self.enter_new_phase_buttonBox.accepted.connect(self.on_accept_button_clicked)
        self.enter_new_phase_lineEdit.textChanged.connect(self.activateComboBoxes)
        self.corresponding_operation_comboBox.currentIndexChanged.connect(self.fillPhasePositionComboBox)

    def activateComboBoxes(self):
        """Enable and populate the combo boxes when input is detected."""
        self.position_comboBox.setEnabled(True)
        self.corresponding_operation_comboBox.setEnabled(True)
        self.fillOperationComboBox()
        self.fillPhasePositionComboBox()

    def fillOperationComboBox(self):
        """Fills the operation combo box with data from type_of_operation_list."""
        self.corresponding_operation_comboBox.clear()
        if not self.type_of_operation_list:
            print("No operations found.")
            return

        for operation in self.type_of_operation_list:
            self.corresponding_operation_comboBox.addItem(operation.type_of_operation, operation.id)

        self.corresponding_operation_comboBox.setCurrentIndex(0)  # Select the first operation by default

    def fillPhasePositionComboBox(self):
        """Fills the position combo box with phases for the selected operation."""
        self.position_comboBox.clear()
        self.position_comboBox.addItem("1. Position", 0)

        if not self.phase_list:
            print("Phase list is empty.")
            return

        index = self.corresponding_operation_comboBox.currentIndex()
        if index == -1:
            return  # Invalid index, no operation selected

        phases = self.type_of_operation_list[index].phase_list

        sorted_phases = sorted(phases, key=lambda x: x.order_number)
        for phase in sorted_phases:
            self.position_comboBox.addItem(phase.name, phase.id)

        self.position_comboBox.setCurrentIndex(0)

    def check_validity(self):
        """Checks if all required fields are filled."""
        return (
            self.enter_new_phase_lineEdit.text().strip() != "" and
            self.corresponding_operation_comboBox.currentIndex() != -1 and
            self.position_comboBox.currentIndex() != -1
        )

    def on_accept_button_clicked(self):
        """Handles the 'OK' button click event."""
        if not self.check_validity():
            QMessageBox.warning(self, "Invalid Input", "Please ensure all required fields are filled.")
            return

        phase_name = self.enter_new_phase_lineEdit.text().strip()
        type_of_operation_id = self.corresponding_operation_comboBox.itemData(self.corresponding_operation_comboBox.currentIndex())
        phase_id = self.position_comboBox.itemData(self.position_comboBox.currentIndex())

        # Calculate the order number for the new phase
        if phase_id == 0:
            order_number = 1
        else:
            phase = next((p for p in self.phase_list if p.id == phase_id), None)
            order_number = phase.order_number + 1 if phase else 1

        # Create a new phase
        new_phase = PhaseObject.new_entry(
            Name=phase_name,
            OrderNumber=order_number,
            InputState="",
            OutputState="",
            ProcedureList=[],
            TypeOfOperationID=type_of_operation_id
        )
        
        if new_phase:
            self.phase_list.append(new_phase)
            print(f"Created Phase: {new_phase}")

        self.change_signal_phase_dialog.emit()
        self.accept()

    def save_phase_data(self):
        """Handles saving phase data and linking it to the selected operation."""
        phase_name = self.enter_new_phase_lineEdit.text().strip()
        selected_operation_id = self.corresponding_operation_comboBox.currentData()

        if not phase_name:
            QMessageBox.warning(self, "Error", "Please enter a phase name.")
            return

        order_number = self.get_next_order_number(selected_operation_id)

        new_phase = PhaseObject.new_entry(
            Name=phase_name,
            OrderNumber=order_number,
            InputState="",
            OutputState="",
            ProcedureList=[],
            TypeOfOperationID=selected_operation_id
        )

        self.phase_list.append(new_phase)
       # QMessageBox.information(self, "Success", "Phase has been added successfully.")

    def get_next_order_number(self, operation_id):
        """Gets the next available order number for a phase under a given operation."""
        phases_for_operation = [phase for phase in self.phase_list if phase.type_of_operation_id == operation_id]
        return max(phase.order_number for phase in phases_for_operation) + 1 if phases_for_operation else 1

    def update_operation_lists(self):
        """Updates the in-memory lists of operations, phases, and procedures."""
        self.type_of_operation_list = TypeOfOperationObject.type_of_operation_list
        self.phase_list = PhaseObject.phase_list
        self.procedure_list = ProcedureObject.procedure_list
        print(f"Operation List: {self.type_of_operation_list}")
        print(f"Phase List: {self.phase_list}")

    def accept(self):
        """Checks validity and closes the dialog if valid."""
        if self.check_validity():
            super().accept()


#if __name__ == "__main__":
    #app = QtWidgets.QApplication(sys.argv)
    #dialog = EnterNewPhaseDialog()
    #dialog.show()
    #sys.exit(app.exec_())
