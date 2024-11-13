class Db:
    @staticmethod
    def save_phase(phase_name, type_of_operation_id, order_number):
        """Save phase details to the database."""
        print(f"Saving phase: {phase_name}, Operation ID: {type_of_operation_id}, Order: {order_number}")
        # Add actual database logic to save the phase

    
    @staticmethod
    def fetch_phases():
        """Fetch all phases from the database."""
        session = Database.get_session()  # Obtain a session from your Database class
        try:
            # Fetch all records from the 'Phase' table
            phases = session.query(Phase).all()

            # Convert the fetched phases into a list of dictionaries
            phases_list = [
                {
                'id': phase.id,
                'name': phase.name,
                'type_of_operation_id': phase.type_of_operation_id,
                'order_number': phase.order_number
                }
                for phase in phases
            ]
            return phases_list

        finally:
            session.close()

class EnterNewPhaseDialog(QDialog, Ui_Dialog):
    phase_selected_signal = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(EnterNewPhaseDialog, self).__init__(parent)
        self.setupUi(self)

        # In-memory list to store phases during runtime
        self.phases = Database.fetch_phases()
        self.operation_types = TypeOfOperationObject.type_of_operation_list  # Assuming it's already populated

        # Fill combo boxes with operation types and existing phases
        self.fill_operation_combobox()
        self.fill_phase_position_combobox()

        self.enter_new_phase_buttonBox.accepted.connect(self.on_accept_button_clicked)
        self.enter_new_phase_buttonBox.rejected.connect(self.reject)

    def fill_operation_combobox(self):
        """Fills the combo box with operation types from TypeOfOperationObject."""
        self.corresponding_operation_comboBox.clear()
        for operation in self.operation_types:
            self.corresponding_operation_comboBox.addItem(operation.type_of_operation, operation.id)
        self.corresponding_operation_comboBox.setCurrentIndex(-1)

    def fill_phase_position_combobox(self):
        """Fills the phase position combo box with existing phases."""
        self.position_comboBox.clear()
        self.position_comboBox.addItem("First Position", 0)

        sorted_phases = sorted(self.phases, key=lambda x: x['order_number'])
        for phase in sorted_phases:
            self.position_comboBox.addItem(phase["name"], phase["id"])
        self.position_comboBox.setCurrentIndex(-1)

    def save_phase(self, phase_name, type_of_operation_id, order_number):
        new_phase = {'name': phase_name, 'type_of_operation_id': type_of_operation_id, 'order_number': order_number}
        self.phases.append(new_phase)

        Db.save_phase(phase_name, type_of_operation_id, order_number)
        self.fill_phase_position_combobox()

    def enter_new_phase(self):
        new_phase_name = self.enter_new_phase_lineEdit.text()
        operation_type_id = self.corresponding_operation_comboBox.itemData(self.corresponding_operation_comboBox.currentIndex())

        if not new_phase_name:
            self.enter_new_phase_lineEdit.setStyleSheet("border: 1px solid red;")
            return

        if self.position_comboBox.currentIndex() == 0:
            order_number = 1
        else:
            last_phase_id = self.position_comboBox.itemData(self.position_comboBox.currentIndex())
            last_phase = next((phase for phase in self.phases if phase['id'] == last_phase_id), None)
            order_number = last_phase['order_number'] + 1 if last_phase else 1

        self.save_phase(new_phase_name, operation_type_id, order_number)
        self.phase_selected_signal.emit(new_phase_name)
        self.close()

    def on_accept_button_clicked(self):
        self.enter_new_phase()

    def update_lists_local(self):
        (
            self.item_list,
            self.procedure_list,
            self.procedure_step_list,
            self.type_of_operation_list,
            self.system_state_list,
            self.phase_list,
            self.checkpoint_list,
        ) = update_lists()    


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    dialog = EnterNewPhaseDialog()
    dialog.show()
    sys.exit(app.exec_())
