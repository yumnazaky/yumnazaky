import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget
import math
from systems_dialog import Ui_systemsRows  # Assuming you saved your class as `systems_dialog`

class systemsRows(QWidget, Ui_systemsRows):
    system_id = math.nan
    system_name = "none"
    system_state = None

    def __init__(self, ID, Name, item_state, person_state, parent=None):
        
        super(systemsRows, self).__init__(parent)
        self.setupUi(self)  # Set up the UI from Ui_systemsRows
        self.system_id = ID
        self.system_name = Name

       
        self.system_state = SystemState(self.system_name, item_state, person_state)

        
        self.label.setText(self.system_name)

        
        self.ProvidesCheckBox.clicked.connect(self.checkboxStateChanged)
        self.requiresCheckBox.clicked.connect(self.checkboxStateChanged)
        self.turnOffCheckBox.clicked.connect(self.checkboxStateChanged)

    def checkboxStateChanged(self):
        checkboxes = [
            self.ProvidesCheckBox,
            self.requiresCheckBox,
            self.turnOffCheckBox,
        ]
        sender_checkbox = self.sender()

        # Uncheck all checkboxes if the sender checkbox is unchecked
        if not sender_checkbox.isChecked():
            for checkbox in checkboxes:
                checkbox.setChecked(False)

        # Uncheck the other checkboxes if the sender checkbox is checked
        else:
            for checkbox in checkboxes:
                if checkbox != sender_checkbox:
                    checkbox.setChecked(False)

        # Update system state based on the selected checkbox
        if self.ProvidesCheckBox.isChecked():
            self.system_state.item_state = "Provides"
        elif self.requiresCheckBox.isChecked():
            self.system_state.item_state = "Requires"
        elif self.turnOffCheckBox.isChecked():
            self.system_state.item_state = "Turns Off"
        else:
            self.system_state.item_state = "None"

        print(f"System State Updated: {self.system_state}")

#class SystemState:
    """ SystemState class definition """
    #def __init__(self, name, item_state, person_state):
        #self.name = name
        #self.item_state = item_state
        #self.person_state = person_state

    #def __repr__(self):
        #return f"SystemState(name={self.name}, item_state={self.item_state}, person_state={self.person_state})"


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    systemsRows = systemsRows(1, "System 1", "Idle", "Operator 1")
    systemsRows.show()
    sys.exit(app.exec_())