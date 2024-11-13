from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
from Checkpoint_Input_Manager import CheckpointManager

class StepContainerWidget(QWidget):
    def __init__(self, step_widget, parent=None):
        super(StepContainerWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        
        
        # Add FlightPhaseStep widget to the container at the top
        self.step_widget = step_widget
        self.layout.addWidget(self.step_widget)

        # Container for checkpoints
        self.checkpoints_container = QWidget()
        self.checkpoints_layout = QVBoxLayout(self.checkpoints_container)
        self.checkpoints_container.setLayout(self.checkpoints_layout)
        self.checkpoints_container.setVisible(False)
        self.layout.addWidget(self.checkpoints_container)
        
        # Button to toggle visibility of checkpoints - add it after everything else
        self.toggle_button = QPushButton("Show Checkpoints ▼", self)
        self.toggle_button.clicked.connect(self.toggle_checkpoints)
        self.layout.addWidget(self.toggle_button)
        self.step_widget.checkpoint_added.connect(self.add_checkpoint)

    def toggle_checkpoints(self):
        """Toggle the visibility of the checkpoints container."""
        visible = not self.checkpoints_container.isVisible()
        self.checkpoints_container.setVisible(visible)
        self.toggle_button.setText("Hide Checkpoints ▲" if visible else "Show Checkpoints ▼")

    def add_checkpoint(self, procedure_step_id, checkpoint_data):
        """Add a checkpoint widget to the container."""
        checkpoint_widget = CheckpointManager(procedure_step_id)
        checkpoint_widget.setStyleSheet("""
            QWidget {
                background-color: rgb(255, 255, 255);
                border: 3px solid red;
                border-radius: 3px;
            }
        """)
        checkpoint_widget.create_checkpoint(
            checkpoint_name=checkpoint_data["checkpoint_name"],
            item_state=checkpoint_data["item_state"],
            person_state=checkpoint_data["person_state"]
        )
        self.checkpoints_layout.addWidget(checkpoint_widget)
        print(f"Checkpoint widget added with name: {checkpoint_data['checkpoint_name']}")
