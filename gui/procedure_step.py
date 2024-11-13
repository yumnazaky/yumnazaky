
import sys, os
import traceback
import math
import json 
import sqlite3, sqlalchemy
import resources_rc
import random

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
from PyQt5.QtGui import QIntValidator
from update_databases import update_lists
from flightphase_step import Ui_FlightPhaseStep
from database_item import DbItemEdition
from define_object_classes import ItemObject, ProcedureStepObject, CheckpointObject, ProcedureObject, TypeOfOperationObject, PhaseObject, SystemStateObject
from Database1 import SystemState as DbSystemStateEdition 
from comments_dialog import Ui_comments_dialog
from rationale_dialog import Ui_Rationale_Dialog
from set_input_req_dialog11 import Ui_setInputReqDialog
from system_functionalties_2 import DialogSystem
from Checkpoint_Input_Manager import CheckpointManager
from container import StepContainerWidget






from PyQt5 import QtWidgets, QtGui, QtCore
import traceback
from datetime import datetime
  

class FlightPhaseStep(QtWidgets.QWidget):
    item_id = math.nan
    
    procedure_step_id = math.nan
    procedure_id = math.nan
    procedure_list=[]
    procedure_step_list=[]
    change_signal_step = QtCore.pyqtSignal()
    checkpoint_added = pyqtSignal(int, dict) 
    move_up_signal = QtCore.pyqtSignal(int)
    move_down_signal = QtCore.pyqtSignal(int) 
    refresh_layout_signal = pyqtSignal()# Signal for notifying changes
    selection_complete = QtCore.pyqtSignal()
    saved_systems_signal = pyqtSignal(dict)

    def __init__(self,  procedure_step_id=None, phase_id=None,parent=None):
        super(FlightPhaseStep, self).__init__(parent)
        print("ItemObject.item_list:", [(item.id, item.name) for item in ItemObject.item_list])

        print(f"Initializing FlightPhaseStep for procedure_step_id: {procedure_step_id}")
        #print("ProcedureStep widget created with:", procedure_step)
        # Set up the UI from the Ui_FlightPhaseStep class (no multiple inheritance)
        #if not hasattr(self, 'saved_systems_by_step'):
            #self.saved_systems_by_step = {}
        self.saved_systems_by_step = {}    
        self.ui = Ui_FlightPhaseStep()
        self.ui.setupUi(self)
        #ItemObject.initialize_default_systems() 
        print(f"ObjectPlainTextEdit: {self.ui.object_plainTextEdit}")
        
        self.ui.addCheckpoint_pushButton.clicked.connect(self.add_checkpoint)
        #self.procedure_step = procedure_step  # The ProcedureStepObject being edited
        self.checkpoints = []
        self.phase_id = phase_id
        #self.item_id = item_id
        self.ui.up_procedureStep.clicked.connect(self.move_procedure_step_up)
        self.ui.down_procedureStep.clicked.connect(self.move_procedure_step_down)
        self.procedure_step_id = procedure_step_id  # Initialize checkpoint list
        self.procedure_step = ProcedureStepObject.return_procedure_step(self.procedure_step_id)
        
        if self.procedure_step and self.procedure_step.item_id != -1:
            self.item_id = self.procedure_step.item_id
            print(f"Using procedure step item_id: {self.item_id}")
        else:
            # Set to default from ItemObject if item_id is -1 or not assigned
            self.item_id = self._get_default_item_id()
            if self.procedure_step:
                self.procedure_step.item_id = self.item_id
            print(f"Assigned default item_id {self.item_id} for procedure step")

         # Initialize if empty

        
        #if self.item_id:
            #self.item = ItemObject.return_item(self.item_id)
            #print(f"Item ID: {self.item_id}, Item: {self.item}")
        physical_features = {}

        if self.procedure_step:
            if isinstance(self.procedure_step.physical_features, str):
                try:
            # If it's a JSON string, parse it to a dictionary
                    physical_features = json.loads(self.procedure_step.physical_features)
                except json.JSONDecodeError:
                    print("Error decoding JSON for physical_features, using empty dictionary instead.")
                    physical_features = {}
            else:
        # If it's already a dictionary, use it directly
                physical_features = self.procedure_step.physical_features

            print(f"Physical Features: {physical_features}")
        else:
            physical_features = {}


        # Store initial values to manage undo functionality
        print(f"Action value: {self.procedure_step.action} (Type: {type(self.procedure_step.action)})")

        self.initial_values = {
            "object_name": self.ui.object_plainTextEdit.toPlainText(),
            "action": self.ui.action_plainTextEdit.toPlainText(),
            "order_step": self.ui.procedureStep_order.text(),
            "executed_by": self.ui.executedBy_plainTextEdit.toPlainText(),
            "output_state": self.ui.output_plainTextEdit.toPlainText(),
            "physical_features": {
                "parameter": self.ui.physicalFeatures_param.toPlainText(),
                "value": self.ui.physicalFeatures_value.toPlainText()
            }
        }

    
        
        self.ui.saveChanges.clicked.connect(self.save_step_data)
        self.ui.caancel_changes.clicked.connect(self.undo_step)
        self.ui.changeLog.clicked.connect(self.open_change_history_dialog)
        self.ui.systems_pushButton.clicked.connect(self.systems_button_clicked)
        self.ui.comments_button.clicked.connect(self.open_comments_dialog)
        self.ui.rationale_button.clicked.connect(self.open_rationale_dialog)
        self.ui.delete_procedureStep.clicked.connect(self.delete_step_confirmation)

        self.ui.addCheckpoint_pushButton.clicked.connect(self.add_checkpoint)

        # Disable Save and Cancel buttons initially
        self.ui.saveChanges.setEnabled(False)
        self.ui.caancel_changes.setEnabled(False)

        # Enable Save and Cancel buttons when text changes
        self.ui.object_plainTextEdit.textChanged.connect(self.enable_save_cancel_buttons)
        self.ui.action_plainTextEdit.textChanged.connect(self.enable_save_cancel_buttons)
        self.ui.output_plainTextEdit.textChanged.connect(self.enable_save_cancel_buttons)
        self.ui.executedBy_plainTextEdit.textChanged.connect(self.enable_save_cancel_buttons)
        self.ui.procedureStep_order.textChanged.connect(self.enable_save_cancel_buttons)
        self.ui.physicalFeatures_value.textChanged.connect(self.enable_save_cancel_buttons)
        self.ui.physicalFeatures_param.textChanged.connect(self.enable_save_cancel_buttons)
        self.update_all_lists()
        # Load initial data into the text fields
        self.load_step_data()
    def on_save_changes(self):
        # Some logic to handle saving
        self.change_signal_procedure_step.emit()
    def load_step_data(self):
        print(f"Loading procedure step: {self.procedure_step}")
        print(f"Expected order_step: {self.procedure_step.order_step}")
        print(f"Expected action: {self.procedure_step.action}")
        """Load the data from the ProcedureStepObject into the UI."""
        self.ui.object_plainTextEdit.setPlainText(self.procedure_step.object_name)
        self.ui.action_plainTextEdit.setPlainText(str(self.procedure_step.action))
        self.ui.executedBy_plainTextEdit.setPlainText(self.procedure_step.executed_by)
        #self.ui.physicalFeatures_value.setPlainText(self.procedure_step.physical_features)
        self.ui.output_plainTextEdit.setPlainText(self.procedure_step.comments)
        self.ui.procedureStep_order.setText(str(self.procedure_step.order_step))


        if isinstance(self.procedure_step.physical_features, dict):
            self.ui.physicalFeatures_param.setPlainText(self.procedure_step.physical_features.get("parameter", ""))
            self.ui.physicalFeatures_value.setPlainText(self.procedure_step.physical_features.get("value", ""))
        self.update_initial_values()
    def _get_default_item_id(self):
        if not ItemObject.item_list:
            print("ItemObject.item_list is empty; cannot fetch a default ID.")
            return -1
        return ItemObject.item_list[0].id
        #selected_item = random.choice(ItemObject.item_list)
        #print(f"Selected default item ID: {selected_item.id}")
        #return selected_item.id
    
    
    def enable_save_cancel_buttons(self):
        """Enable Save and Cancel buttons when the user modifies data."""
        self.ui.saveChanges.setEnabled(True)
        self.ui.caancel_changes.setEnabled(True)

    
    # Set a default item_id during procedure step creation or loading
        if self.procedure_step.item_id == -1 or self.procedure_step.item_id is None:
        # Check if `item_list` has been populated with items
            if ItemObject.item_list:
                first_item = ItemObject.item_list[0]
                self.procedure_step.item_id = first_item.id
                print(f"Assigned default item_id {self.procedure_step.item_id} to procedure step.")
            else:
            # If `item_list` is empty, defer setting item_id until items are available
                print("Warning: ItemObject.item_list is empty; cannot assign a valid item_id.")
    def save_step_data(self):
        print(f"Saving procedure step: Action from UI: {self.ui.action_plainTextEdit.toPlainText()}")
        if self.procedure_step is None:
            QtWidgets.QMessageBox.warning(self, "Error", "Procedure step not initialized.")
            return 
      
        item = ItemObject.return_item(self.item_id)
        if isinstance(self.procedure_step.physical_features, str):
            try:
                self.procedure_step.physical_features = json.loads(self.procedure_step.physical_features)
            except json.JSONDecodeError:
                print("Error decoding JSON for physical_features; defaulting to empty dictionary.")
                self.procedure_step.physical_features = {}
        changes = []  # Initialize changes as an empty list

    # Check each field and record changes
        if self.procedure_step.object_name != self.ui.object_plainTextEdit.toPlainText():
            changes.append(f"Changed object_name from '{self.procedure_step.object_name}' to '{self.ui.object_plainTextEdit.toPlainText()}'")
            self.procedure_step.object_name = self.ui.object_plainTextEdit.toPlainText()

        if self.procedure_step.action != self.ui.action_plainTextEdit.toPlainText():
            changes.append(f"Changed action from '{self.procedure_step.action}' to '{self.ui.action_plainTextEdit.toPlainText()}'")
            self.procedure_step.action = self.ui.action_plainTextEdit.toPlainText()
        if self.procedure_step.executed_by != self.ui.executedBy_plainTextEdit.toPlainText():
            changes.append(f"Changed executed_by from '{self.procedure_step.executed_by}' to '{self.ui.executedBy_plainTextEdit.toPlainText()}'")
            self.procedure_step.executed_by = self.ui.executedBy_plainTextEdit.toPlainText()

        if self.procedure_step.output_state != self.ui.output_plainTextEdit.toPlainText():
            changes.append(f"Changed output_state from '{self.procedure_step.output_state}' to '{self.ui.output_plainTextEdit.toPlainText()}'")
            self.procedure_step.output_state = self.ui.output_plainTextEdit.toPlainText()

    # Check each part of physical_features
        if self.procedure_step.physical_features.get("parameter") != self.ui.physicalFeatures_param.toPlainText():
            changes.append(f"Changed physical_features parameter from '{self.procedure_step.physical_features.get('parameter')}' to '{self.ui.physicalFeatures_param.toPlainText()}'")
            self.procedure_step.physical_features["parameter"] = self.ui.physicalFeatures_param.toPlainText()

        if self.procedure_step.physical_features.get("value") != self.ui.physicalFeatures_value.toPlainText():
            changes.append(f"Changed physical_features value from '{self.procedure_step.physical_features.get('value')}' to '{self.ui.physicalFeatures_value.toPlainText()}'")
            self.procedure_step.physical_features["value"] = self.ui.physicalFeatures_value.toPlainText()

    # Order step, ensuring conversion to integer
        #new_order_step = str(self.ui.procedureStep_order.text()) if self.ui.procedureStep_order.text().isdigit() else 0
        if self.procedure_step.order_step != str(self.ui.procedureStep_order.text()):
            changes.append(f"Changed order_step from '{self.procedure_step.order_step}' to '{str(self.ui.procedureStep_order.text())}'")
            self.procedure_step.order_step = str(self.ui.procedureStep_order.text())   
        if isinstance(self.procedure_step.change_history, str):
            try:
                self.procedure_step.change_history = json.loads(self.procedure_step.change_history)
            except json.JSONDecodeError:
                print("Error decoding change_history JSON; initializing with an empty list.")
                self.procedure_step.change_history = []
    # Continue checking other fields similarly...
        physical_features_json = json.dumps(self.procedure_step.physical_features)
        #change_history_json = json.dumps(self.procedure_step.change_history)
    # If there are changes, add to change history
        if changes:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            for change in changes:
                self.procedure_step.change_history.append({"time": timestamp, "change": change})
        change_history_json = json.dumps(self.procedure_step.change_history)
    
       
        

    # Save to the in-memory list and update the database
        ProcedureStepObject.edit_procedure_step(
            self.procedure_step.id,
            object_name=self.procedure_step.object_name,
            order_step=self.procedure_step.order_step,
            action=self.procedure_step.action,
            executed_by=self.procedure_step.executed_by,
            required_input_state=self.procedure_step.required_input_state,
            output_state=self.procedure_step.output_state,
            physical_features=physical_features_json,
            rationale=self.procedure_step.rationale,
            comments=self.procedure_step.comments,
            change_history=change_history_json,
            procedure_id=self.procedure_step.procedure_id,
            item_id=self.procedure_step.item_id
        )

        self.update_initial_values()
        self.ui.saveChanges.setEnabled(False)
        self.ui.caancel_changes.setEnabled(False)
   

    def undo_step(self):
        """Revert the step to its initial values."""
        self.load_step_data()
        self.ui.saveChanges.setEnabled(False)
        self.ui.caancel_changes.setEnabled(False)

    def update_initial_values(self):
        """Update initial values with the current step data."""
        print(f"Updating initial values: order_step = {self.ui.procedureStep_order.text()}, action = {self.ui.action_plainTextEdit.toPlainText()}")
   
        self.initial_values["order_step"] = str(self.ui.procedureStep_order.text())

        self.initial_values["object_name"] = self.ui.object_plainTextEdit.toPlainText()
        self.initial_values["action"] = self.ui.action_plainTextEdit.toPlainText()
        self.initial_values["executed_by"] = self.ui.executedBy_plainTextEdit.toPlainText()
        self.initial_values["output_state"] = self.ui.output_plainTextEdit.toPlainText()
        self.initial_values["physical_features"] = {
            "parameter": self.ui.physicalFeatures_param.toPlainText(),  # Assuming this is a QLabel or QLineEdit
            "value": self.ui.physicalFeatures_value.toPlainText()  # Assuming this is a QPlainTextEdit
        }
        print(f"Initial values set:")
        print(f" - order_step: {self.initial_values['order_step']}")
        print(f" - action: {self.initial_values['action']}")
        print(f" - object_name: {self.initial_values['object_name']}")
        print(f" - executed_by: {self.initial_values['executed_by']}")
        print(f" - output_state: {self.initial_values['output_state']}")
        print(f" - physical_features: {self.initial_values['physical_features']}")
    

        
    def move_procedure_step_up(self):
        self.move_up_signal.emit(self.procedure_step.order_step)
  
    def move_procedure_step_down(self):
        self.move_down_signal.emit(self.procedure_step.order_step)

    def find_parent_layout(self):
        """Helper method to find and return the parent layout."""
        parent_widget = self.parentWidget()
        while parent_widget is not None:
            layout = parent_widget.layout  # Access the layout property without parentheses
            if layout is not None:
                return layout
            parent_widget = parent_widget.parentWidget()
        return None      
    def swap_step_with_previous(self, layout, current_order):
        """Swaps this widget with the one above it in the layout."""
        print(f"Swapping step at order {current_order} with the previous step.")
        index = layout.indexOf(self.parentWidget())  # `self` is `FlightPhaseStep` inside `StepContainerWidget`
        if index > 0:
            previous_widget = layout.itemAt(index - 1).widget()
        
        # Swap in the layout
            layout.removeWidget(self.parentWidget())
            layout.removeWidget(previous_widget)
            #layout.insertWidget(previous_widget())
            #self.parentWidget().setParent(None)
            #previous_widget.setParent(None)
        
        # Swap in the layout
            layout.insertWidget(index - 1, self.parentWidget())
            layout.insertWidget(index, previous_widget)
            layout.update()
        # Swap order in data model
            self.procedure_step.order_step, previous_widget.procedure_step.order_step = (
                previous_widget.procedure_step.order_step,
                self.procedure_step.order_step,
            )
        
        # Update initial values for each step
            self.update_initial_values()
            previous_widget.update_initial_values()

    def swap_step_with_next(self, layout, current_order):
        """Swaps this widget with the one below it in the layout."""
        #print(f"Swapping step at order {current_order} with the previous step.")
        index = layout.indexOf(self.parentWidget())
        if index < layout.count() - 2:  # Ensure there is a widget below
            next_widget = layout.itemAt(index + 1).widget()

        # Swap in the layout
            layout.removeWidget(self.parentWidget())
            layout.insertWidget(index + 1, self.parentWidget())
            layout.update()

        # Swap order in data model
            self.procedure_step.order_step, next_widget.procedure_step.order_step = (
                next_widget.procedure_step.order_step,
                self.procedure_step.order_step,
            )

        # Update initial values for each step
            self.update_initial_values()
            next_widget.update_initial_values()


    def open_change_history_dialog(self):
    
        if isinstance(self.procedure_step.change_history, str):
            try:
                self.procedure_step.change_history = json.loads(self.procedure_step.change_history)
                if not isinstance(self.procedure_step.change_history, list):
                    raise ValueError("change_history JSON is not a list.")
            except (json.JSONDecodeError, ValueError):
                print("Error decoding change_history or unexpected format. Initializing as an empty list.")
                self.procedure_step.change_history = []

        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Change History")
        layout = QtWidgets.QVBoxLayout(dialog)

        change_log_browser = QtWidgets.QTextBrowser(dialog)
        if self.procedure_step.change_history:
            change_log_text = "\n".join(
                [f"{entry['time']}: {entry['change']}" for entry in self.procedure_step.change_history]
            )
        else:
            change_log_text = "No changes recorded."

        change_log_browser.setPlainText(change_log_text)
        layout.addWidget(change_log_browser)

        close_button = QtWidgets.QPushButton("Close", dialog)
        close_button.clicked.connect(dialog.accept)
        layout.addWidget(close_button)

        dialog.exec_()

    def systems_button_clicked(self):
        self.update_all_lists() 
        dialog = DialogSystem(
            parent=self,
            item_id=self.item_id,
            instance_id=(self.phase_id, self.procedure_step_id),
            saved_systems_by_step=self.saved_systems_by_step
        )
        dialog.systems_selected.connect(self.update_systems_selection)  # Connect selection updates

    # Load saved selections before showing the dialog
       
        dialog.exec_()  # Open dialog as a modal



    def update_systems_selection(self, item_id, provides, requires, turns_off):
        print("update_systems_selection called with:", item_id, provides, requires, turns_off)
        instance_id = (self.phase_id, self.procedure_step_id)
        #instance_id = (self.phase_id, self.procedure_step_id)
    
        self.saved_systems_by_step[instance_id] = {
            "item_id": item_id,
            "provides": provides,
            "requires": requires,
            "turns_off": turns_off
        }

        

        procedure_step = ProcedureStepObject.return_procedure_step(self.procedure_step_id)
        if procedure_step:
            procedure_step.item_id = item_id
            procedure_step.provides = provides[:]
            procedure_step.requires = requires[:]
            procedure_step.turns_off = turns_off[:]
        
            ProcedureStepObject.edit_procedure_step(
                procedure_step.id,
                object_name=procedure_step.object_name,
                order_step=procedure_step.order_step,
                action=procedure_step.action,
                executed_by=procedure_step.executed_by,
                required_input_state=procedure_step.required_input_state,
                output_state=procedure_step.output_state,
                physical_features=procedure_step.physical_features,
                rationale=procedure_step.rationale,
                comments=procedure_step.comments,
                change_history=procedure_step.change_history,
                procedure_id=procedure_step.procedure_id,
                item_id=item_id
            )
        print(f"Selections saved for procedure_step_id {self.procedure_step_id}")
    # Update `saved_systems_by_step` for the specific procedure_step_id and item_id
        
    # Initialize saved_systems_by_step if it doesn't exist
        #if self.procedure_step_id not in self.saved_systems_by_step:
            #self.saved_systems_by_step[self.procedure_step_id] = {}
        #self.saved_systems_by_step[self.procedure_step_id][item_id] = current_selections
     

        #self.selection_complete.emit()
    # Debugging output to confirm persistence
       
    

    def open_comments_dialog(self):
        """Open the comments dialog and save the entered comment."""
        # Create the dialog instance
        dialog = QtWidgets.QDialog(self)
        comments_ui = Ui_comments_dialog()  # Assuming Ui_comments_dialog is defined somewhere
        comments_ui.setupUi(dialog)

        # Load the current comment into the dialog's comment field
        comments_ui.comments_textEdit.setPlainText(self.procedure_step.comments)

        # Execute the dialog
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            # Retrieve the entered comment from the dialog
            new_comment = comments_ui.comments_textEdit.toPlainText()

            # Save the new comment in the ProcedureStepObject
            self.procedure_step.comments = new_comment

            # Optionally, log this change in the change history
            self.procedure_step.add_change_log("Comment updated.")
            self.enable_save_cancel_buttons() 
    def open_rationale_dialog(self):
        """Open the rationale dialog and save the entered rationale."""
        # Create the dialog instance
        dialog = QtWidgets.QDialog(self)
        rationale_ui = Ui_Rationale_Dialog()  # Assuming Ui_Rationale_Dialog is defined somewhere
        rationale_ui.setupUi(dialog)

        # Load the current rationale into the dialog's text field
        rationale_ui.textEdit.setPlainText(self.procedure_step.rationale)

        # Execute the dialog
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            # Retrieve the entered rationale from the dialog
            new_rationale = rationale_ui.textEdit.toPlainText()

            # Save the new rationale in the ProcedureStepObject
            self.procedure_step.rationale = new_rationale

            # Optionally, log this change in the change history
            self.procedure_step.add_change_log("Rationale updated.")

            

            # Mark changes as made, enabling the save button
            self.enable_save_cancel_buttons()  
    def delete_step_confirmation(self):
        """Ask the user if they are sure they want to delete the procedure step."""
        # Create a confirmation dialog
        msg_box = QtWidgets.QMessageBox(self)
        msg_box.setIcon(QtWidgets.QMessageBox.Warning)
        msg_box.setWindowTitle("Delete Step")
        msg_box.setText("Are you sure you want to delete this step?")
        msg_box.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        msg_box.setDefaultButton(QtWidgets.QMessageBox.No)

    # Execute the message box and get the user's response
        response = msg_box.exec_()

    # If the user clicks Yes, delete the step
        if response == QtWidgets.QMessageBox.Yes:
            self.delete_step()

    def delete_step(self):
        """Deletes the current procedure step and updates the order of remaining steps."""
        if self.procedure_step is None:
            return  # No step to delete

        step_to_delete_order = int(self.procedure_step.order_step)
        step_to_delete_id = self.procedure_step.id

    # Delete the step from the database and in-memory list
        self.procedure_step.delete()
        #ProcedureStepObject.procedure_step_list = [
            #step for step in ProcedureStepObject.procedure_step_list if step.id != step_to_delete_id
        #]
        ProcedureStepObject.procedure_step_list = [
            step for step in ProcedureStepObject.procedure_step_list if step.id != step_to_delete_id
        ]

    # Reorder remaining steps
        #self.reorder_steps(int(self.procedure_step.order_step))
        container_layout = None
        widget = self

        parent_container = self.parentWidget()  # This should be the StepContainerWidget if setup correctly
        if isinstance(parent_container, StepContainerWidget):
            container_widget = parent_container
            layout = container_widget.parentWidget().layout()  # Layout holding the StepContainerWidget

    # Check if both the container widget and layout are found
        if not container_widget or not layout:
            print("Error: No valid StepContainerWidget or layout found.")
            return

    # Remove the StepContainerWidget from the layout and delete it
        index = layout.indexOf(container_widget)
        if index != -1:
            item = layout.takeAt(index)
            if item.widget() == container_widget:
                container_widget.deleteLater()
    # Step 3: Emit signal to trigger immediate UI reload
        #self.changes_signal_step.emit()
        self.reorder_steps(step_to_delete_order)

    # Refresh the UI
        #self.setParent(None)  # This removes the widget from the layout
        self.update_all()

    def reorder_steps(self, deleted_order):
        """Reorder the steps after a deletion to close the gap in the order numbers."""
        print(f"Reordering steps after deletion of order: {deleted_order}")
        for step in ProcedureStepObject.procedure_step_list:
            print(f"Before: ID: {step.id}, Order Step: {step.order_step}")
            if int(step.order_step) > deleted_order:
            # Decrease order number by 1 for all steps that were after the deleted step
                new_order_step = int(step.order_step) - 1
                step.order_step = new_order_step

            # Update the order in the database
                #DbProcedureStepEdition.change_entry(
                    #step.id,
                    #object_name=step.object_name,
                    #action=step.action,
                    #order_step=new_order_step,
                    #executed_by=step.executed_by,
                    #required_input_state=step.required_input_state,
                    #output_state=step.output_state,
                    #physical_features=step.physical_features,
                    #rationale=step.rationale,
                    #comments=step.comments,
                    #change_history=step.change_history,
                    #procedure_id=step.procedure_id,
                    #item_id=step.item_id
                #)
        self.setParent(None)          
        self.update_all()    
    def update_all(self):
        """Emits a signal to update the UI in the main window after deletion."""
        self.change_signal_step.emit()
    def add_checkpoint(self):
        """Open the custom checkpoint dialog to add a new checkpoint."""
        checkpoint_dialog = QtWidgets.QDialog(self)
        ui_dialog = Ui_setInputReqDialog()
        ui_dialog.setupUi(checkpoint_dialog)
       
     
    
        # Ensure the buttons are connected to dialog accept/reject
        ui_dialog.inputButtonBox.accepted.connect(checkpoint_dialog.accept)
        ui_dialog.inputButtonBox.rejected.connect(checkpoint_dialog.reject)
        result = checkpoint_dialog.exec_()

        if result == QtWidgets.QDialog.Accepted:
            checkpoint_name = ui_dialog.checkpointInputLineEdit.text()
            item_state = ui_dialog.systemInputLineEdit.text()
            person_state = ui_dialog.parameterLineEdit.text()

            if checkpoint_name and item_state and person_state:
                checkpoint_data = {
                    "checkpoint_name": checkpoint_name,
                    "item_state": item_state,
                    "person_state": person_state
                }
                self.checkpoint_added.emit(self.procedure_step_id, checkpoint_data)
            else:
                QtWidgets.QMessageBox.warning(self, "Input Error", "All fields are required to add a checkpoint.")


    def update_all_lists(self):
        self.type_of_operation_list = TypeOfOperationObject.type_of_operation_list
        self.phase_list = PhaseObject.phase_list
        self.procedure_list = ProcedureObject.procedure_list
        self.procedure_step_list = ProcedureStepObject.procedure_step_list
        self.checkpoint_list = CheckpointObject.checkpoint_list    
        self.item_list = ItemObject.item_list
        #print("Item list after update_all_lists:", self.item_list)  # Ensuring items are updated for system dialog
        self.system_state_list = SystemStateObject.system_state_list 



     