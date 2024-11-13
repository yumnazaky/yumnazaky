import sys
import os
import traceback
import math

import json
from PyQt5.QtGui import QPalette, QColor

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
from system_functionalties_2 import DialogSystem
from define_object_classes import ProcedureObject, ProcedureStepObject, PhaseObject
from Database1 import Database  

class FlightPhaseWidget(QWidget, Ui_FlightPhaseWidget):
    change_signal_phase = QtCore.pyqtSignal()
    move_up_signal = pyqtSignal(int)   # Define signal for moving up
    move_down_signal = pyqtSignal(int)
    def __init__(self, PID, Name, parent=None):
        super(FlightPhaseWidget, self).__init__(parent)
      
        
        self.phase_id = PID
        self.phase_name = Name
        self.setupUi(self)
        #self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        
        # Ensure the internal layout does not expand or have extra margins/spacings
      

        # Set the fixed size for the widget
        self.setFixedSize(350, 120)
        
        # Set QSizePolicy to Fixed to prevent resizing
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        #self.setSizePolicy(size_policy)
        self.up_flightPhase.clicked.connect(lambda: self.move_up_signal.emit(self.phase_id))
        self.down_flightPhase.clicked.connect(lambda: self.move_down_signal.emit(self.phase_id))
        

        # Fetch the phase object based on the phase ID
        self.phase = PhaseObject.return_phase(self.phase_id)
        self.flightPhase_order.setText(str(self.phase.order_number))

        self.procedure_step = [
            obj for obj in ProcedureStepObject.procedure_step_list
            if obj.procedure_id == self.phase_id and getattr(obj, 'order_number', None) == 0
        ]
        if not self.procedure_step:
            print(f"No procedure steps found for phase with ID: {self.phase_id}")
            self.step_id = None
            self.step = None
            self.item_id = None
        else:
            self.step_id = self.procedure_step[0].step_id
            self.step = next((obj for obj in ProcedureStepObject.step_list if obj.id == self.step_id), None)
            self.item_id = self.step.item_id if self.step else None
        # Ensure there are steps before accessing them
        #if self.procedure_step:
            #self.step_id = self.procedure_step[0].step_id
            #self.step = [obj for obj in ProcedureStepObject.step_list if obj.id == self.step_id][0]
            #self.item_id = self.step.item_id
        #else:
            #self.step_id = None
            #self.step = None
            #self.item_id = None

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
        confirm_dialog.setStyleSheet("""
        QMessageBox {
            background-color: white;
        }
        QLabel {
            background-color: white;
        }
        QPushButton {
            background-color: white;
        }
        """)
        confirm_dialog.setText(f"Are you sure you want to delete the phase '{self.phase_name}'?")
        confirm_dialog.setWindowTitle("Confirm Phase Deletion")
        confirm_dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        confirm_dialog.setDefaultButton(QMessageBox.No)

       # Handle the user's choice
        result = confirm_dialog.exec_()
        if result == QMessageBox.Yes:
        # Delete the phase and handle necessary cleanup
            phase = PhaseObject.return_phase(self.phase_id)
            if phase:
                print(f"Phase to delete: {phase}")
        # Remove procedures associated with this phase
                procedures_to_delete = [p for p in ProcedureObject.procedure_list if p.phase_id == self.phase_id]
                for procedure in procedures_to_delete:
                    ProcedureObject.procedure_list.remove(procedure)

                phase.list_harmonisation_delete()
                phase.delete()

                #self.main_window.create_flight_phase_widget(self.main_window.phase_list, self.main_window.container_layout)
                self.change_signal_phase.emit()
                self.setParent(None)  # Detach the widget from its parent layout
                self.deleteLater() 
            else:
                print(f"No phase found with ID {self.phase_id}")    


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
                phase = PhaseObject.return_phase(self.phase_id)
                phase.edit_phase(
                    phase.id,
                    new_name,
                    phase.order_number,
                    phase.input_state,
                    phase.output_state,
                    phase.procedure_list,
                    phase.type_of_operation_id,
                )

             # Update procedure names or other related fields if needed
                for procedure in ProcedureObject.procedure_list:
                    if procedure.phase_id == self.phase_id:
                        procedure.input_state = phase.input_state  # Example of updating input state if tied to phase
                        procedure.output_state = phase.output_state  # Update output state similarly

            dialog.close()
            self.change_signal_phase.emit()


        

        button.clicked.connect(update_phase_name)
        dialog.exec_()


    def moveUp(self):
        phase = PhaseObject.return_phase(self.phase_id)
        if not phase:
            print(f"Phase with ID {self.phase_id} not found.")
            return
    
    # Perform the move up logic
        result = PhaseObject.move_up(self.phase_id)

    # If the result is successful, emit the change signal
        if result:
            self.change_signal_phase.emit()

    def moveDown(self):
        phase = PhaseObject.return_phase(self.phase_id)
        if not phase:
            print(f"Phase with ID {self.phase_id} not found.")
            return
    
     # Perform the move down logic
        result = PhaseObject.move_down(self.phase_id)

     # If the result is successful, emit the change signal
        if result:
            self.change_signal_phase.emit()
    

    def open_system_dialog(self):
        procedure_step_id = getattr(self, 'procedure_step_id', None)
        instance_id = (self.phase_id, procedure_step_id) if procedure_step_id is not None else self.phase_id
    
        dialog = DialogSystem(
            parent=self,
            item_id=self.item_id,
            instance_id=instance_id  # Use the combined identifier
        )

        dialog.setStyleSheet("""
            QDialog, QFrame, QLabel, QScrollArea, QScrollBar, QWidget, QDialogButtonBox, QLineEdit, QPushButton, QCheckBox {
                background-color: white;
            }
            QScrollArea > QWidget > QWidget, QScrollArea > QViewport {
                background-color: white;
            }
            QFrame#systemsButtonsContainer, QFrame#requirementsHeader {
                background-color: white;
            }
            QLabel, QLineEdit, QCheckBox, QPushButton, QDialogButtonBox {
                color: black;
            }
            QLabel#systemsTitle, QLabel#ProvidesLabel, QLabel#requiresLabel, QLabel#turnsOffLabel, QWidget#requirementsHeader {
                background-color: white;
                color: black;
            }
        """)
        dialog.exec_()


# Set up the UI for the dialog
    
    # You can now use self.item_id here if needed, for example:
     #ui.some_widget.setText(str(self.item_id))  # Set item_id in a widget if needed
        #dialog.phase_id = self.phase_id 
        #dialog.exec_()  # Open the dialog



#if __name__ == "__main__":
    #app = QtWidgets.QApplication(sys.argv)
    #widget = FlightPhaseWidget(PID=1, Name="Sample Phase")
    #widget.show()
    #sys.exit(app.exec_())