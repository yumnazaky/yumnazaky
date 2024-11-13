import sys, os
import traceback
import math
import json 
import sqlite3, sqlalchemy
from sqlalchemy.orm import subqueryload
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
import resources_rc


from PyQt5 import QtCore, QtGui, QtWidgets
from Database1 import Database, Phase, TypeOfOperation, ProcedureStep, Item, SystemState
from update_databases import update_lists
from new_step import Ui_newStep_dialog
from define_object_classes import PhaseObject, TypeOfOperationObject,ProcedureStepObject, SystemStateObject, ItemObject, ProcedureObject, CheckpointObject  
from systems_dialog import Ui_DialogSystem
from system_functionalties_2 import DialogSystem

class newStep_dialog(QDialog, Ui_newStep_dialog):
    valid_flag = False  # To check the validity of the entered data
    phase_list = []
    type_of_operation_list = []
    system_state_list = []
    item_list = []
    procedure_list = []
    phase_list = []
    procedure_step_list = []
    checkpoint_list = []
    item_id = math.nan
    #change_signal_phase = QtCore.pyqtSignal()
    change_signal_procedure_dialog= pyqtSignal()
    step_saved_signal = pyqtSignal(dict)
    #Database.create_engine()  # Initialize the database engine at the start

    def __init__(self,selected_operation_id=None, selected_phase_id=None, parent=None):
        super(newStep_dialog, self).__init__(parent)

        # Call setupUi to initialize the dialog UI
        self.setupUi(self)

        # Populate lists on dialog load
        self.phase_list, self.type_of_operation_list = self.load_phase_and_operation_lists()
        self.procedure_step = None
        self.selected_operation_id = selected_operation_id
        self.selected_phase_id = selected_phase_id
        self.populate_operation_combo_box()
        #self.procedure_step_id =procedure_step_id
        #self.procedure_step_list = ProcedureStepObject.procedure_step_list

        # Set up the button box functionality
        self.buttonBox_new_step.accepted.connect(self.save_object_data)
        self.buttonBox_new_step.rejected.connect(self.reject)
        self.refresh_ui()
        #self.procedure_step = ProcedureStepObject.return_procedure_step(self.procedure_step_id)
        #if self.procedure_step is None:
            #QtWidgets.QMessageBox.warning(self, "Error", "Procedure step not found for the given ID.")
            #return

        
        #self.flightPhase_select.currentIndexChanged.connect(self.populate_flight_phase_combo_box)

        # Populate the flight phase combo box when an operation type is selected
        #self.flightPhase_select.currentIndexChanged.connect(self.populate_flight_phase_combo_box)
        # In your setupUi or __init__ method
        #self.pushButton_systems.clicked.connect(self.open_system_dialog)
        self.belonging_to_operation_select.currentIndexChanged.connect(self.on_operation_changed)
        self.flightPhase_select.currentIndexChanged.connect(self.on_phase_changed)



        # Example connection to other widgets
        self.new_object.textChanged.connect(self.validate_fields)
        self.action_new.textChanged.connect(self.validate_fields)
    def disable_all_inputs(self):
        """
        Disables all input fields in the dialog to prevent user interaction.
        """
        
        self.buttonBox_new_step.setDisabled(True)  # Example button

    def enable_all_inputs(self):
        """
        Enables all input fields in the dialog to allow user interaction.
        """
       
        self.buttonBox_new_step.setEnabled(True)
    def load_phase_and_operation_lists(self):
        # Load phase and operation lists from database or other sources
        (
            item_list,
            procedure_list,
            procedure_step_list,
            type_of_operation_list,
            system_state_list,
            phase_list,
            checkpoint_list,
        ) = update_lists()
        #self.populate_flight_phase_combo_box()
        #self.populate_procedure_combo_box()
        return phase_list, type_of_operation_list
    def populate_operation_combo_box(self):
        """Populates the 'Belonging to Operation Type' combo box with available operation types."""
        self.belonging_to_operation_select.clear()

    # Add operation types from the list
        for operation in self.type_of_operation_list:
            self.belonging_to_operation_select.addItem(operation.type_of_operation, operation.id)
        if self.selected_operation_id is not None:
            index = self.belonging_to_operation_select.findData(self.selected_operation_id)
            if index != -1:
                self.belonging_to_operation_select.setCurrentIndex(index)
            self.on_operation_changed()

    # Connect the combo box to the phase population function
        
    def on_operation_changed(self):
        """Handles changes in the operation type combo box."""
        selected_operation_index = self.belonging_to_operation_select.currentIndex()
        selected_operation_id = self.belonging_to_operation_select.itemData(selected_operation_index)
        
        if selected_operation_id is not None:
            self.populate_flight_phase_combo_box(selected_operation_id)

    def populate_flight_phase_combo_box(self, operation_type):
        """
        Populates the flightPhase_select combo box with phases based on the selected operation type.
        """
        #current_tab_index = self.flightPhases_tabs.currentIndex()
        #if current_tab_index == -1 or current_tab_index >= len(self.new_tab_input):
            #QtWidgets.QMessageBox.warning(self, "Error", "No valid operation selected.")
            #return
    
        #selected_operation_id = self.new_tab_input[current_tab_index]["id"]
    # Now filter the phases using the selected operation ID
        
    # Clear the combo box before populating it
        self.flightPhase_select.blockSignals(True)
        self.flightPhase_select.clear()
        phases = [phase for phase in self.phase_list if phase.type_of_operation_id == operation_type]


    # Add each phase into the combo box with the phase name and phase ID as data
        if phases:
            for phase in phases:
                self.flightPhase_select.addItem(phase.name, phase.id)

        # Automatically populate procedures based on the first phase
            first_phase_id = phases[0].id
            self.populate_procedure_combo_box(first_phase_id)
        else:
        # If no phases exist, add a fallback message
            self.flightPhase_select.addItem("No Phases Available", None)    
        self.flightPhase_select.blockSignals(False)
    # Connect the phase combo box to procedure population
        #self.flightPhase_select.currentIndexChanged.connect(self.on_phase_changed)
    

        # Trigger procedure combo population after the phase combo box is populated
        #if phases:
            #self.populate_procedure_combo_box(phases[0].id)
        #else:
            #print(f"No phases found for operation type '{selected_operation_id}'")
        #session = Database.get_session()
        
        # Query the database for the TypeOfOperation matching the selected operation type
        #operation = next((op for op in self.type_of_operation_list if op.type_of_operation == operation_type), None)

        #operation = session.query(TypeOfOperation).filter_by(type_of_operation=operation_type).first()

        #if operation and operation.phase_list:
            # Clear the combo box before populating it
            #self.flightPhase_select.clear()

            # Add each phase from the phase_list into the combo box
            #for phase in operation.phase_list:
                #self.flightPhase_select.addItem(phase["name"])

             

        #session.close()
    def on_phase_changed(self):
        """Handles changes in the flight phase combo box."""
        selected_phase_index = self.flightPhase_select.currentIndex()
        selected_phase_id = self.flightPhase_select.itemData(selected_phase_index)
        self.populate_procedure_combo_box(selected_phase_id)
        
    def populate_procedure_combo_box(self, phase_id):
        """
        Populates the belonging_to_procedure_select combo box with procedures based on the selected phase.
        """
        #session = Database.get_session()

    # Fetch the procedures for the selected phase
        
        #procedures = session.query(ProcedureObject).filter_by(phase_id=phase_id).all()

    # Clear the procedure combo box before populating it
        self.belonging_to_procedure_select.clear()
        procedures = [proc for proc in ProcedureObject.procedure_list if proc.phase_id == phase_id]


    # Add a default "Select Procedure" option
        #self.belonging_to_procedure_select.addItem("Select Procedure", None)

    # Populate the combo box with the fetched procedures
        if procedures:
            for procedure in procedures:
                self.belonging_to_procedure_select.addItem(procedure.name, procedure.id)
        else:
            self.belonging_to_procedure_select.addItem("No Procedures Available", None)

        #session.close()
    


    def update_object_in_db(self,object_name, action, order_step, executed_by, output_param, physical_features,procedure_id,):
        """
        Updates the ProcedureStepObject in the database when a new object, action, executed by, output parameter,
        or physical feature is provided.
        """
        #session = Database.get_session()

        # Fetch the procedure step if it exists, otherwise create a new one
        #procedure_step = next((step for step in ProcedureStepObject.procedure_step_list if step.object_name == object_name), None)

        #procedure_step = session.query(ProcedureStepObject).filter_by(object_name=object_name).first()
        #if isinstance(order_step, str) and order_step.isdigit():
            #order_step = str(order_step)

    # Check if the procedure step already exists in memory
        procedure_step = next((step for step in ProcedureStepObject.procedure_step_list if step.object_name == object_name), None)

        if procedure_step:
            # Update existing procedure step details
            procedure_step.object_name = object_name
            procedure_step.action = action
            procedure_step.executed_by = executed_by
            procedure_step.order_step = int(order_step)
            procedure_step.output_state = output_param
            procedure_step.physical_features = {
                "parameter": physical_features.get("parameter", ""),
                "value": physical_features.get("value", "")
            }
            procedure_step.procedure_id = procedure_id
            procedure_step.item_id = item_id
            print(f"Order Step: {self.procedure_step.order_step}, Action: {self.procedure_step.action}")
            
            #procedure_step.item_id = item_id # Update procedure_id
            #procedure_step.phase_id = phase_id  
        else:
            # Create new procedure step entry
           
    
            change_history = []
            change_history_json = json.dumps(change_history)
            new_procedure_step = ProcedureStepObject.new_entry(
                 
                ObjectName=object_name,
                
                Action=action,
                OrderStep= order_step,
                ExecutedBy=executed_by,
                OutputState=output_param,
                PhysicalFeatures={
                    "parameter": physical_features.get("parameter", ""),
                    "value": physical_features.get("value", "")
                },
                ProcedureID=procedure_id, 
                Rationale="",  # Default empty rationale
                Comments="",  # Default empty comments
                ChangeHistory=change_history_json,  # Default empty change history
                RequiredInputState="",                  

                ItemID=item_id # Link to the procedure
                #phase_id=phase_id  
                #ItemID=item_id
            )
            ProcedureStepObject.procedure_step_list.append(new_procedure_step)
            if new_procedure_step is None:
                print("[Debug] new_procedure_step creation failed: received None")
            else:
                print(f"[Debug] New procedure step created with ID: {new_procedure_step.id}")
            #session.add(new_procedure_step)

        # Commit the changes to the database
        #session.commit()
        #session.close()

        print(f"Procedure Step '{object_name}' updated or added successfully.")

    #def update_item_in_db(self, item_name, provides, requires, turns_off):
       
       # item = next((itm for itm in ItemObject.item_list if itm.name == item_name), None)

        #if item:
            # Update existing item details
            #item.provides = provides
            #item.requires = requires
            #item.turns_off = turns_off
        #else:
            # Create new item entry
            #new_item = ItemObject(
                #name=item_name,
                #provides=provides,
               # requires=requires,
                #turns_off=turns_off
            #)
           # ItemObject.item_list.append(new_item)
          

       #print(f"Item '{item_name}' updated or added successfully.")

    def save_object_data(self):
        
        #Saves or updates the data entered in the object field into the database.
        
         # Get input values from the UI fields
        print("save_object_data called!") 
        print(f"Object Name: {self.new_object.text().strip()}")
        print(f"Order Step: {self.spinBox_step_position.value()} (From spin box)")
        print(f"Action: {self.action_new.text().strip()} (From action field)")
        object_name = self.new_object.text().strip()  # Assuming new_object is a QLineEdit
        action = self.action_new.text().strip()  # Assuming action_new is a QLineEdit
        executed_by = self.executedBy_new.text().strip()  # Assuming executedBy_new is a QLineEdit
        output_param = self.outputParameters_new.text().strip()  
        order_step = int(self.spinBox_step_position.value())
        rationale = ""  # Default value
        comments = "" 
        required_input_state = "" 
        change_history = json.dumps([])  # Default value for an empty change history
        item_id = ItemObject.item_list[0].id if ItemObject.item_list else -1  # Default to the first item ID or -1 if empty
        #order_step = max(1, int(self.spinBox_step_position.value())) 
        #order_step_str = str(order_step)# Assuming outputParameters_new is a QLineEdit
        physical_features = {
            "parameter": self.parameterPhysicalFeatures.text().strip(),
            "value": self.valuePhysicalFeatures.text().strip()
        } # Assuming parameterPhysicalFeatures is a QLineEdit
        new_step_data = {
            "object_name": object_name,
            
            "action": action,
            "order_step": order_step,
            "executed_by": executed_by,
            "output_state": output_param,
            "physical_features": physical_features
        }
        #self.step_saved_signal.emit(new_step_data)
        #self.accept()
    # Flags for validation
        is_valid = True

    # Validate each field, and show red border if validation fails
        if not object_name:
            self.new_object.setStyleSheet("border: 2px solid red;")
            is_valid = False
        else:
            self.new_object.setStyleSheet("")

        if not action:
            self.action_new.setStyleSheet("border: 2px solid red;")
            is_valid = False
        else:
            self.action_new.setStyleSheet("")

        #if not executed_by:
            #self.executedBy_new.setStyleSheet("border: 2px solid red;")
            #is_valid = False
        #else:
            #self.executedBy_new.setStyleSheet("")

        #if not output_param:
            #self.outputParameters_new.setStyleSheet("border: 2px solid red;")
            #is_valid = False
        #else:
            #self.outputParameters_new.setStyleSheet("")

        #if not physical_features:
            #self.parameterPhysicalFeatures.setStyleSheet("border: 2px solid red;")
            #is_valid = False
        #else:
            #self.parameterPhysicalFeatures.setStyleSheet("")
        
            # Generate a new ID for the procedure step
              
    # If all inputs are valid, proceed to save or update data
        if is_valid:
            try:
            # Retrieve the selected procedure and phase
                procedure_index = self.belonging_to_procedure_select.currentIndex()
                procedure_id = self.belonging_to_procedure_select.itemData(procedure_index)

            # Get the specified `order_step` and ensure it is within valid bounds
                order_step = max(1, int(self.spinBox_step_position.value()))
                #order_step = int(self.spinBox_step_position.value())
            # Fetch existing steps for the procedure, sorted by `order_step`
                current_step_list = [
                    obj for obj in self.procedure_step_list
                    if obj is not None and obj.procedure_id == procedure_id
                ]
                if not current_step_list:
                    order_step = 1
                sorted_procedure_step_list = sorted(
                    [step for step in current_step_list if step.order_step is not None],
                    key=lambda x: int(x.order_step)
                )

            # Shift the order of existing steps down if the specified `order_step` already exists
                for step in sorted_procedure_step_list:
                    if int(step.order_step) >= order_step:
                        step.order_step = int(step.order_step) + 1
                        ProcedureStepObject.edit_procedure_step(  # Update in-memory and database
                            step.id,
                            object_name=step.object_name,
                            action=step.action,
                            order_step=step.order_step,
                            executed_by=step.executed_by,
                            required_input_state=step.required_input_state,
                            output_state=step.output_state,
                            physical_features=step.physical_features,
                            rationale=step.rationale,
                            comments=step.comments,
                            change_history=step.change_history,
                            procedure_id=step.procedure_id,
                            item_id=step.item_id
                        )

            # Generate a new ID for the new procedure step
                new_step_id = ProcedureStepObject.generate_id()

            # Save the new step at the specified `order_step`
                ProcedureStepObject.new_entry(
                    ObjectName=object_name,
                    Action=action,
                    OrderStep=order_step,
                    ExecutedBy=executed_by,
                    RequiredInputState=required_input_state,
                    OutputState=output_param,
                    PhysicalFeatures=physical_features,
                    Rationale=rationale,
                    Comments=comments,
                    ChangeHistory=change_history,
                    ProcedureID=procedure_id,
                    ItemID=item_id
                )

            # Refresh the step list in memory and UI to show the updated order
                ProcedureStepObject.create_procedure_step_list()
                #self.populate_selected_procedure_step(procedure_id)
                if hasattr(self, 'change_signal_procedure_dialog'):
                    self.change_signal_procedure_dialog.emit()
            # Notify the user of successful save
                #QtWidgets.QMessageBox.information(None, "Success", "Procedure step saved successfully.")
                #print("Procedure step saved successfully.")
                self.accept()
            except Exception as e:
                #print(f"Error saving procedure step: {str(e)}")  # Debug print instead of message box
                #QtWidgets.QMessageBox.critical(None, "Error", f"Failed to save procedure step: {str(e)}")
                print(f"Failed to save procedure step: {e}")
        else:
            print("Validation failed: object_name and action are required.")
    def validate_fields(self):
        object_name = self.new_object.text().strip()
        action = self.action_new.text().strip()
        #executed_by = self.executedBy_new.text().strip()
        

    # Only enable the save button if required fields are filled
        if object_name and action:
           self.buttonBox_new_step.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(True)
           return True
        else:
           self.buttonBox_new_step.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)
           return False 
    def accept(self):
        # Validate inputs or perform necessary actions
        if self.validate_fields():
            self.valid_flag = True
            self.change_signal_procedure_dialog.emit()
            super().accept()  # Call QDialog's accept method to close the dialog
        else:
            reurn
            #QtWidgets.QMessageBox.warning(self, "Invalid Input", "Please check the input.")

    #def update_system_display(self, provides, requires, turns_off):
        
        # Update the UI labels for provides, requires, and turns off
        #self.provides_display.setText("\n".join(provides) if provides else "No systems selected")
        #self.requires_display.setText("\n".join(requires) if requires else "No systems selected")
        #self.turnsoff_display.setText("\n".join(turns_off) if turns_off else "No systems selected")     

    def refresh_ui(self):
      
        self.type_of_operation_list = TypeOfOperationObject.type_of_operation_list
        self.phase_list = PhaseObject.phase_list
        self.procedure_list = ProcedureObject.procedure_list
        self.procedure_step_list =ProcedureStepObject.procedure_step_list
        self.checkpoint_list =CheckpointObject.checkpoint_list
        (
            self.item_list,
            self.procedure_list,
            self.procedure_step_list,
            self.type_of_operation_list,
            self.system_state_list,
            self.phase_list,
            self.checkpoint_list,
        ) = update_lists()

        
        #if self.phase_list:
            #selected_phase_id = self.get_selected_phase_id()
            #self.populate_procedure_combo_box(selected_phase_id)

        #if self.type_of_operation_list:
            #selected_operation_type = self.get_selected_operation_type()
            #self.populate_flight_phase_combo_box(selected_operation_type)
        # Refresh combo boxes or lists in the UI
        #self.object_combo.clear()
        #self.object_combo.addItems([item.name for item in item_list])
    
    #def open_system_dialog(self):

        #print("Opening system dialog...")  # Debug print statement
    # Create an instance of the DialogSystem dialog
        #dialog = DialogSystem(self)
    
    # Connect the signal from the DialogSystem to update the UI after changes
        #dialog.change_signal_systems.connect(self.update_system_display)

    # Open the dialog as modal
        #dialog.exec_()
        #print("System dialog closed.") 

    #def add_test_flight_phase(self):
        """
          Adds a test flight phase to the database for testing the functionality.
        """
        #session = Database.get_session()

      # Fetch a TypeOfOperation if one exists, or create a new one
        #operation = session.query(TypeOfOperation).first()
        #if not operation:
        # Create a new operation if none exists
            #operation = TypeOfOperation(
            #type_of_operation="Test Operation",
                #type_of_mission="Test Mission",
                #references="Test References",
                #comments="Test Comments",
                #phase_list=[]
            #)
            #session.add(operation)
            #session.commit()  # Commit the operation first to assign an ID

    # Create a new flight phase and link it to the existing TypeOfOperation
        #new_phase = Phase(
            #name="",
            #order_number="1",
            #input_state="Initial",
            #output_state="Final",
            #procedure_list=[],
           #type_of_operation_id=operation.id
        #)

    # Add the new phase to the operation's phase list
        #operation.phase_list.append({"name": new_phase.name, "order_number": new_phase.order_number})

        #session.add(new_phase)
        #session.commit()  # Commit the new phase to the database
        

        #print("Test flight phase added successfully.")
        #self.populate_flight_phase_combo_box(operation.type_of_operation)
        #self.add_test_flight_phase()
        #session.close()
    def get_step_data(self):
        """Return a dictionary with the step data collected from the dialog inputs."""
    
    # Print debug information directly from UI fields
        order_step = int(self.spinBox_step_position.value())
        action = self.action_new.text().strip()
        print(f"Object Name: {self.new_object.text().strip()}")
        print(f"Order Step: {self.spinBox_step_position.value()}")
        print(f"Action: {self.action_new.text().strip()}")
    
    # Return data dictionary
        return {
            "object_name": self.new_object.text().strip(),
            "order_step": order_step, #int(self.spinBox_step_position.value()),  # Ensure integer
            "action": action, #self.action_new.text().strip(),
            "executed_by": self.executedBy_new.text().strip(),
            "output_state": self.outputParameters_new.text().strip(),
            "physical_features": {
                "parameter": self.physicalFeatures_param.text().strip(),
                "value": self.physicalFeatures_value.text().strip()
            },
            "rationale": "",  # Default values as needed
            "comments": "",
            "required_input_state": "",
            "item_id": ItemObject.item_list[0].id if ItemObject.item_list else -1,
        }


def verify_order_and_action(self):
    if not isinstance(self.order_step, int) or not isinstance(self.action, str):
        raise ValueError("Order step must be an integer, and action must be a string")
    if self.order_step < 0:
        raise ValueError("Order step cannot be negative")    



    

