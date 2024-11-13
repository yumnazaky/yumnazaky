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
    valid_flag = bool  # Flag zur Weitergabe der validität der Eingaben
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
  # Emit item_id, provides, requires, turns_off lists

    def __init__(self, parent=None, item_id=None, instance_id=None):
        super(DialogSystem, self).__init__(parent)
        self.setupUi(self)

        self.instance_id = instance_id
        self.item_id = item_id if item_id is not None else (ItemObject.item_list[0].id if ItemObject.item_list else -1)
        
        # Initialize lists for system state tracking
        self.provides_list = []
        self.requires_list = []
        self.turns_off_list = []
        
        # Load saved selections if available
        self.load_saved_selections(self.instance_id)

        # Setup UI and signals
        self.fill_scroll_area()
        self.buttonBox_system_dialog.accepted.connect(self.accept_button_clicked)
        self.buttonBox_system_dialog.rejected.connect(self.reject)

    def fill_scroll_area(self):
        self.remove_duplicate_systems()  # Ensure unique items in the list
        for item in ItemObject.item_list:
            saved_state = self.saved_systems_by_step.get(self.instance_id, {}).get(item.name, item.state_list)
            self.add_system_row(item.name, saved_state.get("provides", False), saved_state.get("requires", False), saved_state.get("turns_off", False))

    def add_system_row(self, system_name, provides=False, requires=False, turns_off=False):
        systemsRow = QtWidgets.QWidget(self.systemsContainer)
        ui = Ui_systemsRows()
        ui.setupUi(systemsRow)
        
        ui.systemlabel.setText(system_name)
        ui.ProvidesCheckBox.setChecked(provides)
        ui.requiresCheckBox.setChecked(requires)
        ui.turnOffCheckBox.setChecked(turns_off)
        
        # Connect checkbox changes to track in DialogSystem state
        ui.ProvidesCheckBox.stateChanged.connect(lambda state: self.checkbox_changed(system_name, 'provides', state))
        ui.requiresCheckBox.stateChanged.connect(lambda state: self.checkbox_changed(system_name, 'requires', state))
        ui.turnOffCheckBox.stateChanged.connect(lambda state: self.checkbox_changed(system_name, 'turns_off', state))
        
        self.verticalLayout_2.addWidget(systemsRow)

    def checkbox_changed(self, system_name, checkbox_type, state):
        is_checked = state == Qt.Checked
        if checkbox_type == 'provides':
            self.update_selection_list(self.provides_list, system_name, is_checked)
        elif checkbox_type == 'requires':
            self.update_selection_list(self.requires_list, system_name, is_checked)
        elif checkbox_type == 'turns_off':
            self.update_selection_list(self.turns_off_list, system_name, is_checked)
    
    def update_selection_list(self, selection_list, system_name, is_checked):
        if is_checked and system_name not in selection_list:
            selection_list.append(system_name)
        elif not is_checked and system_name in selection_list:
            selection_list.remove(system_name)

    def accept_button_clicked(self):
        # Emit signal with updated lists when dialog is accepted
        self.systems_selected.emit(self.item_id, self.provides_list, self.requires_list, self.turns_off_list)
        self.close()

    def load_saved_selections(self, instance_id):
        saved_state = self.saved_systems_by_step.get(instance_id, {})
        for system_name, states in saved_state.items():
            if states["provides"]:
                self.provides_list.append(system_name)
            if states["requires"]:
                self.requires_list.append(system_name)
            if states["turns_off"]:
                self.turns_off_list.append(system_name)
