import sys, os, json
import math
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add 'modules' folder to the system path
modules_path = os.path.join(current_dir, "modules")
sys.path.append(modules_path)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QWidget, QCheckBox, QPushButton, QLineEdit
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from database_item import DbItemEdition
from Database1 import Item 
from Database1 import Database
from Database1 import SystemState   # Replace with actual imports
from define_object_classes import ItemObject, SystemStateObject, PhaseObject, CheckpointObject, ProcedureStepObject, ProcedureObject, TypeOfOperationObject
from systems_dialog import Ui_DialogSystem
from systen_row import Ui_systemsRows
from update_databases import update_lists 
class DialogSystem(QDialog, Ui_DialogSystem):
    valid_flag = bool  
    item_list = []
    type_of_operation_list = []
    phase_list = []
    procedure_list= []
    procedure_step_list = []
    system_state_list = []
    checkpoint_list = []
    item_id = math.nan
    phase_list =[]
    phase_id =math.nan
    procedure_step_id = math.nan
    checkbox_state_changed = pyqtSignal(str, str, bool)

    
    saved_systems_by_step = {}
    systems_selected = pyqtSignal(int, list, list,list)
    change_signal_systems = QtCore.pyqtSignal()
    selection_complete = QtCore.pyqtSignal()
    def __init__(self,  parent=None,selections=None,item_id=None, phase_id=None, procedure_step_id=None,  instance_id=None):
        super(DialogSystem, self).__init__(parent)
        self.setupUi(self)

        
        #self.saved_systems_by_step = {}
        #CheckpointObject.clear_all_checkpoints()
        #print("Checkpoint list explicitly cleared in DialogSystem.")
        #CheckpointObject.print_table()
        #DbCheckpointEdition.print_table()
        #self.load_saved_selections()
        self.setStyleSheet("""
            QDialog, QWidget, QFrame, QScrollArea, QLabel, QPushButton, QCheckBox, QLineEdit, QDialogButtonBox {
                background-color: white;
            }
            QScrollArea {
                background: transparent; /* Removes background of the scroll area itself */
            }
            QScrollArea > QWidget > QWidget { /* Applies background to scroll area contents */
                background-color: white;
            }
            QHeaderView::section {
                background-color: white;
            }
        """)

        self.provides = []
        self.requires = []
        self.turns_off = []

        # Default systems that should always appear
        self.item_id = item_id if item_id is not None else (ItemObject.item_list[0].id if ItemObject.item_list else -1)
      
        ItemObject.initialize_default_systems()  # Ensure default systems are loaded once
        self.instance_id = instance_id


        self.remove_duplicate_systems()
        self.system_list = []
        #self.instance_id = instance_id or (phase_id, procedure_step_id)
        
        self.phase_id = self.phase_id
        self.procedure_step_id = self.procedure_step_id
        self.valid_flag = False
        self.setModal(False)
        self.saved_systems_by_step.setdefault(self.instance_id, {})
        #if self.procedure_step_id is not None:
            #print(f"Initialized with procedure_step_id: {self.procedure_step_id}")
        #else:
            #print("Dialog initialized without procedure_step_id")

        #self.saved_systems_by_step = self.saved_systems_by_step or {}
        print("Initialized saved_systems_by_step:", self.saved_systems_by_step)
        self.provides_list = []
        self.requires_list = []
        self.turns_off_list = []
        
        if self.instance_id is not None:
        # If the instance ID doesn't exist in the dictionary, create it with empty lists for selections
            if self.instance_id not in self.saved_systems_by_step:
                self.saved_systems_by_step[self.instance_id] = {
                    "item_id": self.item_id,
                    "provides": [],
                    "requires": [],
                    "turns_off": []
                }
            else:
            # If instance_id exists, load the saved lists
                saved_data = self.saved_systems_by_step[self.instance_id]
                self.provides = saved_data.get("provides", [])
                self.requires = saved_data.get("requires", [])
                self.turns_off = saved_data.get("turns_off", [])
        self.fill_scroll_area()        
        self.load_saved_selections(self.instance_id)
    
        # Setup connections for the buttons
        self.pushButton.clicked.connect(self.add_system)
        self.newSystemLineEdit.textChanged.connect(self.activate_new_system_button)
        self.pushButton.setDisabled(True)
        self.buttonBox_system_dialog.accepted.connect(self.accept_button_clicked)
        self.buttonBox_system_dialog.rejected.connect(self.reject)
        self.checkbox_state_changed.connect(self.save_checkbox_state)
        # Update lists and fill scroll area with existing systems
        self.update_lists_all()
        
        #self.apply_saved_states()
        #self.systems_selected.emit(self.provides_list, self.requires_list, self.turns_off_list)
        #self.saved_systems_by_step = {} if self.procedure_step_id is None else self.saved_systems_by_step
        self.selections = selections if selections is not None else {}
        #self.remove_duplicate_systems()
        
        #if self.procedure_step_id is not None:
            #self.load_saved_selections()

            #print("Final item list after initialization:", [(item.id, item.name) for item in ItemObject.item_list])
    def remove_duplicate_systems(self):
       
        unique_items = {}
        for item in ItemObject.item_list:
            if item.name not in unique_items:
                unique_items[item.name] = item  # Keep the first occurrence of each item name
        ItemObject.item_list = list(unique_items.values())  # Rebuild list without duplicates
        #print("Item list after duplicate removal:", [(item.id, item.name) for item in ItemObject.item_list])
    
    #def closeEvent(self, event):
    
        #ItemObject.item_list.clear()  # Ensure clean state on close
        #event.accept()
    def fill_scroll_area(self):
        while self.verticalLayout_2.count():
            widget = self.verticalLayout_2.takeAt(0).widget()
            if widget is not None:
                widget.deleteLater()
        
        for item in ItemObject.item_list:
           
            self.add_system_row(item.name, item.provides, item.requires, item.turns_off)
    
        
           
    def add_system(self):
        """Add a new system to the list and update the database."""
        system_name = self.newSystemLineEdit.text().strip()
        if not system_name:
            print("System name is empty; cannot add system.")
            return

    # Check if the system name already exists in item_list to avoid duplicates
        if any(item.name == system_name for item in ItemObject.item_list):
            print(f"System '{system_name}' already exists in item list; skipping addition.")
            return

        new_item = ItemObject(
            ID=None,
            name=system_name,
            state_list={"provides": False, "requires": False, "turns_off": False},
            input_param="",
            output_param="",
            provides=[],
            requires=[],
            turns_off=[]
        )
        ItemObject.add_unique_item(new_item)
        #ItemObject.item_list.append(new_item)
        self.add_system_row(system_name)  # Refresh UI to show the new system
        self.newSystemLineEdit.clear()  # Clear input after adding
        

            #ItemObject.item_list.append(new_item)
            #self.add_system_row(system_name)
            #new_system_state = SystemState(name=system_name, item_state="", person_state="")
            #SystemStateObject.system_state_list.append(new_system_state) 
          
            #self.newSystemLineEdit.clear()

    def add_system_row(self, system_name, provides="", requires="", turns_off=""):
    
        systemsRows = QtWidgets.QWidget(self.systemsContainer)

        # Instantiate the Ui_systemsRows to set up the UI for the row
        ui = Ui_systemsRows()
        ui.setupUi(systemsRows)

        # Set the system name in the label
        ui.systemlabel.setText(system_name)
        #print(f"Added QLabel with text: {ui.systemlabel.text()} for system {system_name}")
        # Set the checkbox states based on the values from ItemObject
        ui.ProvidesCheckBox.setChecked(bool(provides))
        ui.requiresCheckBox.setChecked(bool(requires))
        ui.turnOffCheckBox.setChecked(bool(turns_off))
        # Connect checkboxes to the update functionality in ItemObject
        ui.ProvidesCheckBox.stateChanged.connect(lambda state: self.checkbox_changed(system_name, 'provides', state, ui))
        ui.requiresCheckBox.stateChanged.connect(lambda state: self.checkbox_changed(system_name, 'requires', state, ui))
        ui.turnOffCheckBox.stateChanged.connect(lambda state: self.checkbox_changed(system_name, 'turns_off', state, ui))

        ui.deleteButton.clicked.connect(
            lambda: self.delete_system_row(systemsRows, system_name)
        )

    # Add the row to the scroll area's layout
        self.verticalLayout_2.addWidget(systemsRows)
    def checkbox_changed(self, system_name, checkbox_type, state, ui):
   
        is_checked = state == Qt.Checked
       
        if checkbox_type == 'provides':
            self.update_selection_list(self.provides_list, system_name, is_checked)
        elif checkbox_type == 'requires':
            self.update_selection_list(self.requires_list, system_name, is_checked)
        elif checkbox_type == 'turns_off':
            self.update_selection_list(self.turns_off_list, system_name, is_checked)
    
        self.checkbox_state_changed.emit(system_name, checkbox_type, is_checked)
   
        self.enforce_single_selection(ui, checkbox_type)
    def sync_saved_states_with_item_list(self):
        for item_id, states in self.saved_systems_by_step.get(self.procedure_step_id, {}).items():
        # Retrieve the item based on item_id
            item = ItemObject.return_item(item_id)
            if item:
                item.provides = states.get("provides", [])
                item.requires = states.get("requires", [])
                item.turns_off = states.get("turns_off", [])
            else:
                print(f"Warning: No item found with item_id {item_id}.")
        print("Synchronized saved states with ItemObject.item_list.")

    def update_selection_list(self, selection_list, system_name, is_checked):
    
        if is_checked and system_name not in selection_list:
            selection_list.append(system_name)
        elif not is_checked and system_name in selection_list:
            selection_list.remove(system_name)     

    def save_checkbox_state(self, system_name, checkbox_type, is_checked):
        item = next((it for it in ItemObject.item_list if it.name == system_name), None)
        if not item:
            print(f"System '{system_name}' not found in item list.")
            return

    # Update only the specific item's provides, requires, or turns_off list
        if checkbox_type == 'provides':
            self.update_selection_list(item.provides, system_name, is_checked)
        elif checkbox_type == 'requires':
            self.update_selection_list(item.requires, system_name, is_checked)
        elif checkbox_type == 'turns_off':
            self.update_selection_list(item.turns_off, system_name, is_checked)

        print(f"Updated item - ID: {item.id}, Name: {item.name}, Provides: {item.provides}, Requires: {item.requires}, Turns Off: {item.turns_off}")

   
    def enforce_single_selection(self, ui, selected_checkbox):
   
        if selected_checkbox == 'provides':
            if ui.ProvidesCheckBox.isChecked():
                ui.requiresCheckBox.setChecked(False)
                ui.turnOffCheckBox.setChecked(False)
        elif selected_checkbox == 'requires':
            if ui.requiresCheckBox.isChecked():
                ui.ProvidesCheckBox.setChecked(False)
                ui.turnOffCheckBox.setChecked(False)
        elif selected_checkbox == 'turns_off':
            if ui.turnOffCheckBox.isChecked():
                ui.ProvidesCheckBox.setChecked(False)
                ui.requiresCheckBox.setChecked(False)    

    def update_system_state(self, system_name, state_type, state):
     
        system_item = next((item for item in ItemObject.item_list if item.name == system_name), None)
        if system_item:
            system_id = system_item.id
        # Fetch the item by ID using the return_item method
            item = ItemObject.return_item(system_id)
            if item:
                if state_type == "Provides":
                    item.provides = "Provides" if state == Qt.Checked else ""
                elif state_type == "Requires":
                    item.requires = "Requires" if state == Qt.Checked else ""
                elif state_type == "Turns Off":
                    item.turns_off = "Turns Off" if state == Qt.Checked else ""

            
                print(f"System '{system_name}' updated: {state_type} set to {system_item.provides or system_item.requires or system_item.turns_off}")
            else:
                print(f"System with ID '{system_id}' not found.")
        else:
            print(f"Warning: System '{system_name}' not found in ItemObject.item_list.")

            

    def delete_system_row(self, system_row_widget, system_name):
      
        self.verticalLayout_2.removeWidget(system_row_widget)
        system_row_widget.setParent(None)

        
        #ItemObject.item_list = [item for item in ItemObject.item_list if item.name != system_name]
        system_item = next((item for item in ItemObject.item_list if item.name == system_name), None)
        if system_item:
        # Call the delete method to handle deletion from both the in-memory list and the database
            system_item.delete()
            print(f"System '{system_name}' deleted from in-memory list and database.")
        else:
            print(f"System '{system_name}' not found in ItemObject.item_list.")


        
        self.change_signal_systems.emit()

    def activate_new_system_button(self):
        #Enable the Add System button when the input field has text
        if self.newSystemLineEdit.text().strip():
            self.pushButton.setEnabled(True)
        else:
            self.pushButton.setDisabled(True)
    def update_checkboxes(self):
        """Update the checkbox states in the scroll area based on saved selections."""
        for i in range(self.verticalLayout_2.count()):
            widget = self.verticalLayout_2.itemAt(i).widget()
            if widget:
                label = widget.findChild(QtWidgets.QLabel)
                system_name = label.text() if label else None
                if system_name:
                    widget.findChild(QCheckBox, "ProvidesCheckBox").setChecked(system_name in self.provides)
                    widget.findChild(QCheckBox, "requiresCheckBox").setChecked(system_name in self.requires)
                    widget.findChild(QCheckBox, "turnOffCheckBox").setChecked(system_name in self.turns_off)
        print(f"Selections loaded for instance_id {self.instance_id}")
        
    def showEvent(self, event):
        super().showEvent(event)
        saved_data = self.saved_systems_by_step.get(self.instance_id, {})
        self.provides = saved_data.get("provides", [])
        self.requires = saved_data.get("requires", [])
        self.turns_off = saved_data.get("turns_off", [])
        self.update_checkboxes()

    #def closeEvent(self, event):
        #self.accept_button_clicked()
        #super().closeEvent(event)
    
    def load_saved_selections(self, instance_id): 
        #self.provides_list.clear()
        #self.requires_list.clear()
        #self.turns_off_list.clear()
        item = ItemObject.return_item(self.item_id)
        if item:
            provides = item.provides
            requires = item.requires
            turns_off = item.turns_off
        else:
            print(f"No item found with ID {self.item_id} for loading selections.")    

        for i in range(self.verticalLayout_2.count()):
            widget = self.verticalLayout_2.itemAt(i).widget()
            if widget:
                label = widget.findChild(QtWidgets.QLabel)
                system_name = label.text() if label else None
                if system_name:
                    # Retrieve saved state for this system
                    #selection_state = self.saved_systems_by_step[self.instance_id].get(system_name, {"provides": False, "requires": False, "turns_off": False})
                    if system_name:
                        widget.findChild(QCheckBox, "ProvidesCheckBox").setChecked(system_name in self.provides)
                        widget.findChild(QCheckBox, "requiresCheckBox").setChecked(system_name in self.requires)
                        widget.findChild(QCheckBox, "turnOffCheckBox").setChecked(system_name in self.turns_off)
        print(f"Selections loaded for instance_id {self.instance_id}")
                    
                
    def accept_button_clicked(self):
        provides = []
        requires = []
        turns_off = []
    
        for i in range(self.verticalLayout_2.count()):
            widget = self.verticalLayout_2.itemAt(i).widget()
            if widget:
                label = widget.findChild(QtWidgets.QLabel)
                if label:
                    system_name = label.text()
                    if widget.findChild(QCheckBox, "ProvidesCheckBox").isChecked():
                        provides.append(system_name)
                    if widget.findChild(QCheckBox, "requiresCheckBox").isChecked():
                        requires.append(system_name)
                    if widget.findChild(QCheckBox, "turnOffCheckBox").isChecked():
                        turns_off.append(system_name)

    # Save selections in memory and database
        self.saved_systems_by_step[self.instance_id] = {
            "provides": provides,
            "requires": requires,
            "turns_off": turns_off
        }
        item = ItemObject.return_item(self.item_id)
        if item:
            item.provides = provides
            item.requires = requires
            item.turns_off = turns_off
            ItemObject.edit_item(
                item.id, item.name, item.state_list, item.input_param, item.output_param,
                provides, requires, turns_off
            )
        
        print(f"Selections saved for instance_id {self.instance_id}: Provides: {provides}, Requires: {requires}, Turns Off: {turns_off}")
        self.accept()
    
    def update_lists_all(self):
        
        self.item_list = ItemObject.item_list
        #print("Updated item list in update_all_lists:", [(item.id, item.name) for item in self.item_list])
        self.procedure_list = ProcedureObject.procedure_list
        self.procedure_step_list = ProcedureStepObject.procedure_step_list
        self.type_of_operation_list = TypeOfOperationObject.type_of_operation_list
        self.phase_list = PhaseObject.phase_list
        self.system_state_list = SystemStateObject.system_state_list
        self.checkpoint_list = CheckpointObject.checkpoint_list 
      
        #print(id(self.phase_list), id(PhaseObject.phase_list)) # Retrieve all updated lists from the database or in-memory data
        #print("Item List:", self.item_list)
        #print("Phase List:", self.phase_list)
        #print("Type of Operation List:", self.type_of_operation_list)
        #print("System State List:", self.system_state_list)
        #print("Checkpoint List:", self.checkpoint_list)
        #print("Procedure List:", self.procedure_list)
        #print("Procedure Step List:", self.procedure_step_list)
        # Print lists for debugging purposes
        #print(f"Updated item list: {self.item_list}")
        #print(f"Updated phase list: {self.phase_list}")
        #print(f"Updated system state list: {self.system_state_list}")
        #print(f"Updated procedure step list: {self.procedure_step_list}")


