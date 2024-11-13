import sys, os, json
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add 'modules' folder to the system path
modules_path = os.path.join(current_dir, "modules")
sys.path.append(modules_path)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QWidget, QCheckBox, QPushButton, QLineEdit
from PyQt5 import QtWidgets
from sqlalchemy.orm import sessionmaker
from Database1 import Database, SystemState  # Replace with actual imports
from define_object_classes import ItemObject, SystemStateObject
from systems_dialog import Ui_DialogSystem
from systen_row import Ui_systemsRows
from update_databases import update_lists 


class DialogSystem(QDialog, Ui_DialogSystem):
    change_signal_systems = pyqtSignal()

    def __init__(self, parent=None):
        super(DialogSystem, self).__init__(parent)
        self.setupUi(self)  # This calls the generated setupUi method from Ui_DialogSystem
        self.system_list = []

        # Define a list of default systems that will always be added
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

    def fill_scroll_area(self):
        """Loads systems from the database and populates the scroll area."""
        session = Database.get_session()
        self.system_list = session.query(SystemState).all()
        session.close()

        # Populate the scroll area with checkboxes for each system
        for system in self.system_list:
            self.add_system_row(system.name, system.item_state)

        # Add the default systems that should always appear
        for default_system in self.default_systems:
            self.add_system_row(default_system["name"], default_system["item_state"])

    def add_system(self):
        """Add a new system to the list and update the database."""
        system_name = self.newSystemLineEdit.text().strip()
        if system_name:
            # Add to the scroll area
            self.add_system_row(system_name)

            # Save new system to the database
            session = Database.get_session()
            new_system = SystemState(name=system_name, item_state="", person_state="")
            session.add(new_system)
            session.commit()
            session.close()

            # Clear the input
            self.newSystemLineEdit.clear()

    def add_system_row(self, system_name, item_state=""):
        """Add a new system row with checkboxes for Provides, Requires, and Turns Off."""
        # Create a widget container for the row
        system_row_widget = QtWidgets.QWidget(self.systemsContainer)

        # Instantiate the Ui_systemsRows to set up the UI for the row
        ui = Ui_systemsRows()
        ui.setupUi(system_row_widget)  # Set up the UI on the widget

        # Set the system name in the label
        ui.label.setText(system_name)

        # Split the item_state string into individual states (e.g., "Provides", "Requires", "Turns Off")
        states = item_state.split(", ") if item_state else []

        # Set the checkbox states based on the item_state
        ui.ProvidesCheckBox.setChecked("Provides" in states)
        ui.requiresCheckBox.setChecked("Requires" in states)
        ui.turnOffCheckBox.setChecked("Turns Off" in states)

        # Connect checkboxes to the update functionality
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
        """Update the item_state (Provides, Requires, Turns Off) for a system."""
        session = Database.get_session()
        system_state = session.query(SystemState).filter_by(name=system_name).first()

        if system_state:
           # Get the current item_state and split it into a list
            states = system_state.item_state.split(", ") if system_state.item_state else []

            # Add or remove the state based on checkbox state
            if state == Qt.Checked:
               if state_type not in states:
                  states.append(state_type)  # Add the state if it's not in the list
            else:
               if state_type in states:
                   states.remove(state_type)  # Remove the state if it's in the list

             # Join the updated states list back into a comma-separated string
            system_state.item_state = ", ".join(states)

            # Save the changes to the database
            session.commit()

        session.close()



        
       
    def delete_system_row(self, system_row_widget, system_name):
        """Delete the system from the UI and the database."""
        # Remove the system from the UI
        self.verticalLayout_2.removeWidget(system_row_widget)
        system_row_widget.setParent(None)  # This deletes the widget from the layout

        # Remove the system from the database
        session = Database.get_session()
        system_state = session.query(SystemState).filter_by(name=system_name).first()
        if system_state:
            session.delete(system_state)
            session.commit()
        session.close()

        # Emit the change signal
        self.change_signal_systems.emit()
    def update_system_state(self, system_name, state_type, state):
        """Update the state (Provides, Requires, Turns Off) for a system."""
        session = Database.get_session()
        system_state = session.query(SystemState).filter_by(name=system_name).first()

        if system_state:
            if state_type == "Provides":
                system_state.item_state = "Provides" if state == Qt.Checked else ""
            elif state_type == "Requires":
                system_state.person_state = "Requires" if state == Qt.Checked else ""
            elif state_type == "Turns Off":
                # If you handle "Turns Off", add the logic here
                pass

            session.commit()
        session.close()

    def activate_new_system_button(self):
        """Enable the 'Add System' button when the input field has text."""
        if self.newSystemLineEdit.text().strip():
            self.pushButton.setEnabled(True)
        else:
            self.pushButton.setDisabled(True)

    def accept_button_clicked(self):
        """Handle the acceptance of the dialog and save the system states."""
        session = Database.get_session()

        # Iterate over all the rows in the scroll area
        for i in range(self.verticalLayout_2.count()):
            widget = self.verticalLayout_2.itemAt(i).widget()

            # Check if the widget exists
        if widget:
            system_label = widget.findChild(QtWidgets.QLabel)
            if system_label:  # Ensure the QLabel is found
                system_name = system_label.text()
                provides = widget.findChild(QCheckBox, "Provides").isChecked()
                requires = widget.findChild(QCheckBox, "Requires").isChecked()
                turns_off = widget.findChild(QCheckBox, "Turns Off").isChecked()

                # Update the system state in the database
                system_state = session.query(SystemState).filter_by(name=system_name).first()
                if system_state:
                    # Create a list of all the checked states
                    states = []
                    if provides:
                        states.append("Provides")
                    if requires:
                        states.append("Requires")
                    if turns_off:
                        states.append("Turns Off")

                    # Store the combined states as a comma-separated string in item_state
                    system_state.item_state = ", ".join(states)
            else:
                print(f"Error: QLabel not found in widget {i}")
        else:
            print(f"Error: Widget not found in layout at position {i}")

        session.commit()
        session.close()

         # Emit the signal that indicates a change has been made
        self.change_signal_systems.emit()

         # Close the dialog
        self.accept()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    
    # Assuming this is your main application window/dialog
    dialog = DialogSystem()
    dialog.show()
    
    sys.exit(app.exec_())