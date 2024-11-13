from sqlalchemy.orm import sessionmaker
from Database1 import Checkpoint, Database
from prettytable import PrettyTable

class DbCheckpointEdition:

    @staticmethod
    def read_table():
        session = Database.get_session()
        results = session.query(Checkpoint).all()
        session.close()
        return results

    @staticmethod
    def print_table():
        checkpoints = DbCheckpointEdition.read_table()
        table = PrettyTable(
            ["ID", "Name", "Item State", "Set Req Input", "Person State", "Procedure Step ID"]
        )  # Define column headers

        for row in checkpoints:  # Populate rows
            table.add_row(
                [row.id, row.name, row.item_state, row.set_req_input, row.person_state, row.procedure_step_id]
            )  # Write rows into the table

        print(table)

    @staticmethod
    def new_entry(name, item_state, set_req_input, person_state, procedure_step_id):
        session = Database.get_session()

        checkpoint = Checkpoint(
            name=name,
            item_state=item_state,
            set_req_input=set_req_input,  # New field
            person_state=person_state,
            procedure_step_id=procedure_step_id
        )  # Create a new Checkpoint object

        session.add(checkpoint)  # Add object to database
        session.commit()  # Commit changes
        session.close()

    @staticmethod
    def delete_entry(entry_id):
        session = Database.get_session()
        session.query(Checkpoint).filter(
            Checkpoint.id == entry_id
        ).delete()  # Delete entry with matching ID
        session.commit()
        session.close()

    @staticmethod
    def change_entry(id, name=None, item_state=None, set_req_input=None, person_state=None, procedure_step_id=None):
        session = Database.get_session()

        # Define updates for each non-None parameter
        updates = {}
        if name: updates[Checkpoint.name] = name
        if item_state: updates[Checkpoint.item_state] = item_state
        if set_req_input: updates[Checkpoint.set_req_input] = set_req_input  # New field
        if person_state: updates[Checkpoint.person_state] = person_state
        if procedure_step_id: updates[Checkpoint.procedure_step_id] = procedure_step_id

        # Apply updates
        session.query(Checkpoint).filter(Checkpoint.id == id).update(updates, synchronize_session="fetch")
        session.commit()
        session.close()
    #@staticmethod
    #def delete_all_entries():
        
        #session = Database.get_session()
        #try:
            #deleted_count = session.query(Checkpoint).delete()
            #session.commit()
            #print(f"Deleted {deleted_count} checkpoints from the database.")
        #except Exception as e:
            #session.rollback()
            #print(f"Error deleting all checkpoints from the database: {e}")
       # finally:
            #session.close()