import sys, os
import traceback
import math
import json 
import sqlite3, sqlalchemy
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
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt

from update_databases import update_lists
from flightphase_step import Ui_FlightPhaseStep
from define_object_classes import ItemObject, ProcedureStepObject, CheckpointObject
from Database1 import SystemState as DbSystemStateEdition 
from comments_dialog import Ui_comments_dialog
from rationale_dialog import Ui_Rationale_Dialog
from set_input_req_dialog11 import Ui_setInputReqDialog
from system_functionalties_2 import DialogSystem

class FlightPhaseStep(QtWidgets.QWidget):
    procedure_step_id = math.nan
    phase_id = math.nan
    item_id = math.nan
    # Signal indicating that a change occurred in the Procedure Step Widget
    change_signal_step = QtCore.pyqtSignal() 

    def __init__(self, parent=None):
        super(FlightPhaseStep, self).__init__(parent)
        self.setupUi(self)
        self.step = ProcedureStepObject.return_procedure_step(self.procedure_step_id)
        self.item = ItemObject.return_item(self.item_id)
        self.addCheckpoint_pushButton.clicked.connect(self.add_checkpoint_widget)
        self.procedureStep_order.textChanged.connect(self.enable_save_dismiss_buttons)
        self.object_plainTextEditt.textChanged.connect(self.enable_save_dismiss_buttons)
        self.action_plainTextEdit.textChanged.connect(self.enable_save_dismiss_buttons)
        self.output_plainTextEdit.textChanged.connect(self.enable_save_dismiss_buttons)
        self.executedBy_plainTextEdit.textChanged.connect(self.enable_save_dismiss_buttons)
        self.physicalFeatures_value.textChanged.connect(self.enable_save_dismiss_buttons)
          # Connect the test_function to one of the buttons
        
        
        self.comments_button.clicked.connect(self.open_comments_dialog)
        self.rationale_button.clicked.connect(self.open_rationale_dialog)
        self.systems_pushButton.clicked.connect(self.open_system_dialog)
        self.saveChanges.clicked.connect(self.save_step)
        self.caancel_changes.clicked.connect(self.undo_step)  # Assuming this undoes the step
        self.changeLog.clicked.connect(self.open_change_history_dialog)
        self.procedureStep_order.setPlainText(str(self.step.order_step))
        # Store the initial values of the widgets (for undo purposes)
    def get_initial_values(self):
        return {
            "order_step": self.step.order_step,
            "object_name": self.step.object_name,
            "action": self.step.action,
            "executed_by": self.step.executed_by,
            "required_input_state": self.step.required_input_state,
            "output_state": self.step.output_state,
            "physical_features": self.step.physical_features,
            "rationale": self.step.rationale,
            "comments": self.step.comments
        }
        

    def enable_save_cancel_buttons(self):
        self.saveChanges.setEnabled(True)
        self.caancel_changes.setEnabled(True)

    def disable_save_cancel_buttons(self):
        self.saveChanges.setEnabled(False)
        self.caancel_changes.setEnabled(False)
    def add_checkpoint_widget(self):
        """Dynamically add a checkpoint widget below the current step."""
        checkpoint_widget = SetInputReqWidget(self)
        self.verticalLayout_4.addWidget(checkpoint_widget)    
    

    
       

    def save_step(self):
        new_data = self.get_current_step_data()
        print("Save button clicked")
        #new_data = {
            #"object_name": self.object_plainTextEdit.toPlainText(),
            #"order_step": self.procedureStep_order.toPlainText(),
            #"action": self.action_plainTextEdit.toPlainText(),
            #"executed_by": self.executedBy_plainTextEdit.toPlainText(),
            #"required_input_state": self.RequiredInputStateText.toPlainText(),
            #"output_state": self.output_plainTextEdit.toPlainText(),
            #"physical_features": self.physicalFeatures_value.toPlainText()
        #}
        if not self.validate_step_data(new_data):
            QtWidgets.QMessageBox.warning(self, "Invalid Input", "Please fill in all required fields before saving.")
            return
        # Save to the ProcedureStepObject (this updates the database and in-memory list)
        ProcedureStepObject.edit_procedure_step(
            self.procedure_step_id,
            **new_data  # Pass the new data
        )
        self.update_in_memory_procedure_step(new_data)
        checkpoint_data = self.get_checkpoint()
        self.create_or_update_checkpoint(checkpoint_data)
        # Update the in-memory list (procedure_step_list) with new data
        #for step in ProcedureStepObject.procedure_step_list:
            #if step.id == self.procedure_step_id:
               #step.update(new_data)  # Assuming ProcedureStepObject has an `update()` method
               #break 
        # Save to the in-memory procedure step list
        #self.update_in_memory_procedure_step(self.procedure_step_id, new_data)

        # Link to Checkpoint (Create a checkpoint for the procedure step)
        #checkpoint_data = {
            #"name": f"Checkpoint for Step {self.step.order_step}",
            #"item_state": new_data["output_state"],
            #"person_state": new_data["executed_by"],
            #"procedure_step_id": self.procedure_step_id
        #}

        # Create or update checkpoint in database and memory
        #self.create_or_update_checkpoint(checkpoint_data)

        # Save the data to a JSON file as well
        #with open("procedure_step_data.json", "w") as json_file:
            #json.dump(new_data, json_file, indent=4)
        #self.update_initial_values()
        self.disable_save_cancel_buttons()
        self.change_signal_step.emit()
    def get_current_step_data(self):
        """Retrieve the current step data from the UI."""
        return {
            "object_name": self.object_plainTextEdit.toPlainText(),
            "order_step": self.procedureStep_order.toPlainText(),
            "action": self.action_plainTextEdit.toPlainText(),
            "executed_by": self.executedBy_plainTextEdit.toPlainText(),
            "required_input_state": self.RequiredInputStateText.toPlainText(),
            "output_state": self.output_plainTextEdit.toPlainText(),
            "physical_features": self.physicalFeatures_value.toPlainText()
        }


    def get_checkpoint_data(self):
        """Prepare checkpoint data for the current step."""
        return {
            "name": f"Checkpoint for Step {self.step.order_step}",
            "item_state": self.output_plainTextEdit.toPlainText(),
            "person_state": self.executedBy_plainTextEdit.toPlainText(),
            "procedure_step_id": self.procedure_step_id
        }    
    def validate_step_data(self, step_data):
        """Validate that all required step fields are filled."""
        required_fields = ["object_name", "action", "executed_by", "output_state"]
        return all(step_data.get(field) for field in required_fields)
   

    def update_in_memory_procedure_step(self, procedure_step_id, new_data):
        """Update the in-memory procedure step list."""
        for step in ProcedureStepObject.procedure_step_list:
            if step.id == procedure_step_id:
                #step.order_step = new_data["order_step"]
                #step.object_name = new_data["object_name"]
                #step.action = new_data["action"]
                #step.executed_by = new_data["executed_by"]
                #step.required_input_state = new_data["required_input_state"]
                #step.output_state = new_data["output_state"]
                #step.physical_features = new_data["physical_features"]
                step.update(new_data)
                break

    def create_or_update_checkpoint(self, checkpoint_data):
        """Creates or updates a checkpoint entry for the procedure step, both in the database and in memory."""
        # Check if a checkpoint already exists for this step
        existing_checkpoint = CheckpointObject.return_checkpoint_by_step(self.procedure_step_id)
        if existing_checkpoint:
            # Update the existing checkpoint in the database
            CheckpointObject.edit_checkpoint(
                existing_checkpoint.id,
                **checkpoint_data
            )
            # Update the in-memory checkpoint
            self.update_in_memory_checkpoint(existing_checkpoint.id, checkpoint_data)
        else:
            # Create a new checkpoint in the database
            new_checkpoint = CheckpointObject.new_entry(
                checkpoint_data["name"],
                checkpoint_data["item_state"],
                checkpoint_data["person_state"],
                checkpoint_data["procedure_step_id"]
            )
            # Add the new checkpoint to the in-memory checkpoint list
            CheckpointObject.checkpoint_list.append(new_checkpoint)

    #def update_in_memory_checkpoint(self, checkpoint_id, checkpoint_data):
        """Update the in-memory checkpoint list."""
        #for checkpoint in CheckpointObject.checkpoint_list:
            #if checkpoint.id == checkpoint_id:
                #checkpoint.name = checkpoint_data["name"]
                #checkpoint.item_state = checkpoint_data["item_state"]
                #checkpoint.person_state = checkpoint_data["person_state"]
                #break

    def undo_step(self):
        # Revert the step to its initial values
        self.procedureStep_order.setPlainText(self.initial_values["order_step"])
        self.object_plainTextEdit.setPlainText(self.initial_values["object_name"])
        self.action_plainTextEdit.setPlainText(self.initial_values["action"])
        self.executedBy_plainTextEdit.setPlainText(self.initial_values["executed_by"])
        self.output_plainTextEdit.setPlainText(self.initial_values["output_state"])
        self.physicalFeatures_value.setPlainText(self.initial_values["physical_features"])
        self.disable_save_cancel_buttons()

    def update_initial_values(self):
        # Update initial values with the current step data
        self.initial_values["order_step"] = self.procedureStep_order.toPlainText()
        self.initial_values["object_name"] = self.object_plainTextEdit.toPlainText()
        self.initial_values["action"] = self.action_plainTextEdit.toPlainText()
        self.initial_values["executed_by"] = self.executedBy_plainTextEdit.toPlainText()
        self.initial_values["output_state"] = self.output_plainTextEdit.toPlainText()
        self.initial_values["physical_features"] = self.physicalFeatures_value.toPlainText()

   


    def open_delete_dialog(self):
        # Open a delete confirmation dialog and proceed if confirmed
        delete_dialog = DeleteDialog(self.procedure_step_id)
        delete_dialog.change_signal_delete.connect(self.update_all)
        result = delete_dialog.exec_()

        if result == DeleteDialog.Accepted:
            ProcedureStepObject.delete(self.procedure_step_id)
            self.change_signal_step.emit()

    def move_step_up(self):
    # Move the step up in the procedure
     if int(self.initial_values["order_step"]) > 1:
        ProcedureStepObject.move_step_up(int(self.initial_values["order_step"]), self.procedure_id)
        self.update_initial_values()
        self.procedureStep_order.setPlainText(str(self.step.order_step))  # Update step order in the UI
        self.change_signal_step.emit()

    def move_step_down(self):
    # Move the step down in the procedure
     max_order_number = max(
        step.order_step for step in ProcedureStepObject.procedure_step_list
        if step.procedure_id == self.procedure_id
    )

     if int(self.initial_values["order_step"]) < max_order_number:
        ProcedureStepObject.move_step_down(int(self.initial_values["order_step"]), self.procedure_id)
        self.update_initial_values()
        self.procedureStep_order.setPlainText(str(self.step.order_step))  # Update step order in the UI
        self.change_signal_step.emit()

    def update_all(self):
        # Emit a signal indicating that changes have been made
        self.change_signal_step.emit()

    def open_change_history_dialog(self):
     try:
        print("Opening Change History Dialog")
        dialog = QDialog()
        dialog.setWindowTitle("Change History")
        dialog.setMinimumSize(450, 200)

        # Ensure that change_history has valid data
        change_history = str(self.step.change_history)
        print(f"Change history content: {change_history}")

        label = QLabel(change_history)
        label.setAlignment(Qt.AlignTop)
        label.setWordWrap(True)

        layout = QVBoxLayout(dialog)
        layout.addWidget(label)

        dialog.adjustSize()
        dialog.exec_()

     except Exception as e:
        print(f"Error opening change history dialog: {e}")


        dialog.exec()
    def open_rationale_dialog(self):
        # Create a QDialog instance for rationale
        rationale_dialog = QDialog()
        ui = Ui_Rationale_Dialog()
        ui.setupUi(rationale_dialog)

        # Show the dialog and wait for user input
        result = rationale_dialog.exec_()

        if result == QDialog.Accepted:
            new_rationale = ui.textEdit.toPlainText()  # Get the text from the textEdit widget
            self.save_rationale(new_rationale)

    def open_comments_dialog(self):
        # Open the Comments Dialog
        comments_dialog = QDialog()
        ui = Ui_comments_dialog()
        ui.setupUi(comments_dialog)

        result = comments_dialog.exec_()

        if result == QDialog.Accepted:
            new_comment = ui.comments_textEdit.toPlainText()
            self.save_comment(new_comment)

    def open_system_dialog(self):
        # Open the Systems Dialog
        dialog = QtWidgets.QDialog()  # Create a QDialog instance
        ui = Ui_DialogSystem()  # Create an instance of the Ui_DialogSystem
        ui.setupUi(dialog)
   
        # Pass procedure step or item context if needed
        #dialog.phase_id = self.phase_id
        dialog.item_id = self.item_id

        dialog.exec_()
      
    def add_checkpoint_widget(self):
        # Create an instance of SetInputReqWidget
        checkpoint_widget = SetInputReqWidget(self)

        # Add it to the layout below the current step widget
        layout = self.parentWidget().layout()  # Assuming the step widget is inside a layout
        index = layout.indexOf(self)  # Get the index of the current step widget
        layout.insertWidget(index + 1, checkpoint_widget)  # Insert checkpoint widget below the step widget

    # Optionally, store the checkpoint widget reference if needed
        self.checkpoint_widget = checkpoint_widget

   
    def test_function(self):
        print("Button clicked!")

# In init method, replace
        self.saveChanges.clicked.connect(self.save_step)
# With this
        self.saveChanges.clicked.connect(self.test_function)
    
        dialog.exec_()  # Open the dialo    
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    FlightPhaseStep = QtWidgets.QWidget()  # Create the main widget instance
    ui = Ui_FlightPhaseStep()  # Create an instance of the UI class
    ui.setupUi(FlightPhaseStep)  # Set up the UI on the widget
    FlightPhaseStep.show()  # Show the widget with all the elements
    sys.exit(app.exec_())