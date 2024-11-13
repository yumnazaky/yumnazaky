import os, sys, math 

current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# get the directory of GUI (which is in a sibling folder)
GUI_path = os.path.join(current_dir, "gui")
module_path = os.path.join(current_dir,"modules")# add GUI path to the system path
sys.path.append(GUI_path) 
sys.path.append(module_path)

from set_input_req_widget import Ui_SetInputReqWidget

from PyQt5 import QtCore, QtGui, QtWidgets
from set_input_req_dialog11 import Ui_setInputReqDialog  # Import the dialog class
from system_req_input_row import Ui_setReqInputRow  # Import the form with labels

class SetInputReqWidget(QtWidgets.QWidget, Ui_SetInputReqWidget):  # Inherit from QWidget
    def __init__(self, parent=None):
        super(SetInputReqWidget, self).__init__(parent)
        self.setupUi(self)  # Set up the UI using the setup method

    def create_checkpoint(self, step_id, item_state, person_state):
        # Create a new checkpoint
        checkpoint = Checkpoint(
            procedure_step_id=step_id,
            itemState=item_state,
            personState=person_state
        )
        # Save the checkpoint in the database
        session.add(checkpoint)
        session.commit()

    def delete_procedure_step(self, step_id):
        # Delete the procedure step from the database
        step = session.query(ProcedureStep).get(step_id)
        if step:
            session.delete(step)
            session.commit()

    def open_input_dialog(self):
        # Create and show the input requirements dialog
        dialog = QtWidgets.QDialog()
        ui_dialog = Ui_setInputReqDialog()
        ui_dialog.setupUi(dialog)

        # Connect the OK button to handle data transfer
        ui_dialog.inputButtonBox.accepted.connect(lambda: self.add_row(ui_dialog.systemInputLineEdit.text(),
                                                                      ui_dialog.parameterLineEdit.text(),
                                                                      ui_dialog.unitLineEdit.text()))

        dialog.exec_()  # This will open the dialog modally

    def add_row(self, system_name, parameter, unit):
        """Add a new row to the ListWidget and display the data."""
        # Create an instance of the second form to add data
        item_widget = QtWidgets.QWidget()
        ui_form = Ui_setReqInputRow()
        ui_form.setupUi(item_widget)

        # Set the text for system name, parameter, and unit labels
        ui_form.systemName.setText(f"<html><head/><body><p><span style=\" font-weight:600;\">{system_name}</span></p></body></html>")
        ui_form.parameterLbael.setText(parameter)
        ui_form.unitLabel.setText(unit)

        # Create a QListWidgetItem
        list_item = QtWidgets.QListWidgetItem(self.req_input_listWidget)
        list_item.setSizeHint(item_widget.sizeHint())  # Set the size of the widget

        # Add the widget to the QListWidget
        self.req_input_listWidget.addItem(list_item)
        self.req_input_listWidget.setItemWidget(list_item, item_widget)

    def delete_checkpoint_with_confirmation(self):
        """Delete the entire checkpoint widget after user confirmation."""
        # Create a confirmation dialog
        confirm_dialog = QtWidgets.QMessageBox()
        confirm_dialog.setIcon(QtWidgets.QMessageBox.Warning)
        confirm_dialog.setText("Are you sure you want to delete this checkpoint?")
        confirm_dialog.setWindowTitle("Delete Checkpoint")
        confirm_dialog.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

        result = confirm_dialog.exec_()

        if result == QtWidgets.QMessageBox.Yes:
            # Delete the entire checkpoint widget
            self.checkpoint_widget.deleteLater()  # Correctly delete the checkpoint widget
