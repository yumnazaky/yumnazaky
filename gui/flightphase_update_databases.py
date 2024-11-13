import sys
import os
import traceback
import math

import json

from PyQt5 import QtCore, QtGui, QtWidgets 
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (
    QWidget,
    QMessageBox,
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QApplication,
)



current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# get the directory of GUI (which is in a sibling folder)
src_path = os.path.join(current_dir, "src")
# add GUI path to the system path
modules_path = os.path.join(current_dir, "modules")
sys.path.append(src_path)
sys.path.append(modules_path)
# print("Path Modules: ", modules_path))


from update_databases import update_lists
from flight_phases_ui import Ui_FlightPhaseWidget
from systems_dialog import Ui_DialogSystem
from define_object_classes import ProcedureObject, ProcedureStepObject, PhaseObject
from Database1 import Database  

class FlightPhaseWidget(QWidget, Ui_FlightPhaseWidget):
    change_signal_phase = QtCore.pyqtSignal()

    def __init__(self, PID, Name, parent=None):
        super(FlightPhaseWidget, self).__init__(parent)
      
        
        self.phase_id = PID
        self.phase_name = Name
        self.setupUi(self)
        self.flightPhase_order.setText(str(self.phase_id))



        # Fetch the phase object based on the phase ID
        self.phase = PhaseObject.return_phase(self.phase_id)

        self.procedure_step = [
            obj
            for obj in ProcedureStepObject.procedure_step_list
            if obj.procedure_id == self.phase_id and obj.order_number == 0
        ]

        # Ensure there are steps before accessing them
        if self.procedure_step:
            self.step_id = self.procedure_step[0].step_id
            self.step = [obj for obj in StepObject.step_list if obj.id == self.step_id][0]
            self.item_id = self.step.item_id
        else:
            self.step_id = None
            self.step = None
            self.item_id = None

        # Sets the label and adds the ID as user Data to the label
        self.flightPhase_label.setText(self.phase_name)
        self.flightPhase_label.setProperty("userData", self.phase_id)

        # Connect buttons to their respective slot functions
        self.delete_flightPhase.clicked.connect(self.deletePhase)
        self.edit_flightPhase.clicked.connect(self.renamePhase)
        self.up_flightPhase.clicked.connect(self.moveUp)
        self.down_flightPhase.clicked.connect(self.moveDown)
        self.systems_flightPhase.clicked.connect(self.open_system_dialog)
        
    def deletePhase(self):
        # Show a confirmation dialog
        confirm_dialog = QMessageBox(self)
        confirm_dialog.setIcon(QMessageBox.Warning)
        confirm_dialog.setStyleSheet("QFrame{background-color: transparent; color: black;}")
        confirm_dialog.setText(f"Are you sure you want to delete the phase '{self.phase_name}'?")
        confirm_dialog.setWindowTitle("Confirm Phase Deletion")
        confirm_dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirm_dialog.setDefaultButton(QMessageBox.No)

       # Handle the user's choice
        result = confirm_dialog.exec_()
        if result == QMessageBox.Yes:
        # Delete the phase and handle necessary cleanup
            phase = PhaseObject.return_phase(self.phase_id)
        
        # Remove procedures associated with this phase
            procedures_to_delete = [p for p in ProcedureObject.procedure_list if p.phase_id == self.phase_id]
            for procedure in procedures_to_delete:
                ProcedureObject.procedure_list.remove(procedure)

            phase.delete()
            self.change_signal_phase.emit()


    def renamePhase(self, index):
        dialog = QDialog()
        layout = QVBoxLayout(dialog)
        label = QLabel("Enter new phase name:")
        line_edit = QLineEdit()
        button = QPushButton("OK")

        layout.addWidget(label)
        layout.addWidget(line_edit)
        layout.addWidget(button)

        def update_phase_name():
            new_name = line_edit.text().strip()
            if new_name:
                self.flightPhase_label.setText(new_name)
                self.phase_name = new_name

                phase = session.query(PhaseObject).filter_by(id=self.phase_id).first()
                if phase:
                # Update the phase name and commit the changes
                    phase.name = new_name
                    session.commit()

                # Optionally update related procedures in the database
                    procedures = session.query(ProcedureObject).filter_by(phase_id=self.phase_id).all()
                    for procedure in procedures:
                        procedure.input_state = phase.input_state
                        procedure.output_state = phase.output_state
                    session.commit()

                self.change_signal_phase.emit()

            dialog.close()


        

        button.clicked.connect(update_phase_name)
        dialog.exec_()


    def moveUp(self):
        phase = PhaseObject.return_phase(self.phase_id)
        phase.move_up(self.phase_id)
        self.change_signal_phase.emit()

    def moveDown(self):
        phase = PhaseObject.return_phase(self.phase_id)
        phase.move_down(self.phase_id)
        self.change_signal_phase.emit()

    def open_system_dialog(self):
     dialog = QtWidgets.QDialog()  # Create a QDialog instance
     ui = Ui_DialogSystem()  # Create an instance of the Ui_DialogSystem
     ui.setupUi(dialog)  # Set up the UI for the dialog
     dialog.phase_id = self.phase_id 

    # You can now use self.item_id here if needed, for example:
     #ui.some_widget.setText(str(self.item_id))  # Set item_id in a widget if needed

     dialog.exec_()  # Open the dialog



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = FlightPhaseWidget(PID=1, Name="Sample Phase")
    widget.show()
    sys.exit(app.exec_())