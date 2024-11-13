from sqlalchemy.orm import sessionmaker
from prettytable import PrettyTable
from Database1 import Phase, Database 

class DbPhaseEdition:
    @staticmethod
    def read_table():
        """
        Retrieve all entries from the 'Phase' table.
        """
        session = Database.get_session()
        results = session.query(Phase).all()
        session.close()
        return results

    @staticmethod
    def print_table():
        """
        Print the 'Phase' table in a formatted table.
        """
        phases = DbPhaseEdition.read_table()
        table = PrettyTable(
            [
                "ID",
                "Name",
                "Order Number",
                "Input State",
                "Output State",
                "Procedure List",
                "Type Of Operation ID"
            ]
        )  # Define the column headers

        for row in phases:
            table.add_row(
                [
                    row.id,
                    row.name,
                    row.order_number,
                    row.input_state,
                    row.output_state,
                    row.procedure_list,
                    row.type_of_operation_id
                ]
            )
        print(table)

    @staticmethod
    def new_entry(name, order_number, input_state, output_state, procedure_list, type_of_operation_id):
        """
        Create a new entry in the 'Phase' table.
        """
        session = Database.get_session()
        phase = Phase(name, order_number, input_state, output_state, procedure_list, type_of_operation_id)
        session.add(phase)
        session.commit()
        session.close()

    @staticmethod
    def delete_entry(EntryID):
        """
        Delete an entry from the 'Phase' table based on the given ID.
        """
        session = Database.get_session()
        session.query(Phase).filter(Phase.id == EntryID).delete()
        session.commit()
        session.close()

    @staticmethod
    def change_entry(ID, name, order_number, input_state, output_state, procedure_list, type_of_operation_id):
        """
        Update an existing entry in the 'Phase' table.
        """
        session = Database.get_session()
        session.query(Phase).filter(Phase.id == ID).update(
            {
                Phase.name: name,
                Phase.order_number: order_number,
                Phase.input_state: input_state,
                Phase.output_state: output_state,
                Phase.procedure_list: procedure_list,
                Phase.type_of_operation_id: type_of_operation_id,
            },
            synchronize_session="fetch",
        )
        session.commit()
        session.close()
    @staticmethod
    def fetch_phases():
        """Fetch all phases from the database."""
        session = Database.get_session()  # Get the session from your Database class
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