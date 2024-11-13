import sys, os, json
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
from Database1 import Item 
from Database1 import Database
from Database1 import SystemState   # Replace with actual imports
from define_object_classes import ItemObject, SystemStateObject
from systems_dialog import Ui_DialogSystem
from systen_row import Ui_systemsRows
from update_databases import update_lists 
class DialogSystem(QDialog, Ui_DialogSystem):
    systems_selected = pyqtSignal(list, list, list) 
    change_signal_systems = QtCore.pyqtSignal()
    def __init__(self, parent=None):
        super(DialogSystem, self).__init__(parent)
        self.setupUi(self)
        self.system_list = []

        # Default systems that should always appear
        self.default_systems = [
            {"name": "Engine", "item_state": "", "person_state": ""},
            {"name": "Fuel System", "item_state": "", "person_state": ""},
            {"name": "Electrical System", "item_state": "", "person_state": ""},
            # Add more default systems as required
        ]

        # Setup connections for the buttons
        self.pushButton.clicked.connect(self.add_system)
        self.newSystemLineEdit.textChanged.connect(self.activate_new_system_button)
        self.pushButton.setDisabled(True)
        self.buttonBox_system_dialog.accepted.connect(self.accept_button_clicked)
        self.buttonBox_system_dialog.rejected.connect(self.reject)

        # Update lists and fill scroll area with existing systems
        self.update_lists_all()
        self.fill_scroll_area()

    def update_lists_all(self):
        """Update all object lists (e.g., items, phases, systems, etc.)."""
        (
            self.item_list,
            self.phase_list,
            self.type_of_operation_list,
            self.system_state_list,
            self.checkpoint_list,
            self.procedure_list,
            self.procedure_step_list,
        ) = update_lists()  # Retrieve all updated lists from the database or in-memory data

        # Print lists for debugging purposes
        print(f"Updated item list: {self.item_list}")
        print(f"Updated phase list: {self.phase_list}")
        print(f"Updated system state list: {self.system_state_list}")
        print(f"Updated procedure step list: {self.procedure_step_list}")



    def add_system(self):
        """Add a new system to the list and update the database."""
        system_name = self.newSystemLineEdit.text().strip()
        if system_name:
            # Add to the scroll area
            self.add_system_row(system_name)

            # Save new system to the database
            session = Database.get_session()
            # Save the system in both the Item table and the SystemState table
            new_item = Item(
                name=system_name, 
                state_list="", 
                input_param="", 
                output_param="", 
                provides="", 
                requires="", 
                turns_off=""
            )
            session.add(new_item)
            
            new_system_state = SystemState(name=system_name, item_state="", person_state="")
            session.add(new_system_state)
            
            session.commit()
            session.close()

            # Clear the input
            self.newSystemLineEdit.clear()

    def add_system_row(self, system_name, provides="", requires="", turns_off=""):
        """Add a new system row with checkboxes for Provides, Requires, and Turns Off."""
        # Create a widget container for the row
        system_row_widget = QtWidgets.QWidget(self.systemsContainer)

        # Instantiate the Ui_systemsRows to set up the UI for the row
        ui = Ui_systemsRows()
        ui.setupUi(system_row_widget)

        # Set the system name in the label
        ui.label.setText(system_name)

        # Set the checkbox states based on the values from ItemObject
        ui.ProvidesCheckBox.setChecked(bool(provides))
        ui.requiresCheckBox.setChecked(bool(requires))
        ui.turnOffCheckBox.setChecked(bool(turns_off))

        # Connect checkboxes to the update functionality in ItemObject
        ui.ProvidesCheckBox.stateChanged.connect(
            lambda state, name=system_name: self.update_system_state(name, "Provides", state)
        )
        ui.requiresCheckBox.stateChanged.connect(
            lambda state, name=system_name: self.update_system_state(name, "Requires", state)
        )
        ui.turnOffCheckBox.stateChanged.connect(
            lambda state, name=system_name: self.update_system_state(name, "Turns Off", state)
        )
        ui.deleteButton.clicked.connect(
            lambda: self.delete_system_row(system_row_widget, system_name)
        )

        # Add the row to the scroll area's layout
        self.verticalLayout_2.addWidget(system_row_widget)

    def update_system_state(self, system_name, state_type, state):
        """Update the system state for a system in ItemObject."""
        session = Database.get_session()
        system_item = session.query(Item).filter_by(name=system_name).first()

        if system_item:
            if state_type == "Provides":
                system_item.provides = "Provides" if state == Qt.Checked else ""
            elif state_type == "Requires":
                system_item.requires = "Requires" if state == Qt.Checked else ""
            elif state_type == "Turns Off":
                system_item.turns_off = "Turns Off" if state == Qt.Checked else ""

            session.commit()
        session.close()

    def delete_system_row(self, system_row_widget, system_name):
        """Delete the system from the UI and the database."""
        # Remove the system from the UI
        self.verticalLayout_2.removeWidget(system_row_widget)
        system_row_widget.setParent(None)

        # Remove the system from the database
        session = Database.get_session()
        system_item = session.query(Item).filter_by(name=system_name).first()
        if system_item:
            session.delete(system_item)
            session.commit()
        session.close()

        # Emit the change signal
        self.change_signal_systems.emit()

    def activate_new_system_button(self):
        """Enable the 'Add System' button when the input field has text."""
        if self.newSystemLineEdit.text().strip():
            self.pushButton.setEnabled(True)
        else:
            self.pushButton.setDisabled(True)

    
     # Emit selected provides, requires, turns_off systems

    def accept_button_clicked(self):
        """
        Handle the acceptance of the dialog and emit the selected systems and their relationships.
        """
        session = Database.get_session()

        provides_list = []
        requires_list = []
        turns_off_list = []

    # Iterate over all the rows in the scroll area
        for i in range(self.verticalLayout_2.count()):
            widget = self.verticalLayout_2.itemAt(i).widget()

            if widget:
                system_label = widget.findChild(QtWidgets.QLabel)
                if system_label:
                    system_name = system_label.text()

                # Check if the QCheckBox for "Provides" exists
                    provides_checkbox = widget.findChild(QCheckBox, "Provides")
                    if provides_checkbox:
                        provides = provides_checkbox.isChecked()
                    else:
                        print(f"Warning: 'Provides' checkbox not found for system: {system_name}")
                        provides = False

                # Check if the QCheckBox for "Requires" exists
                    requires_checkbox = widget.findChild(QCheckBox, "Requires")
                    if requires_checkbox:
                        requires = requires_checkbox.isChecked()
                    else:
                        print(f"Warning: 'Requires' checkbox not found for system: {system_name}")
                        requires = False

                # Check if the QCheckBox for "Turns Off" exists
                    turns_off_checkbox = widget.findChild(QCheckBox, "Turns Off")
                    if turns_off_checkbox:
                        turns_off = turns_off_checkbox.isChecked()
                    else:
                        print(f"Warning: 'Turns Off' checkbox not found for system: {system_name}")
                        turns_off = False

                # Add system names to respective lists
                    if provides:
                        provides_list.append(system_name)
                    if requires:
                        requires_list.append(system_name)
                    if turns_off:
                        turns_off_list.append(system_name)

        session.close()

    # Emit the selected systems and their relationships to the main dialog
        self.systems_selected.emit(provides_list, requires_list, turns_off_list)

    # Close the dialog
        self.accept()
    def fill_scroll_area(self):
        """Loads systems from the database and populates the scroll area."""
        session = Database.get_session()

    # Query the Item table to get the systems
        self.system_list = session.query(Item).all()

        session.close()

    # Populate the scroll area with checkboxes for each system
        for system in self.system_list:
            self.add_system_row(system.name, system.provides, system.requires, system.turns_off)

    # Add the default systems that should always appear
        for default_system in self.default_systems:
            self.add_system_row(default_system["name"], default_system["item_state"], "")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    # Assuming this is your main application window/dialog
    dialog = DialogSystem()
    dialog.show()

    sys.exit(app.exec_())
