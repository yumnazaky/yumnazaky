from sqlalchemy.orm import sessionmaker
from Database1 import SystemState, Database
from prettytable import PrettyTable

class DbSystemStateEdition:

    @staticmethod
    def read_table():
        session = Database.get_session()
        results = session.query(SystemState).all()
        session.close()
        return results

    @staticmethod
    def print_table():
        system_states = DbSystemStateEdition.read_table()
        table = PrettyTable(
            ["ID", "Name", "Item State", "Person State"]
        )  # Define column headers

        for row in system_states:  # Populate rows
            table.add_row(
                [row.id, row.name, row.item_state, row.person_state]
            )  # Write rows into the table

        print(table)

    @staticmethod
    def new_entry(name, item_state, person_state):
        session = Database.get_session()

        system_state = SystemState(
            name=name,
            item_state=item_state,
            person_state=person_state
        )  # Create a new SystemState object

        session.add(system_state)  # Add object to database
        session.commit()  # Commit changes
        session.close()

    @staticmethod
    def delete_entry(entry_id):
        session = Database.get_session()
        session.query(SystemState).filter(
            SystemState.id == entry_id
        ).delete()  # Delete entry with matching ID
        session.commit()
        session.close()

    @staticmethod
    def change_entry(id, name=None, item_state=None, person_state=None):
        session = Database.get_session()

        # Define updates for each non-None parameter
        updates = {}
        if name: updates[SystemState.name] = name
        if item_state: updates[SystemState.item_state] = item_state
        if person_state: updates[SystemState.person_state] = person_state

        # Apply updates
        session.query(SystemState).filter(SystemState.id == id).update(updates, synchronize_session="fetch")
        session.commit()
        session.close()
