import sys
import os 
import math


# get the current directory
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# get the directory of GUI (which is in a sibling folder)
GUI_path = os.path.join(current_dir, "gui")
module_path = os.path.join(current_dir,"modules")# add GUI path to the system path
sys.path.append(GUI_path) 
sys.path.append(module_path)

from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget
from update_databases import update_lists
from define_object_classes import ItemObject, SystemStateObject, PhaseObject, ProcedureStepObject
from Database1 import Database, Item, Phase, ProcedureStep
from warning_widget import Ui_warningContainer
class warningContainer(QWidget,Ui_warningContainer ):
    
    system_id = math.nan
    system_name = "none"
    missing_list = []

    def __init__(self, PhaseName, ProcedureName, SON, SIDList, parent=None):
        # Call the constructor of the parent class.
        super(warningContainer, self).__init__(parent)
        print(f"Initializing warningContainer for Phase: {PhaseName}, Procedure: {ProcedureName}, Step Order: {SON}, Missing Systems: {SIDList}")
        # Call the setupUi method to set up the user interface of the widget.
        self.setupUi(self)

        # Initialize variables
        self.phase_name = PhaseName
        self.procedure_name=ProcedureName  # The name of the procedure
        self.step_order_number = SON         # The step order number
        self.system_id_list = SIDList         # List of system IDs (or names)

        self.missing_list = []

        # Loop through the system IDs and retrieve system names from the Item class
        for system_id in self.system_id_list:
            # Query the database for the system using the Item class
            system_item = self.get_item_by_id(system_id)
            if system_item:
                name = system_item.name  # Assuming system_item.name is the system's name
                self.missing_list.append(name)
            else:
                print(f"No item found with ID {system_id} in ItemObject.item_list.")    

        # Set the UI labels with the provided data
        self.orderNo.setText(str(self.step_order_number)) 
        self.procedureText.setText(self.procedure_name) # Set the step order number
        self.flightPhaseWarning.setText(self.phase_name)        # Set the procedure name
        self.systemsWarning.setText("\n".join(self.missing_list))     # Display the system names
    def get_item_by_id(self, system_id):
        if not ItemObject.item_list:
            print("Warning: ItemObject.item_list is empty.")
        
        # Retrieve item based on ID
        
        for item in ItemObject.item_list:
            if item.id == system_id:
                return item
        return None
   

