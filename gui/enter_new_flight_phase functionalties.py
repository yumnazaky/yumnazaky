import sys
import os
import traceback
import math
import json
import sqlite3, sqlalchemy
from PyQt5 import QtWidgets, QtCore

from PyQt5.QtWidgets import QDialog, QMessageBox
from PyQt5.QtCore import pyqtSignal
# get the current directory
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(os.path.dirname(__file__), "config.ini")
# get the directory of GUI (which is in a sibling folder)
modules_path = os.path.join(current_dir, "modules")
# add GUI path to the system path
sys.path.append(modules_path)

from define_object_classes import PhaseObject, TypeOfOperationObject, ProcedureObject  # Assuming these are the object classes
from enter_new_flight_phase_ui import Ui_Dialog  # UI file for this dialog
from update_databases import update_lists  # For updating in-memory lists
from Database1 import Database as Db  # Database interaction handled here
from Database1 import Phase as DbPhaseEdition


class EnterNewPhaseDialog(QDialog, Ui_Dialog):
    valid_flag = bool  # Flag to check the validity of inputs
    phase_id = math.nan
    #type_of_operation_id = math.nan
    type_of_operation_list = []
    phase_list = []
    procedure_list=[]
    change_signal_phase_dialog = pyqtSignal()  # Signal to notify changes
    update = str

    def __init__(self, parent=None):
        super(EnterNewPhaseDialog, self).__init__(parent)
        self.setupUi(self)
        self.setModal(True)  
        self.update_local_lists()
        self.fillOperationComboBox()
        self.valid_flag = False

        self.enter_new_phase_buttonBox.accepted.connect(self.on_accept_button_clicked)
        self.enter_new_phase_lineEdit.textChanged.connect(self.activateComboBoxes)
        self.corresponding_operation_comboBox.currentIndexChanged.connect(self.fillPhasePositionComboBox)

    def activateComboBoxes(self):
        self.position_comboBox.setEnabled(True)
        self.corresponding_operation_comboBox.setEnabled(True)
        self.fillOperationComboBox()

    def fillOperationComboBox(self):
        """Fills the operation combo box with data from type_of_operation_list."""
        self.corresponding_operation_comboBox.clear()
        for operation in self.type_of_operation_list:
            self.corresponding_operation_comboBox.addItem(operation.type_of_operation, operation.id)
        self.corresponding_operation_comboBox.setCurrentIndex(-1)

    def fillPhasePositionComboBox(self):
        self.position_comboBox.clear()
        self.position_comboBox.addItem("1. Position", 0)
        list = [
            obj
            for obj in self.phase_list
            if obj.type_of_operation_id
            == self.corresponding_operation_comboBox.itemData(self.corresponding_operation_comboBox.currentIndex())
        ]  # Sucht alle Procedures aus dem State heraus
        sorted_list = sorted(list, key=lambda x: x.order_number)
        for phase in sorted_list:
            self.position_comboBox.addItem(phase.name, phase.id)
           
        self.position_comboBox.setCurrentIndex(
            -1
        )

    def check_validity(self):
        """Validates the input fields."""
        if (
            self.enter_new_phase_lineEdit.text() != ""
            and self.corresponding_operation_comboBox.currentIndex() != -1
            and self.position_comboBox.currentIndex() != -1
        ):
            return True
        else:
            return False

    def on_accept_button_clicked(self):
        """Handles the 'OK' button click event."""
        valid_flag = self.check_validity()
        if valid_flag:
            phase_name = self.enter_new_phase_lineEdit.text().strip()
            procedure_name = self.associated_procedure_lineEdit.text().strip()

            if not procedure_name:
                QtWidgets.QMessageBox.warning(self, "Error", "Please enter an associated procedure name.")
                return

            type_of_operation_id = self.corresponding_operation_comboBox.itemData(self.corresponding_operation_comboBox.currentIndex())
            phase_id = self.position_comboBox.itemData(self.position_comboBox.currentIndex())

            if phase_id == 0:
                order_number = 1
            else:
                phase = PhaseObject.return_phase(phase_id)
                order_number = phase.order_number + 1

        # Start a session and handle all operations in one transaction
            session = Database.get_session()
            try:
            # Create new phase
                new_phase = PhaseObject.new_entry(phase_name, order_number, "", "", [], type_of_operation_id, session=session)
                new_phase_id = new_phase.id

            # Create new procedure linked to the phase
                new_procedure = ProcedureObject.new_entry(
                    name=procedure_name,
                    input_state="",
                    output_state="",
                    procedure_step_list=[],
                    references_procedure=f"Procedure for Phase {phase_name} in Type of Operation ID {type_of_operation_id}",
                    comments_procedure="",
                    phase_id=new_phase_id,
                    session=session  # Use the same session
                )

                ProcedureStepObject.new_entry(
                    order_step=0,  # First step
                    procedure_id=new_procedure.id,  # The procedure ID
                    description="Initial procedure step",  # Description of the step
                    session=session  # Use the same session
                )

                session.commit()  # Commit once, after all operations
                self.change_signal_phase_dialog.emit()
                self.accept()

            except Exception as e:
                session.rollback()  # Roll back all operations if any fail
                QtWidgets.QMessageBox.critical(self, "Error", f"Failed to save phase and procedure: {e}")
            finally:
                session.close()
        else:
            QtWidgets.QMessageBox.warning(self, "Invalid Input", "Please ensure all required fields are filled.")


    def save_phase_data(self):
        """Handles saving phase data and linking it to the selected operation."""
     # Get the user-entered phase name
        phase_name = self.enter_new_phase_lineEdit.text().strip()
    
     # Get the selected operation from the corresponding_operation_comboBox
        selected_operation_id = self.corresponding_operation_comboBox.currentData()  # Assuming the operation ID is stored in item data

     # Check if a phase name was entered
        if not phase_name:
            QtWidgets.QMessageBox.warning(None, "Error", "Please enter a phase name.")
            return

    # Start a session to interact with the database
        session = Database.get_session()

        try:
        # Create and save the new Phase
            new_phase = Phase(
                name=phase_name,
                order_number=self.get_next_order_number(selected_operation_id),  # Get the next order number for the phase
                input_state="",   # Default input state or can be set later
                output_state="",  # Default output state or can be set later
                procedure_list=[],  # Empty initially, procedures can be added later
                type_of_operation_id=selected_operation_id  # Link to the selected operation
            )
            session.add(new_phase)
            session.commit()

            QtWidgets.QMessageBox.information(None, "Success", "Phase has been added successfully.")

        except Exception as e:
            session.rollback()
            QtWidgets.QMessageBox.critical(None, "Error", f"An error occurred while saving the phase: {e}")
        finally:
            session.close()

    def get_next_order_number(self, operation_id):
        """Gets the next available order number for a phase under a given operation."""
        session = Database.get_session()
        try:
        # Query the phases for the given operation and return the highest order number + 1
            highest_order = session.query(Phase).filter_by(type_of_operation_id=operation_id).order_by(Phase.order_number.desc()).first()
            if highest_order:
                return highest_order.order_number + 1
            else:
                return 1  # If no phases exist, start with order number 1
        finally:
            session.close()


    def update_local_lists(self):
        
        self.type_of_operation_list = []
        self.phase_list = []
        #self.procedure_list =[]

        (   
            self.item_list,
            self.phase_list,
            self.type_of_operation_list,
            self.system_state_list,
            self.checkpoint_list,
            self.procedure_list,
            self.procedure_step_list,
        ) = update_lists()

    def accept(self):
        """Checks validity and closes the dialog if valid."""
        valid_flag = self.check_validity()
        if valid_flag:
            super().accept()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dialog = EnterNewPhaseDialog()
    dialog.show()
    sys.exit(app.exec_())
