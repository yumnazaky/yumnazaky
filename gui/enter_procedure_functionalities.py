
import sys, os
import traceback
import math

# get the current directory
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# get the directory of GUI (which is in a sibling folder)
modules_path = os.path.join(current_dir, "modules")
# add GUI path to the system path
sys.path.append(modules_path)

from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore, QtGui, QtWidgets
from enter_procedure import Ui_newProcedure
from define_object_classes import TypeOfOperationObject, ProcedureObject, PhaseObject, ProcedureStepObject
from Database1 import TypeOfOperation, Procedure, Phase, Database 
from update_databases import update_lists

class newProcedure(QDialog, Ui_newProcedure):
    valid_flag = bool  # Flag to check the validity of inputs
    procedure_id = math.nan
    type_of_operation_list = []
    phase_list = []
    procedure_list = []
    change_signal_phase_dialog = pyqtSignal()  # Signal to notify changes
    update = str

    def __init__(self, parent=None):
        super(newProcedure, self).__init__(parent)
        self.setupUi(self)
        self.setModal(True)
        self.update_local_lists()
        self.populate_operation_combo()  # Populate operation combo first
        self.valid_flag = False

        # Connect combo boxes
        self.operationComboBox.currentIndexChanged.connect(self.populate_phase_combo)
        self.procedurebuttonBox.accepted.connect(self.validate_procedure_data)  # OK button
        self.procedurebuttonBox.rejected.connect(self.reject)  # Cancel button


        self.populate_phase_combo()

    def activateComboBoxes(self):
        self.operationComboBox.setEnabled(True)
        self.phaseComboBox.setEnabled(True)
        self.populate_phase_combo()
        self.populate_operation_combo()

    def populate_operation_combo(self):
        """Populate the operation combo box with all operations."""
        self.operationComboBox.clear()
        print("hena")

        for operation in self.type_of_operation_list:
            self.operationComboBox.addItem(operation.type_of_operation, operation.id)

    def populate_phase_combo(self):
        """Populate the phase combo box based on the selected operation."""
        self.phaseComboBox.clear()
        selected_type_of_operation_id = self.operationComboBox.currentData()
    
        if selected_type_of_operation_id is None:
            return

        phase_list = [phase for phase in self.phase_list if phase.type_of_operation_id == selected_type_of_operation_id]
        # Populate the combo box with the retrieved phases
        for phase in phase_list:
            self.phaseComboBox.addItem(phase.name, phase.id)

    def save_procedure_data(self):
        """Save the new procedure to the database and update relevant lists."""
        # Get the user-entered procedure name
        procedure_name = self.procedurelineEdit.text().strip()

        # Get the selected phase ID from the combo box
        selected_phase_id = self.phaseComboBox.currentData()

        # Validate input fields
        if not procedure_name or selected_phase_id is None:
            #QtWidgets.QMessageBox.warning(None, "Error", "Please enter all fields correctly.")
            return

        # Start the database session
        #session = Database.get_session()

        try:
            # Create the new Procedure object
            #new_procedure = Procedure(
                #name=procedure_name,
                #input_state="",  # You can modify these as per your workflow
                #output_state="",
                #procedure_step_list=[],  # Empty initially
                #references_procedure="",
                #comments_procedure="",
                #phase_id=selected_phase_id  # Link the procedure to the selected phase
            #)
            new_procedure = ProcedureObject.new_entry(
                Name=procedure_name,
                InputState="",  # You can modify these as per your workflow
                OutputState="",
                ProcedureStepList=[],  # Empty initially
                ReferencesProcedure="",
                CommentsProcedure="",
                PhaseID=selected_phase_id  # Link the procedure to the selected phase
            )


            # Add the new procedure to the database
            #session.add(new_procedure)
            #session.commit()
            if new_procedure:
                self.procedure_list.append(new_procedure)
            # Notify the user that the procedure was successfully saved
            #QtWidgets.QMessageBox.information(None, "Success", "Procedure has been added successfully.")
                self.update_local_lists()
                self.valid_flag = True 

        except Exception as e:
            print(f"Error saving procedure: {e}")
            #session.rollback()
            #QtWidgets.QMessageBox.critical(None, "Error", f"An error occurred while saving the procedure: {e}")

        #finally:
            #session.close()
    def validate_procedure_data(self):
        # Get values from input fields
        procedure_name = self.procedurelineEdit.text().strip()
        selected_phase_id = self.phaseComboBox.currentData()

        # Check if all required fields are filled
        if procedure_name and selected_phase_id:
            self.valid_flag = True 
            self.save_procedure_data() # Valid inputs
            self.accept()  # Close the dialog as accepted
        else:
            #QtWidgets.QMessageBox.warning(self, "Invalid Input", "Please fill in all required fields.")
            self.valid_flag = False
            return         

    def update_local_lists(self):
        self.type_of_operation_list = TypeOfOperationObject.type_of_operation_list
        self.phase_list = PhaseObject.phase_list
        self.procedure_list = ProcedureObject.procedure_list
        self.procedure_step_list =ProcedureStepObject.procedure_step_list
        (
            self.item_list,
            self.procedure_list,
            self.procedure_step_list,
            self.type_of_operation_list,
            self.system_state_list,
            self.phase_list,
            self.checkpoint_list,
        ) = update_lists()

#if __name__ == "__main__":
    #import sys
    #app = QtWidgets.QApplication(sys.argv)
    #newProcedure = QtWidgets.QDialog()
    #ui = Ui_newProcedure()
    #ui.setupUi(newProcedure)
   # newProcedure.show()
    #sys.exit(app.exec_())