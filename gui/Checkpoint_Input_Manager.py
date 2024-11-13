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
from define_object_classes import CheckpointObject, ProcedureStepObject



class CheckpointManager(QtWidgets.QWidget, Ui_SetInputReqWidget):
    def __init__(self, step_id, parent=None):
        super(CheckpointManager, self).__init__(parent)
        self.setupUi(self)
        self.setStyleSheet("""
            QWidget {
                background-color: rgb(255, 255, 255);
                border: 3px solid red;
                border-radius: 3px;
            }
            QLabel, QPushButton {
                border: 2px solid red;
                color: black;
            }
            QLabel {
                color: red;
                font-weight: bold;
            }
        """)
        self.step_id = step_id  # Procedure step ID
        self.current_checkpoint = None  # Track the currently selected checkpoint
        #self.clear_checkpoint_list()
        # Connect buttons to their respective functionalities
        self.inputButton.clicked.connect(self.open_input_dialog)
        #CheckpointObject.clear_all_checkpoints()
       # print("Checkpoint list explicitly cleared in DialogSystem.")
        #CheckpointObject.print_table()
        #self.verticalLayout_2.addWidget(self.inputButtonBox)
        self.deleteCheckpointButton.clicked.connect(self.delete_checkpoint_with_confirmation)
        self.req_input_listWidget.clear()

    def create_checkpoint(self, checkpoint_name, item_state, person_state):
        """Creates a new checkpoint and adds it to the in-memory list and UI."""
        # Create and append the new checkpoint to the in-memory list
        checkpoint = CheckpointObject(
            ID=len(CheckpointObject.checkpoint_list) + 1,  # Simulated ID
            Name=checkpoint_name,
            ItemState=item_state,
            PersonState=person_state,
            ProcedureStepID=self.step_id
        )
        CheckpointObject.checkpoint_list.append(checkpoint)

    # Add a row to display this checkpoint in the ListWidget
        self.add_row(checkpoint_name, item_state, person_state)
        # In create_checkpoint after adding checkpoint
        #self.load_existing_checkpoints()

    # Optional: Emit a signal or directly call a refresh function in the main window
        print(f"Checkpoint created: {checkpoint_name} for step ID: {self.step_id}")


    def update_checkpoint(self, checkpoint, checkpoint_name, item_state, person_state):
        """Updates an existing checkpoint with new data."""
        checkpoint.name = checkpoint_name
        checkpoint.item_state = item_state
        checkpoint.person_state = person_state
        print(f"Checkpoint updated: {checkpoint.name} for step ID: {self.step_id}")

    def open_input_dialog(self):
        """Opens the input dialog for adding a new checkpoint."""
        dialog = QtWidgets.QDialog()
        ui_dialog = Ui_setInputReqDialog()
        ui_dialog.setupUi(dialog)
        button_box = ui_dialog.inputButtonBox
        ui_dialog.inputButtonBox.accepted.connect(dialog.accept)  # Close dialog on OK
        ui_dialog.inputButtonBox.rejected.connect(dialog.reject)

    # Execute the dialog and check if the user clicked OK
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            # Collect field values after OK is clicked
            checkpoint_name = ui_dialog.checkpointInputLineEdit.text()
            item_state = ui_dialog.systemInputLineEdit.text()
            person_state = ui_dialog.parameterLineEdit.text()

        # Ensure all fields are filled before creating the checkpoint
            if checkpoint_name and item_state and person_state:
                self.create_checkpoint(checkpoint_name, item_state, person_state)
                print(f"Checkpoint '{checkpoint_name}' added for step ID: {self.step_id}")
            else:
                QtWidgets.QMessageBox.warning(self, "Input Error", "All fields are required to add a checkpoint.")

    def delete_checkpoint_with_confirmation(self):
        """Deletes a checkpoint after user confirmation."""
        confirm_dialog = QtWidgets.QMessageBox()
        confirm_dialog.setIcon(QtWidgets.QMessageBox.Warning)
        confirm_dialog.setText("Are you sure you want to delete this checkpoint?")
        confirm_dialog.setWindowTitle("Delete Checkpoint")
        confirm_dialog.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

        result = confirm_dialog.exec_()

        if result == QtWidgets.QMessageBox.Yes:
            parent_layout = self.parentWidget().layout() if self.parentWidget() else None
            if parent_layout:
                parent_layout.removeWidget(self)
        
        # Step 2: Delete the widget
            self.setParent(None)  # Detach from any parent widget
            self.deleteLater()  # Schedule for deletion

        # Step 3: Refresh the layout if possible
            if parent_layout:
                parent_layout.update() 
                print(f"Checkpoint widget for step ID {self.step_id} deleted.")
    def load_existing_checkpoints(self):
        checkpoints = [cp for cp in CheckpointObject.checkpoint_list if cp.procedure_step_id == self.step_id]
        print(f"Loading {len(checkpoints)} checkpoints for step ID: {self.step_id}")
        for checkpoint in checkpoints:
            print(f"Loading checkpoint: {checkpoint.name}, {checkpoint.item_state}, {checkpoint.person_state}")
            self.add_row(checkpoint.name, checkpoint.item_state, checkpoint.person_state)

    def add_row(self, checkpoint_name, item_state, person_state):
        """Adds a new row to display the checkpoint in the ListWidget."""
        # Create an instance of the second form to add data
        item_widget = QtWidgets.QWidget()
        ui_form = Ui_setReqInputRow()
        ui_form.setupUi(item_widget)

    # Set the text for checkpoint name, system name, parameter, and unit labels
        ui_form.checkpointName.setText(f"<html><head/><body><p><span style=\" font-weight:600;\">{checkpoint_name}</span></p></body></html>")
        ui_form.systemName.setText(f"<html><head/><body><p><span style=\" font-weight:600;\">{item_state}</span></p></body></html>")
        ui_form.parameterLbael.setText(person_state)  # You may need to fix the spelling 'parameterLabel'
        

    # Create a QListWidgetItem
        list_item = QtWidgets.QListWidgetItem(self.req_input_listWidget)
        list_item.setSizeHint(item_widget.sizeHint())  # Set the size of the widget

    # Add the widget to the QListWidget
        self.req_input_listWidget.addItem(list_item)
        self.req_input_listWidget.setItemWidget(list_item, item_widget)

    #def clear_checkpoint_list(self):
        
        # Clear database checkpoints
        #CheckpointObject.checkpoint_list.clear()
        #print("Clearing checkpoints from database and memory.")
        #session = Database.get_session()
    
        #try:
            #deleted_count = session.query(Checkpoint).delete()
            #print(f"Deleted {deleted_count} checkpoints from the database.")
            #session.commit()
        #except Exception as e:
            #print(f"Error clearing database checkpoints: {e}")
            #session.rollback()
        #finally:
            #session.close()

    # Clear the in-memory checkpoint list
        #CheckpointObject.checkpoint_list.clear()
        #print("In-memory checkpoint list after clear:", CheckpointObject.checkpoint_list)