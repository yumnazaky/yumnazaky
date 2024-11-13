import sys
import os 
import math
import json
from functools import partial
import sqlite3, sqlalchemy
import traceback
import resources_rc


# get the current directory
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# get the directory of GUI (which is in a sibling folder)
GUI_path = os.path.join(current_dir, "gui")
module_path = os.path.join(current_dir,"modules")# add GUI path to the system path
sys.path.append(GUI_path) 
sys.path.append(module_path)

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QInputDialog,QVBoxLayout,QWidget

from PyQt5.QtCore import pyqtSignal

from container import StepContainerWidget


from PyQt5.QtWidgets import QMessageBox  # Correct import for QMessageBox
#from enter_new_flight_phase_ui import Ui_Dialog
from enter_new_operation_dialog_ui import Ui_New_operation_type

from enter_procedure_functionalities import newProcedure
from operatio_type_database import DbTypeOfOperationEdition# Import the dialog code
from mainwindow1_ui import Ui_flightFlow_main_window
from flight_phase_functions import FlightPhaseWidget
from flightphase_step import Ui_FlightPhaseStep
from update_databases import update_lists
from update_databases import create_requirements_list
from warning_2 import warningContainer
from procedure_step import FlightPhaseStep
from new_step_functionalties import newStep_dialog
from enter_new_flight_phase_functionalties1 import EnterNewPhaseDialog
from Database1 import TypeOfOperation, Phase, Item, SystemState, Checkpoint, Procedure, ProcedureStep, Database
#from database_selection import TypeOfOperationDialog
from enter_database import TypeOfOperationDialog
from system_functionalties_2 import DialogSystem
from define_object_classes import TypeOfOperationObject, PhaseObject, ProcedureStepObject, SystemStateObject, ItemObject, CheckpointObject, ProcedureObject
from comments_for_procedures11 import Ui_DialogProceduresComments  
from reference_for_procedures import Ui_DialogReferencesProcedure
from Checkpoint_Input_Manager import CheckpointManager
class FlightFlowMainWindow(QMainWindow, Ui_flightFlow_main_window):
    item_list=[]
    procedure_list=[]
    procedure_step_list=[]
    type_of_operation_list=[]
    system_state_list=[]
    phase_list=[]
    checkpoint_list=[]
    selected_phase_id=None
    #change_signal_phase = pyqtSignal()
    def __init__(self, parent=None):
        super(FlightFlowMainWindow, self).__init__(parent)
        

         
        #self.ui.setupUi(self)
        self.ui =Ui_flightFlow_main_window
        self.setupUi(self) 
      
        #if not ItemObject.item_list:
            #ItemObject.initialize_default_systems()
        #print("Initialized main ItemObject.item_list:", [(item.id, item.name) for item in ItemObject.item_list])
        
        #self.open_database_selection_dialog()
        self.setup_context_menu()
        self.saved_systems_by_step = {}
        self.new_tab_input = []
        self.selected_procedure_id = None
        self.type_of_operation_id = None
        self.remove_normal_operations_tab()
        self.step_widget_map = {}
        
        #self.saved_systems_by_step = {}
        
        #self.phase_widget = QtWidgets.QWidget(self)  
        
        # Now assign the container_layout to phase_widget
        #self.container_layout = QtWidgets.QVBoxLayout(self.phase_widget)
       
        # Now assign the container_layout to phase_widget
        #self.container_layout = QtWidgets.QVBoxLayout(self.phase_widget)
        refresh_layout_signal = QtCore.pyqtSignal()
        self.newOperationType_button.clicked.connect(self.open_new_operation_type_dialog)
        self.new_procedure_button.clicked.connect(self.open_new_procedure_dialog)
        #self.comboBox_flight_phases.currentIndexChanged.connect(self.reload_all)
        #self.change_signal_phase.connect(self.on_phase_order_changed)
        self.comboBox_flight_phases.currentIndexChanged.connect(self.on_phase_changed)
        #ItemObject.item_updated.connect(lambda: self.populate_warning_view(self.selected_procedure_id, self.type_of_operation_id))
        # In your setup method (constructor or setupUi)
        self.newFlightPhase_button.clicked.connect(self.open_new_flight_phase_dialog)
        self.flightPhases_tabs.tabCloseRequested.connect(self.confirm_close_tab)
        # Connect the reload button to a method
        self.reload_button.clicked.connect(self.reload_all)  # Assuming self.reload_button is the QToolButton

        #self.flightPhases_tabs.currentChanged.connect(self.populate_warning_view)

        #self.populate_flight_phases_combo_box(self.phase_list)  # Call this right after update_all_lists()
        # In your setup method (constructor or setupUi)
        self.reload.clicked.connect(self.reload_procedure_steps)
        self.new_procedureStep.clicked.connect(self.new_step_dialog)
        self.commentsProcedure_button.clicked.connect(self.open_comments_procedure_dialog)
        self.comboBox_procedures.currentIndexChanged.connect(self.on_procedure_changed)
        self.referencesProcedure_button.clicked.connect(self.open_references_procedure_dialog)
        #self.populate_warning_view(selected_procedure_id,type_of_operation_id)
        #self.populate_warning_view()
        
        if not self.open_database_selection_dialog():
        
            sys.exit()# Exit the application if the dialog was closed or rejected

        # Continue with the main window setup if the dialog was accepted
        #self.setupUi(Ui_flightFlow_main_window) 
        (
            self.item_list,
            self.procedure_list,
            self.procedure_step_list,
            self.type_of_operation_list,
            self.phase_list,
            self.system_state_list,
            self.checkpoint_list
        ) = update_lists()
        self.update_all_lists()
    def open_database_selection_dialog(self):
        database_dialog = TypeOfOperationDialog(self)
        #database_dialog.database_changed.connect(self.refresh_data_and_ui)
    # Show the dialog and check if it was accepted
        if database_dialog.exec_() == QDialog.Accepted:
            
            return True  # Main window should open
        else:
            return False  # Main window should not open

    
    

    def populate_flight_phases_combo_box(self, phase_list):
        
        try:
            self.comboBox_flight_phases.clear()

            if phase_list:
           
                for phase in phase_list:
                    self.comboBox_flight_phases.addItem(phase.name, phase.id)

       
        except Exception:
            print(f"Error populating flight phases combo box: {e}")
            traceback.print_exc()

    def on_phase_changed(self):
        # Get the selected phase ID from the phase combo box
        selected_phase_index = self.comboBox_flight_phases.currentIndex()
        selected_phase_id = self.comboBox_flight_phases.itemData(selected_phase_index)
        session = None 
        if selected_phase_id is None:
            return  # No phase selected, do nothing

        try:
            
            procedures = [procedure for procedure in ProcedureObject.procedure_list if procedure.phase_id == selected_phase_id]
 
        # Clear the current items in the combo box
            self.populate_procedure_combo_box(procedures)
            #self.comboBox_procedures.clear()

        # Add a default "Select Procedure" option
            #self.comboBox_procedures.addItem("Select Procedure", None)

        # Update the in-memory procedure list
            #self.procedure_list = procedures  # Store the fetched procedures in the in-memory list

        # Populate the combo box with procedure names and their IDs
            #for procedure in procedures:
                #self.comboBox_procedures.addItem(procedure.name, procedure.id)


        except Exception as e:
            print(f"Error fetching procedures: {e}")
             
    def populate_procedure_combo_box(self, procedures):
        """
        Populates the belonging_to_procedure_select combo box with procedures.
        """
    # Clear the procedure combo box before populating it
        self.comboBox_procedures.clear()

    # Add a default "Select Procedure" option
        self.comboBox_procedures.addItem("Select Procedure", None)

    # Populate the combo box with the fetched procedures
        for procedure in procedures:
            self.comboBox_procedures.addItem(procedure.name, procedure.id)
    


        
 
   
    def create_procedure_steps(self, num_instances, sorted_procedure_step_list):
        try:
            main_widget = self.findChild(QtWidgets.QWidget, "scrollAreaWidgetContents_4") 
             # Replace "MainWidgetName" with the main widget containing your layout
            step_container_layout = main_widget.findChild(QVBoxLayout, "verticalLayout_7") if main_widget else None
            if step_container_layout is None:
                print("Error: 'verticalLayout_7' not found in the UI.")
                return
            self.clear_layout(step_container_layout)
            #added_step_ids = set(widget.procedure_step_id for widget in self.get_widgets_of_type(step_container_layout, FlightPhaseStep))
            added_step_ids = set()
            self.print_layout_contents(step_container_layout)

        # Track IDs to prevent duplicates within the function itself
            #added_step_ids = set()  
            
                
            
            #step_container_layout = self.findChild(QVBoxLayout,"verticalLayout_7")
            step_container_layout.setContentsMargins(10, 10, 10, 10)  # Adjust margins as needed
            step_container_layout.setSpacing(0)
        # Iterate through sorted procedure steps
            #for i in sorted_procedure_step_list:
            for index, procedure_step in enumerate(sorted_procedure_step_list):
                if procedure_step is None or procedure_step.id in added_step_ids:
                    continue
                #if procedure_step is None:
                    #print(f"Warning: Encountered None procedure_step at index {index}. Skipping.")
                    #continue
                #if procedure_step.id in added_step_ids:
                    #print(f"Skipping duplicate step with ID: {procedure_step.id}")
                    #continue

            # Mark this step as added
                step_widget = self.create_step_widget(procedure_step)
                step_container_layout.addWidget(step_widget)
                added_step_ids.add(procedure_step.id)    
                step_widget.selection_complete.connect(lambda: self.populate_warning_view(self.selected_procedure_id, self.type_of_operation_id))
                order_step = index + 1  # Set order_step by incrementing the index
                procedure_step.order_step = order_step
                step_widget.move_up_signal.connect(self.refresh_step_layout)
                step_widget.move_down_signal.connect(self.refresh_step_layout)
                step_widget.change_signal_step.connect(self.refresh_step_layout)
                
                step_container = StepContainerWidget(step_widget)
                self.step_widget_map[procedure_step.id] = step_container
                
                step_container_layout.addWidget(step_container)
                
                self.add_checkpoints_to_container(step_container, procedure_step.id)
                

                #step_container_layout.insertWidget(0, procedure_step_widget)
            #spacer = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
            #step_container_layout.addSpacerItem(spacer)
            step_container_layout.addSpacerItem(
                QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
            )

               
        except Exception:
            traceback.print_exc()
    def insert_checkpoints_for_step(self, layout, procedure_step_id):
        """Adds checkpoints for a given procedure step below the step widget."""
        for checkpoint in CheckpointObject.checkpoint_list:
            if checkpoint.procedure_step_id == procedure_step_id:
                checkpoint_widget = self.create_checkpoint_widget(checkpoint)
                step_widget = self.step_widget_map.get(procedure_step_id)
                if step_widget:
                    index = layout.indexOf(step_widget)
                    layout.insertWidget(index + 1, checkpoint_widget)
                    checkpoint_widget.show()
                    print(f"Added checkpoint for step ID {procedure_step_id}")        
    def create_step_widget(self, procedure_step):
        """Creates and returns a FlightPhaseStep widget for a given procedure step."""
        step_widget = FlightPhaseStep(procedure_step.id)
        step_widget.selection_complete.connect(lambda: self.populate_warning_view(self.selected_procedure_id, self.type_of_operation_id))

    # Retrieve and handle physical features
        physical_features = procedure_step.physical_features
        if isinstance(physical_features, str):
            try:
                physical_features = json.loads(physical_features)
            except json.JSONDecodeError:
                print("Error decoding JSON for physical_features, using empty dictionary instead.")
                physical_features = {}
        elif not isinstance(physical_features, dict):
        # In case it's neither a string nor a dict, default to an empty dict
            print("Warning: Unexpected type for physical_features, using empty dictionary.")
            physical_features = {}

    # Populate the widget with procedure step data
        step_widget.ui.object_plainTextEdit.setPlainText(procedure_step.object_name)
        step_widget.ui.action_plainTextEdit.setPlainText(procedure_step.action)
        step_widget.ui.executedBy_plainTextEdit.setPlainText(procedure_step.executed_by)
        step_widget.ui.output_plainTextEdit.setPlainText(procedure_step.output_state)
        step_widget.ui.procedureStep_order.setText(str(procedure_step.order_step))
    
    # Populate physical features if they exist
        step_widget.ui.physicalFeatures_param.setPlainText(physical_features.get("parameter", ""))
        step_widget.ui.physicalFeatures_value.setPlainText(physical_features.get("value", ""))
        step_widget.move_up_signal.connect(lambda: self.move_step_up(procedure_step.id))
        step_widget.move_down_signal.connect(lambda: self.move_step_down(procedure_step.id))

        step_widget.update_initial_values()
        #step_widget.checkpoint_added.connect(self.add_checkpoint_below_step)
    
        return step_widget

    def get_widgets_of_type(self, layout, widget_type):
        #Retrieve all widgets of a certain type from a layout.
        widgets = []
        for i in range(layout.count()):
            item = layout.itemAt(i)
            widget = item.widget()
            if isinstance(widget, widget_type):
                widgets.append(widget)
        return widgets
 
    def create_new_operation_types(self, index):
        type_of_operation_name, ok = QInputDialog.getText(
            self, "New operation Type", " Enter operation name"
        )    
        if ok:
            TypeOfOperationObject.new_entry(type_of_operation_name)
            self.flightPhases_tabs.setCurrentIndex(self.flightPhases_tabs.count())
            if self.new_operation_has_procedures():
                self.reload_procedure_steps()
            else:
                print("No procedures available to reload for this new operation.")
    
    def populate_selected_procedure_step(self, procedure_id):
        try:
            print(f"Fetching procedure steps for procedure_id: {procedure_id}")
        
        # Fetch procedure steps by ID and filter them
            selected_procedure_step_list = [obj for obj in self.procedure_step_list if obj is not None and obj.procedure_id == procedure_id]
            if not selected_procedure_step_list:
                print(f"No procedure steps found for procedure_id: {procedure_id}")
                return
        
        # Sort procedure steps by order
            # Sort procedure steps by order, ensuring order_step is treated as an integer
            sorted_procedure_step_list = sorted(selected_procedure_step_list, key=lambda x: int(x.order_step))

            #sorted_procedure_step_list = sorted(selected_procedure_step_list, key=lambda x: x.order_step)
            seen_step_ids = set()
        # Clear the existing layout
            step_container_layout = self.findChild(QVBoxLayout, "verticalLayout_7")
            self.clear_layout(step_container_layout)
        
        # Call create_procedure_steps to create and add widgets for steps
            self.create_procedure_steps(len(sorted_procedure_step_list), sorted_procedure_step_list)

        # Handle associated checkpoints for each procedure step
            for procedure_step in sorted_procedure_step_list:
                print(f"Processing checkpoints for procedure_step with ID: {procedure_step.id}")
                checkpoints = [cp for cp in CheckpointObject.checkpoint_list if cp.procedure_step_id == procedure_step.id]
            
                for checkpoint in checkpoints:
                    checkpoint_widget = CheckpointManager(checkpoint.procedure_step_id, self)
                    #checkpoint_widget.load_existing_checkpoints()
                    #procedure_step_widget.checkpoint_added.connect(self.add_checkpoint_below_step)  # Load and display checkpoint data
                
                # Add checkpoint widget right below the corresponding step in the layout
                    step_container_layout.addWidget(checkpoint_widget)
                    #step_container_layout.insertWidget(0, procedure_step_widget)
                    print(f"Added checkpoint widget for procedure_step {procedure_step.id}")
    
        except Exception as e:
            print(f"Failed to populate procedure step: {e}")
            #QtWidgets.QMessageBox.critical(self, "Error", f"Failed to populate procedure step: {e}")
            traceback.print_exc()
    def create_checkpoint_widget(self, checkpoint):
        """Creates and returns a CheckpointManager widget for a given checkpoint."""
        checkpoint_widget = CheckpointManager(len(CheckpointObject.checkpoint_list) + 1, self)
        checkpoint_widget.create_checkpoint(
            checkpoint_name=checkpoint.name,
            item_state=checkpoint.item_state,
            person_state=checkpoint.person_state
        )
        return checkpoint_widget



        #layout.update()
    def add_checkpoints_to_container(self, step_container, procedure_step_id):
        """Add checkpoints for a given procedure step to the StepContainerWidget."""
        checkpoints = [cp for cp in CheckpointObject.checkpoint_list if cp.procedure_step_id == procedure_step_id]

        for checkpoint in checkpoints:
            if checkpoint.procedure_step_id == procedure_step_id:
                checkpoint_widget = self.create_checkpoint_widget(checkpoint)
                step_container.add_checkpoint(checkpoint_widget)    
    def clear_layout(self, layout):
        """Clears all widgets from the given layout."""
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.deleteLater()    
    def move_step_up(self, procedure_step_id):
        """Move the specified procedure step up in the list and refresh layout."""
        try:
        # Retrieve type_of_operation_id based on the current tab selection
            

        # Find index and move up if possible
            steps = ProcedureStepObject.procedure_step_list
            index = next((i for i, step in enumerate(steps) if step.id == procedure_step_id), None)

            if index is not None and index > 0:
            # Swap order values in the model and update list order
                steps[index].order_step, steps[index - 1].order_step = steps[index - 1].order_step, steps[index].order_step
                steps[index], steps[index - 1] = steps[index - 1], steps[index]

            # Refresh the UI immediately
                self.refresh_step_layout()
            else:
                print(f"No movement possible for step ID {procedure_step_id} (index {index})")
        # Now call populate_warning_view with both arguments
           
        except Exception as e:
            print(f"Error in move_step_up: {e}")

    def move_step_down(self, procedure_step_id):
    
        try:
        # Retrieve type_of_operation_id based on the current tab selection
           
        # Find index and move down if possible
            steps = ProcedureStepObject.procedure_step_list
            index = next((i for i, step in enumerate(steps) if step.id == procedure_step_id), None)

            if index is not None and index < len(steps) - 1:
            # Swap order values in the model and update list order
                steps[index].order_step, steps[index + 1].order_step = steps[index + 1].order_step, steps[index].order_step
                steps[index], steps[index + 1] = steps[index + 1], steps[index]

            # Refresh the UI immediately
                self.refresh_step_layout()

        # Now call populate_warning_view with both arguments
            else:
                print(f"No movement possible for step ID {procedure_step_id} (index {index})")

        except Exception as e:
            print(f"Error in move_step_down: {e}")


    

    #def refresh_step_layout(self):
        #"""Refreshes the layout to reflect the updated order of step containers."""
        #layout = self.findChild(QVBoxLayout, "verticalLayout_7")
        #if layout is None:
            #print("Error: 'verticalLayout_7' not found.")
            #return
        # Clear layout
            #while layout.count():
                #item = layout.takeAt(0)
                #widget = item.widget()
                #if widget:
                    #widget.setParent(None)
        
        # Re-add steps in sorted order based on `order_step`
            #sorted_steps = sorted(ProcedureStepObject.procedure_step_list, key=lambda x: x.order_step)
            #self.create_procedure_steps(sorted_steps)
        #layout.addSpacerItem(QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))
        # Add a spacer at the end
    def refresh_step_layout(self):
        """Refreshes the layout to reflect the updated order of step containers."""
        layout = self.findChild(QVBoxLayout, "verticalLayout_7")
        if layout is None:
            print("Error: 'verticalLayout_7' not found.")
            return
    
    # Sort steps by order, then re-add them in the sorted order
        
    # Clear the layout only for widgets currently in `layout`
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)

    # Re-add widgets in the sorted order based on `order_step`
        sorted_steps = sorted(ProcedureStepObject.procedure_step_list, key=lambda x: int(x.order_step))
        self.create_procedure_steps(len(sorted_steps), sorted_steps)


    # Add a spacer at the end to keep layout consistent
        layout.addSpacerItem(QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))
       

    def get_checkpoint_widget(self, procedure_step_widget):
        """Retrieve the checkpoint widget associated with the given procedure step."""
        for i in range(self.verticalLayout.count()):
            widget = self.verticalLayout.itemAt(i).widget()
            if isinstance(widget, CheckpointManager) and widget.step_id == procedure_step_widget.procedure_step.id:
                return widget
        return None        

    def on_procedure_changed(self):
        self.comboBox_procedures.blockSignals(True)
        # Get the selected procedure ID from the procedures combo box
        #self.comboBox_procedures.currentIndexChanged.disconnect(self.on_procedure_changed)
        selected_procedure_index = self.comboBox_procedures.currentIndex()
        selected_procedure_id = self.comboBox_procedures.itemData(selected_procedure_index)

        if selected_procedure_id is not None:
            #step_container_layout = self.findChild(QVBoxLayout, "verticalLayout_7")
            #self.clear_layout(step_container_layout)
            
              # No procedure selected, do nothing
            self.populate_selected_procedure_step(selected_procedure_id)
        #self.disable_comments_button()
        #self.disable_references_buttons()    

        # Assuming you have a way to get the type_of_operation_id from the current context
        current_tab_index = self.flightPhases_tabs.currentIndex()
        if current_tab_index == -1 or current_tab_index >= len(self.new_tab_input):
            type_of_operation_id = self.new_tab_input[current_tab_index]["id"]
            self.populate_warning_view(selected_procedure_id, type_of_operation_id)

            #QtWidgets.QMessageBox.warning(self, "Error", "No valid operation selected.")
            #return 
        #type_of_operation_id = self.new_tab_input[current_tab_index]["id"]
        #if type_of_operation_id is not None:
           # self.populate_warning_view(selected_procedure_id, type_of_operation_id)
        #else:
            #QtWidgets.QMessageBox.warning(self, "Error", "Invalid operation ID.")
        # Now, call populate_warning_view with both the procedure and operation ID
        #self.flightPhases_tabs.currentChanged.connect(
            #lambda: self.populate_warning_view(
                #self.comboBox_procedures.currentData(),  # procedure_id
                #self.new_tab_input[self.flightPhases_tabs.currentIndex()]["id"]  # operation_id
            #)
        #)
        #try:
        # Filter the procedure steps based on the selected procedure
           # self.populate_selected_procedure_step(selected_procedure_id)
            #self.populate_warning_view(selected_procedure_id, type_of_operation_id)    
        #except Exception:
            #traceback.print_exc()
        self.comboBox_procedures.blockSignals(False)

    def new_step_dialog(self):
    
        try:
            current_tab_index = self.flightPhases_tabs.currentIndex()

        # Check if an operation is selected
            if current_tab_index == -1 or current_tab_index >= len(self.new_tab_input):
                QtWidgets.QMessageBox.warning(self, "No Operation Selected", "Please create or select an operation type first.")
                new_step_dialog = newStep_dialog(None, None, self)
                new_step_dialog.disable_all_inputs()  # Disable inputs if no valid operation is selected
                new_step_dialog.exec_()
                return

        # Retrieve selected operation ID
            selected_operation_id = self.new_tab_input[current_tab_index]["id"]
            print(f"Selected operation ID: {selected_operation_id}")

        # Get the selected phase in the context of the current operation
            selected_phase_index = self.comboBox_flight_phases.currentIndex()
            selected_phase_id = self.comboBox_flight_phases.itemData(selected_phase_index)

        # If no phase is selected, show a warning and disable inputs
            if selected_phase_id is None:
                QtWidgets.QMessageBox.warning(self, "No Phase Selected", "Please select a valid phase.")
                new_step_dialog = newStep_dialog(selected_operation_id, None, self)
                new_step_dialog.disable_all_inputs()  # Disable inputs if no valid phase is selected
            else:
            # Create an instance of newStep_dialog and pass the operation and phase context
                new_step_dialog = newStep_dialog(selected_operation_id, selected_phase_id, self)
                new_step_dialog.enable_all_inputs()  # Enable inputs if valid operation and phase are selected

        # Execute the dialog and handle the result
            result = new_step_dialog.exec_()
            if result == QDialog.Accepted and new_step_dialog.valid_flag:
                step_data = new_step_dialog.get_step()

            # Before adding, check current step list size to help detect duplication
                print(f"Step count before adding: {len(ProcedureStepObject.procedure_step_list)}")
                if step_data:
            # Add the new step to the ProcedureStepObject
                    ProcedureStepObject.new_entry(
                        ObjectName=step_data.get('object_name'),
                        Action=step_data.get('action'),
                        OrderStep=step_data.get('order_step'),
                        ExecutedBy=step_data.get('executed_by'),
                        RequiredInputState=step_data.get('required_input_state'),
                        OutputState=step_data.get('output_state'),
                        PhysicalFeatures=step_data.get('physical_features'),
                        ChangeHistory=[],  # Start with an empty change history for the new step
                        ProcedureID=selected_procedure_id,  # Use the selected phase ID
                        Rationale=step_data.get('rationale', ""),
                        Comments=step_data.get('comments', ""),
                        ItemID=step_data.get('item_id', -1)
                    )

                    print(f"Step count after adding: {len(ProcedureStepObject.procedure_step_list)}")
                #new_step_dialog.step_saved_signal.connect(lambda: self.reload_procedure_steps())

            # Call populate_selected_procedure_step only once to refresh the view with the new step
                    self.populate_selected_procedure_step(selected_procedure_id)

        except IndexError:
            QtWidgets.QMessageBox.warning(self, "Operation Selection Error", "Please create or select an operation first.")
        except Exception as e:
            print(f"Error opening new step dialog: {e}")
         
    def remove_normal_operations_tab(self):
        tab_count = self.flightPhases_tabs.count()

        # Find and remove the 'normal_operations' tab
        for index in range(tab_count):
            if self.flightPhases_tabs.tabText(index) == "normal_operations":
                self.flightPhases_tabs.removeTab(index)
                break

    def add_operation_type(self):
        try:
            try:
                self.flightPhases_tabs.currentChanged.disconnect()
            except TypeError:
                pass
        # Clear existing tabs

            self.flightPhases_tabs.clear()
            self.new_tab_input.clear()

            self.update_all_lists()

            print("hena 1")
        # Iterate over the type of operation list to create new tabs
            for type_of_operation in self.type_of_operation_list:
                new_tab = QtWidgets.QWidget()
                #new_tab.setContentsMargins(0,0,0,0)
                #new_tab.setMinimumSize(350,1500)
                new_tab_layout = QtWidgets.QVBoxLayout(new_tab)
                new_tab_layout.setContentsMargins(0, 0, 0, 0)
                new_tab_layout.setSpacing(0)

                scroll_area = QtWidgets.QScrollArea(new_tab)
                scroll_area.setContentsMargins(0,0,0,0)
                scroll_area.setWidgetResizable(True)
                scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
                scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)

                container_widget =QtWidgets.QWidget(scroll_area)
                container_widget.setObjectName("container_widget")
                #container_widget.setContentsMargins(0,0,0,0)
                
                container_layout = QtWidgets.QVBoxLayout(container_widget)
                container_layout.setContentsMargins(2, 2, 2, 2)
                container_layout.setSpacing(0)
                
                #container_widget.setMaximumSize(400,1450)
                
        
                scroll_area.setWidget(container_widget)
                new_tab_layout.addWidget(scroll_area)
                operation_phases = [phase for phase in self.phase_list if phase.type_of_operation_id == type_of_operation.id]
                self.create_flight_phase_widget(operation_phases, container_layout)
                self.flightPhases_tabs.addTab(new_tab, type_of_operation.type_of_operation)
       
            # Store the operation type name and ID for later use
                self.new_tab_input.append({"name": type_of_operation.type_of_operation, "id": type_of_operation.id})
                operation_phases = [phase for phase in self.phase_list if phase.type_of_operation_id == type_of_operation.id]
                self.create_flight_phase_widget(operation_phases, container_layout)

                print("hena 2")

                if self.new_tab_input:
                    self.flightPhases_tabs.currentChanged.connect(
                    lambda index: self.populate_warning_view(
                        self.comboBox_procedures.currentData(),  # procedure_id
                        self.new_tab_input[self.flightPhases_tabs.currentIndex()]["id"]  # operation_id
                    )
                )
                else:
                    #QtWidgets.QMessageBox.warning(self, "Error", "No operation tabs found to populate.")
                    print("No operation tabs found to populate.")
                #self.reload_all()
        except Exception as e:
            print(f"Failed to add operation types: {e}")
            #QtWidgets.QMessageBox.critical(self, "Error", f"Failed to add operation types: {e}")
            traceback.print_exc()   
        # Connect the signal to the fill_warning_view method
        #self.flightPhases_tabs.currentChanged.connect(
            #lambda index: self.populate_warning_view(self.comboBox_procedures.currentData(), self.new_tab_input[self.flightPhases_tabs.currentIndex()]["id"])
        #)
        
        #self.reload_all()
    def create_flight_phase_widget(self, phase_list, container_layout):
       
        #Creates flight phase widgets for the given phase list.

      
     
        while container_layout.count():
            item = container_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        if not phase_list:
            QtWidgets.QMessageBox.warning(self, "No Phases", "No phases found to display.")
            return

        sorted_phase_list = sorted(phase_list, key=lambda x: x.order_number)

    # Make sure the layout doesn't have unnecessary margins
        container_layout.setContentsMargins(0, 0, 0, 0)  # Remove any margin
        container_layout.setSpacing(0)  # Minimal space between widgets


        for phase in sorted_phase_list:
            try:
                # Add check for procedure_id if it's required for certain logic
                 
                phase_widget = FlightPhaseWidget(phase.id, phase.name)
                phase_widget.setFixedSize(350, 120)  # Ensure size is fixed as per requirement
                phase_widget.move_up_signal.connect(lambda phase_id=phase.id: self.handle_move_up(phase_id,container_layout))
                phase_widget.move_down_signal.connect(lambda phase_id=phase.id: self.handle_move_down(phase_id, container_layout))
            # Add the widget to the layout with alignment at the top
                container_layout.addWidget(phase_widget, alignment=QtCore.Qt.AlignTop)
                
            # Add minimal spacer between widgets
                spacer_item = QtWidgets.QSpacerItem(0, 8, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
                container_layout.addItem(spacer_item)

                print(f"Widget size: {phase_widget.size()}")
            except Exception as e:
                print(f"Error adding FlightPhaseWidget for phase {phase.name}: {e}")

    # Ensure that everything aligns to the top and fills from the top of the layout
        container_layout.setAlignment(QtCore.Qt.AlignTop)
    def handle_move_up(self, phase_id, container_layout):
        # Find the specific phase and move it up
        if PhaseObject.move_up(phase_id):
        # Retrieve updated phases for the current operation and refresh only this tab's layout
            current_operation_id = self.new_tab_input[self.flightPhases_tabs.currentIndex()]["id"]
            operation_phases = [phase for phase in self.phase_list if phase.type_of_operation_id == current_operation_id]
            self.create_flight_phase_widget(operation_phases, container_layout)

    def handle_move_down(self, phase_id, container_layout):
        # Find the specific phase and move it down
        if PhaseObject.move_down(phase_id):
        # Retrieve updated phases for the current operation and refresh only this tab's layout
            current_operation_id = self.new_tab_input[self.flightPhases_tabs.currentIndex()]["id"]
            operation_phases = [phase for phase in self.phase_list if phase.type_of_operation_id == current_operation_id]
            self.create_flight_phase_widget(operation_phases, container_layout)

        
    def add_flight_phase(self, type_of_operation_id, phase_name, order_number, input_state, output_state):
        
        if not phase_name.strip():
            #QtWidgets.QMessageBox.warning(self, "Input Error", "Phase name cannot be empty.")
            print("Phase name cannot be empty.")
            return

    
        if not isinstance(order_number, int) or order_number <= 0:
            #QtWidgets.QMessageBox.warning(self, "Input Error", "Order number must be a positive integer.")
            print("Order number must be a positive integer.")
            return
        #session = Database.get_session()
        for phase in self.phase_list:
            if phase.type_of_operation_id == type_of_operation_id and phase.order_number >= order_number:
                phase.order_number += 1  # Shift the order number of phases after the inserted phase
                PhaseObject.edit_phase(
                phase.id,
                phase.name,
                phase.order_number,
                phase.input_state,
                phase.output_state,
                phase.procedure_list,
                phase.type_of_operation_id
            )
        #try:
        # Create new flight phase and link to operation
        new_phase  =  PhaseObject.new_entry(
            Name=phase_name,
            OrderNumber=order_number,
            InputState=input_state,
            OutputState=output_state,
            ProcedureList=[],  # Empty procedure list initially
            TypeOfOperationID=type_of_operation_id
        )
            #session.add(new_phase)
            #session.commit()
        if new_phase:
            self.phase_list.append(new_phase)
            self.phase_list = sorted(self.phase_list, key=lambda p: p.order_number)
            print(f"New phase '{phase_name}' added with order number {order_number}.")
            self.create_flight_phase_widget(self.phase_list, self.container_layout)
        # Reload the tabs to reflect the new phase
            #self.add_operation_type()
        #self.load_phases(type_of_operation_id)

        #QtWidgets.QMessageBox.information(self, "Success", "New flight phase added successfully.")
        print("New flight phase added successfully.")
    #def open_new_operation_dialog(self):
        # Create the dialog and its UI
        #dialog = QtWidgets.QDialog()
        #dialog_ui = Ui_New_operation_type()
        #dialog_ui.setupUi(dialog)

       # Connect buttons to the accept/reject handlers
        #dialog_ui.new_operation_buttonBox.accepted.connect(lambda: self.get_new_operation_data(dialog_ui, dialog))
        #dialog_ui.new_operation_buttonBox.rejected.connect(dialog.reject)
    
        # Show the dialog and wait for the user's input
        #dialog.exec_()
    def open_new_flight_phase_dialog(self):
        # Create an instance of the EnterNewPhaseDialog
        dialog = EnterNewPhaseDialog(self)
        dialog.fillOperationComboBox() 
    # Show the dialog and wait for the user's input
        result = dialog.exec_()

    # Check if the dialog was accepted and the user entered valid data
        if result == QDialog.Accepted:
        # Reload necessary data or update the UI
            self.reload_all()
    #def on_phase_order_changed(self):
    # Recreate the flight phase widgets to reflect the updated order
        #self.create_flight_phase_widget(self.phase_list, self.container_layout) 

    def confirm_close_tab(self, index):
        
        print(f"Current tab index: {index}")
        print(f"Total tabs: {len(self.new_tab_input)}")
        if index >= len(self.new_tab_input) or index < 0:
            print("Invalid tab index.")
            #QtWidgets.QMessageBox.warning(self, "Error", "Invalid tab index.")
            return

    # Get the name of the operation type (the tab label)
        tab_label = self.flightPhases_tabs.tabText(index)
        tab_info = self.new_tab_input[index]
        type_of_operation_name = tab_info["name"]
        type_of_operation_id = tab_info["id"]

    # Create a confirmation dialog
        reply = QtWidgets.QMessageBox.question(
            None, "Close Tab", f"Are you sure you want to close the operation type '{tab_label}'?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )

        if reply == QtWidgets.QMessageBox.Yes:
            self.flightPhases_tabs.removeTab(index)
            self.delete_type_of_operation(type_of_operation_id)
            del self.new_tab_input[index]  # Remove the tab info from the list


    def delete_type_of_operation(self, type_of_operation_id):
        # Fetch the type of operation by its ID and delete it
        type_of_operation = TypeOfOperationObject.return_type_of_operation(type_of_operation_id)
        if type_of_operation:
            type_of_operation.delete()
    def get_new_type_of_operation_data(self, dialog_ui, dialog):
        """Handles adding a new operation tab and saving it to the database."""
        new_type_of_operation = dialog_ui.enter_new_operation_lineEdit.text().strip()

        if new_type_of_operation:
        # Call the function to add a new tab in the UI
            self.add_operation_type(new_type_of_operation)

        # Now, update the database and background in-memory list
            try:
            # Save the new operation to the database and update in-memory list
                TypeOfOperationObject.save_operation(
                    operation_type=new_type_of_operation,
                    mission_type="",  # Empty since the dialog only opens a new tab
                    references="",  # Default empty value
                    comments=""  # Default empty value
                )
                # Reload the in-memory list from the database
                TypeOfOperationObject.create_type_of_operation_list()

                # Optionally print or log the updated operation list for debugging
                TypeOfOperationObject.print_table()
                self.update_operation_lists()
                self.fillOperationComboBox()

            except Exception as e:
                # Rollback in case of error and display a message
                print(f"Failed to add new operation: {e}")
                #QtWidgets.QMessageBox.critical(dialog, "Error", "Failed to save the operation type. Please try again.")
                return

            # If everything goes well, close the dialog
            dialog.accept()
        else:
           # Warn the user if the input is empty
    

         QtWidgets.QMessageBox.warning(dialog, "Warning", "Please enter a valid operation type.")
    

    
    def setup_context_menu(self):
        # Set up the context menu for the tab widget
        self.flightPhases_tabs.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.flightPhases_tabs.customContextMenuRequested.connect(self.show_tab_context_menu)

    def show_tab_context_menu(self, point):
        # Get the index of the tab where the right-click occurred
        tab_index = self.flightPhases_tabs.tabBar().tabAt(point)

        if tab_index != -1:
            # Create the context menu
            context_menu = QMenu(self)

            # Add the rename action to the context menu
            rename_action = QAction("Rename", self)
            context_menu.addAction(rename_action)

        # Connect the rename action to the rename function
            rename_action.triggered.connect(lambda: self.change_tab_name(tab_index))

        # Show the context menu at the right-click position
            context_menu.exec_(self.flightPhases_tabs.mapToGlobal(point))
    def on_operation_changed(self):
        current_tab_index = self.flightPhases_tabs.currentIndex()
        if current_tab_index == -1:
            return
        type_of_operation_id = self.new_tab_input[current_tab_index]["id"]
        self.load_phases(type_of_operation_id)
    def load_phases(self, type_of_operation_id):
        #session = Database.get_session()
        try:

            #phases = session.query(Phase).filter_by(type_of_operation_id=type_of_operation_id).all()
            filtered_phases = [
                phase for phase in PhaseObject.phase_list if phase.type_of_operation_id == type_of_operation_id
            ]
            self.populate_flight_phases_combo_box(filtered_phases)
        #finally:
            #session.close()
        except Exception as e:
            pass
            #QtWidgets.QMessageBox.critical(self, "Error", f"Failed to load flight phases: {e}")    
    def load_procedures(self, selected_phase_id):
        #session = Database.get_session()
        try:
            #procedures = session.query(Procedure).filter_by(phase_id=selected_phase_id).all()
            filtered_procedures = [
                procedure for procedure in ProcedureObject.procedure_list if procedure.phase_id == selected_phase_id
            ]

            self.populate_procedures_combo_box(filtered_procedures)
        #finally:
            #session.close()
        except Exception as e:
            #QtWidgets.QMessageBox.critical(self, "Error", f"Failed to load procedures: {e}")    
            pass
    
    def change_tab_name(self, index):
        dialog = QDialog()
        layout = QVBoxLayout(dialog)
    
    # Create the label and input field
        label = QLabel("Enter new tab name:")
        line_edit = QLineEdit()
    
    # Create the OK button
        button = QPushButton("OK")
    
    # Add the label, input field, and button to the layout
        layout.addWidget(label)
        layout.addWidget(line_edit)
        layout.addWidget(button)
    
    # Define the function to update the tab name
        def update_tab_name():
            new_name = line_edit.text().strip()
            if new_name:
            # Update the tab's name in the UI
                self.flightPhases_tabs.setTabText(index, new_name)
            
            # Get the tab information and update it in memory and in the database
                tab_info = self.new_tab_input[index]
                TypeOfOperationObject.edit_type_of_operation(tab_info["id"], new_name, tab_info["type_of_mission"], "", "", tab_info["phase_list"])
            
            # Update the local in-memory list as well
                self.new_tab_input[index]["name"] = new_name

            dialog.close()

        # Connect the OK button click to the update function
        button.clicked.connect(update_tab_name)
    
        # Show the dialog
        dialog.exec_()

    def open_new_operation_type_dialog(self):
        """Opens the 'New Operation Type' dialog."""
        dialog = QtWidgets.QDialog(self)  # Create a QDialog instance with self as parent
        dialog_ui = Ui_New_operation_type()  # Create an instance of the dialog's UI
        dialog_ui.setupUi(dialog)  # Set up the dialog UI

    # Handle the OK/Cancel button press
        dialog_ui.new_operation_buttonBox.accepted.connect(
            lambda: self.save_new_operation_type(dialog_ui.enter_new_operation_lineEdit.text(), dialog)
        )
        dialog_ui.new_operation_buttonBox.rejected.connect(dialog.reject)

    # Show the dialog modally
        dialog.exec_()

    def update_operation_types(self):
        # Update the operation types in the combo box for the New Phase dialog
        self.update_operation_lists()  # Refresh your local data
        #self.fillOperationComboBox() 
        self.populate_flight_phases_combo_box(self.phase_list)  


    def save_new_operation_type(self, new_operation_type, dialog):
        """Saves the new operation type entered by the user and creates a new tab."""
        if new_operation_type.strip():  # Validate non-empty input
        # Check if the operation type already exists in memory
            # Check if the operation type already exists and append a suffix if it does
            duplicate_count = sum(1 for op in self.type_of_operation_list if op.type_of_operation == new_operation_type)

            if duplicate_count > 0:
                new_operation_type = f"{new_operation_type} ({duplicate_count + 1})"  # Add a suffix to make it unique


        # Create a new TypeOfOperationObject
            new_operation = TypeOfOperationObject(
                ID=len(TypeOfOperationObject.type_of_operation_list) + 1,    # Set a unique ID (you might adjust this depending on how you handle IDs)
                TypeOfOperation=new_operation_type,
                TypeOfMission="",  # Set default values
                References="",
                Comments="",
                PhaseList=[]
            )

        # Add the new operation to the in-memory list
            #self.type_of_operation_list.append(new_operation)
            TypeOfOperationObject.type_of_operation_list.append(new_operation)


            try:
                TypeOfOperationObject.new_entry(
                    TypeOfOperation=new_operation_type,  # Capitalized
                    TypeOfMission=new_operation.type_of_mission,
                    References=new_operation.references, 
                    Comments=new_operation.comments,
                    PhaseList=new_operation.phase_list
                )

            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Database Error", f"Failed to save operation type to the database: {e}")
                return

        # Create a new tab for the new operation type
            new_tab = QtWidgets.QWidget() 
            new_tab_layout = QtWidgets.QVBoxLayout(new_tab)
            new_tab_layout.setContentsMargins(0, 0, 0, 0)
            new_tab_layout.setSpacing(0)

            scroll_area = QtWidgets.QScrollArea(new_tab)
            scroll_area.setWidgetResizable(True)
            scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
            scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)

            container_widget = QtWidgets.QWidget(scroll_area)
            container_widget.setObjectName("container_widget")
            container_layout = QtWidgets.QVBoxLayout(container_widget)
            container_layout.setContentsMargins(0, 0, 0, 0)

            scroll_area.setWidget(container_widget)
            new_tab_layout.addWidget(scroll_area)

        # Add the tab to the tab widget
            self.flightPhases_tabs.addTab(new_tab, new_operation_type)
              

        # Add the new tab information to `new_tab_input`
            self.new_tab_input.append({
                "name": new_operation_type,
                "id": new_operation.id  # Use the `id` from the newly created object
            })
            
        # Close the dialog after successful creation
            dialog.accept()
             # Refresh the operation types and reload tabs


            #QtWidgets.QMessageBox.information(self, "Success", f"New operation type '{new_operation_type}' created and added to tabs.")
        else:
            pass
            #QtWidgets.QMessageBox.warning(self, "Invalid Input", "Please enter a valid operation type.")

 
                 

    def open_comments_procedure_dialog(self):
        """Opens the 'Comments for Procedure' dialog when the button is clicked."""
        self.dialog = QtWidgets.QDialog()  # Create a QDialog instance
        self.ui = Ui_DialogProceduresComments()  # Create an instance of the dialog's UI
        self.ui.setupUi(self.dialog)  # Set up the dialog's UI
        self.dialog.exec_()  # Show the dialog
    def open_references_procedure_dialog(self):
        """Opens the 'References for Procedure' dialog when the button is clicked."""
        self.dialog = QtWidgets.QDialog()  # Create a QDialog instance
        self.ui = Ui_DialogReferencesProcedure()  # Create an instance of the dialog's UI
        self.ui.setupUi(self.dialog)  # Set up the dialog's UI
        self.dialog.exec_()  # Show the dialog  
    #def open_db_dialog(self):
        #db_dialog = DatabaseDialog(self)
        #db_dialog.exec_()
    def open_new_procedure_dialog(self):
        """Opens the 'New Procedure' dialog and handles its outcome."""

    # Create an instance of the newProcedure dialog, passing 'self' as the parent
        new_procedure_dialog = newProcedure(self)
    
    # Execute the dialog modally (blocks the main window until the dialog is closed)
        result = new_procedure_dialog.exec_()

    # Check if the dialog was accepted
        if result == QDialog.Accepted:
        # Optionally, check the valid_flag or other conditions in the newProcedure dialog
            if new_procedure_dialog.valid_flag:
            # Call any methods to update the UI or data after a successful dialog close
                self.reload_all()
            else:
            # Optionally, handle the case where the dialog was accepted but not valid
                QtWidgets.QMessageBox.warning(self, "Invalid Input", "The procedure is invalid or incomplete.")
 

    def populate_warning_view(self, selected_procedure_id, type_of_operation_id):
        self.update_all_lists()
        print("populate_warning_view called")

    # Clear existing widgets in the warningLayout
        if selected_procedure_id is None or type_of_operation_id is None:
            print("Either procedure or operation is not selected.")
            return

        for i in reversed(range(self.verticalLayout_5.count())):
            widget = self.verticalLayout_5.itemAt(i).widget()
            if widget:
                self.verticalLayout_5.removeWidget(widget)
                widget.setParent(None)

        try:
            print("Current ItemObject.item_list state before generating warnings:")
            for item in ItemObject.item_list:
                print(f"Item ID: {item.id}, Provides: {item.provides}, Requires: {item.requires}, Turns Off: {item.turns_off}")

            warning_list = create_requirements_list(selected_procedure_id, type_of_operation_id)

        # Process each warning in the list
            for row in warning_list:
                #step_item_key = (row.procedure_step_id, row.procedure_step_id)
                #saved_system_state = self.saved_systems_by_step.get(step_item_key, {})
            # Check if any systems are required and not provided
                missing_systems = [
                    item.id for item in ItemObject.item_list 
                    if item.name in row.requires and item.name not in row.provides
                ]

            # Only create and add warning_widget if missing systems are found
                if missing_systems:
                    print(f"Adding warning for procedure: {row.procedure_name}, phase: {row.phase_name}, step: {row.step_order_number}, missing systems: {missing_systems}")
                    warning_widget = warningContainer(
                        row.phase_name, 
                        row.procedure_name, 
                        row.step_order_number,   
                        missing_systems          
                    )
                    print(f"Warning generated for missing systems: {missing_systems}")
                    self.verticalLayout_5.addWidget(warning_widget, alignment=QtCore.Qt.AlignTop)  # Add the warning widget to the layout

        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to populate warnings: {e}")
            traceback.print_exc()             
    def reload_procedure_steps(self):
        selected_procedure_index = self.comboBox_procedures.currentIndex()
        selected_procedure_id = self.comboBox_procedures.itemData(selected_procedure_index)

        if selected_procedure_id is None:
            QtWidgets.QMessageBox.warning(self, "Warning", "Please select a valid procedure.")
            return

        try:
            #self.adjust_step_order(selected_procedure_id)
            print("Clearing and reloading procedure steps")
            self.populate_selected_procedure_step(selected_procedure_id)
            self.adjust_step_order(selected_procedure_id)
            QtWidgets.QMessageBox.information(self, "Success", "Procedure steps reloaded successfully.")
        except Exception as e:
           QtWidgets.QMessageBox.critical(self, "Error", f"Failed to reload procedure steps: {e}")
           traceback.print_exc()  
    def adjust_step_order(self, procedure_id):
        
    # Fetch all steps for the given procedure and sort them by order
        steps = [step for step in ProcedureStepObject.procedure_step_list if step.procedure_id == procedure_id]
        sorted_steps = sorted(steps, key=lambda x: int(x.order_step))
    
    # Reorder the steps to be sequentially numbered starting from 1
        for index, step in enumerate(sorted_steps):
            correct_order = index + 1
            if int(step.order_step) != correct_order:
            # Update the step order
                step.order_step = correct_order
                ProcedureStepObject.edit_procedure_step(
                    step.id,
                    object_name=step.object_name,
                    order_step=step.order_step,
                    action=step.action,
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

    # Reload the updated order in the UI
        self.populate_selected_procedure_step(procedure_id)
        print(f"Adjusted order for procedure {procedure_id}")       
    def reload_all(self):
        try:

        # Store the currently selected tab to restore it later
            self.update_all_lists()
            current_tab_index = self.flightPhases_tabs.currentIndex()
            selected_procedure_index = self.comboBox_procedures.currentIndex()
        
        # Block signals to avoid recursive calls
            self.flightPhases_tabs.blockSignals(True)

        # Update all in-memory lists from the database
           

        
        # Prevent recursion in add_operation_type
            if not getattr(self, "_reloading_operations", False):
                self.add_operation_type()

        # Repopulate combo boxes based on updated data
            if self.phase_list:
                self.populate_flight_phases_combo_box(self.phase_list)  # Reload phase combo box
            if selected_procedure_index != -1:
                self.comboBox_procedures.setCurrentIndex(selected_procedure_index)
        # Make sure that the current procedure is selected and its steps are reloaded
            if current_tab_index != -1:
                self.flightPhases_tabs.setCurrentIndex(current_tab_index)
                self.on_phase_changed()  # Handle phase change
                self.on_procedure_changed()  # Handle procedure change

            # Get the selected procedure
                #selected_procedure_index = self.comboBox_procedures.currentIndex()
                selected_procedure_id = self.comboBox_procedures.itemData(selected_procedure_index)

                #if selected_procedure_id is None:
                    #QtWidgets.QMessageBox.warning(self, "Error", "No valid procedure selected.")
                    #return

            #Ensure procedure steps are created (use num_instances argument)
                #if hasattr(self, 'selected_phase_id') and self.selected_phase_id is not None:
            #Clear existing layout before reloading steps
                    #self.clear_layout(self.findChild(QVBoxLayout, "verticalLayout_7"))
    
                    #procedure_steps_count = len([step for step in self.procedure_step_list if step.phase_id == self.selected_phase_id])
                    #self.create_procedure_steps(procedure_steps_count)

                #if current_tab_index < len(self.new_tab_input):
                if selected_procedure_id is not None and current_tab_index < len(self.new_tab_input):
                    type_of_operation_id = self.new_tab_input[current_tab_index]["id"]
                    self.populate_warning_view(selected_procedure_id, type_of_operation_id)
               # else:
                    #print("Invalid operation index; skipping type_of_operation_id assignment.")
                    #type_of_operation_id = None


            #Reapply any warning or specific UI view updates
                #self.populate_warning_view(selected_procedure_id, type_of_operation_id)

                print("reload_all executed successfully")
            #else:
                #QtWidgets.QMessageBox.warning(self, "Error", "No valid tab selected.")
    
        except Exception as e:
        # Add error handling to ensure proper error messaging if something goes wrong
            #QtWidgets.QMessageBox.critical(self, "Error", f"Failed to reload all components: {e}")
            traceback.print_exc()
        finally:
        # Re-enable signals after completing the task
            self.flightPhases_tabs.blockSignals(False)
    def adjust_step_order(self, procedure_id):
  
     #Adjusts the order of steps for the given procedure to be sequential starting from 1.
    
        current_step_list = [
            obj for obj in self.procedure_step_list if obj is not None and obj.procedure_id == procedure_id
        ]
        sorted_steps = sorted(current_step_list, key=lambda step: int(step.order_step))

        for index, step in enumerate(sorted_steps, start=1):
            if int(step.order_step) != index:
                step.order_step = index
            # Update in database if necessary
                self.update_object_in_db(
                    step.object_name, step.action, step.order_step, step.executed_by,
                    step.output_state, step.physical_features, step.procedure_id
                )
    def print_layout_contents(self, layout):
        print("Current contents of layout:")
        for i in range(layout.count()):
            item = layout.itemAt(i)
            widget = item.widget()
            if widget:
                print(f" - Widget at position {i}: {widget.objectName()}, Type: {type(widget)}")
            else:
                print(f" - Spacer at position {i}")              

    def update_all_lists(self):
       
        #print(id(self.item_list), id(ItemObject.item_list))
        self.item_list = ItemObject.item_list
        self.procedure_list = ProcedureObject.procedure_list
        self.procedure_step_list = ProcedureStepObject.procedure_step_list
        self.type_of_operation_list = TypeOfOperationObject.type_of_operation_list
        self.phase_list = PhaseObject.phase_list
        self.system_state_list = SystemStateObject.system_state_list
        self.checkpoint_list = CheckpointObject.checkpoint_list
    def showEvent(self, event):
        super().showEvent(event)
        self.reload_all()
       
if __name__ == "__main__":

    import sys
    app = QtWidgets.QApplication(sys.argv)
    main_window = FlightFlowMainWindow()  # Create the main window
    main_window.showMaximized()  # Show the main window maximized
    sys.exit(app.exec_())
