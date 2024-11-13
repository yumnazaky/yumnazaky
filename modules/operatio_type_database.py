from Database1 import TypeOfOperation, Database
from prettytable import PrettyTable
from sqlalchemy.orm import sessionmaker

class DbTypeOfOperationEdition:
    @staticmethod
    def read_table():
        """
        Retrieve all entries from the 'TypeOfOperation' table.
        """
        session = Database.get_session()
        results = session.query(TypeOfOperation).all()
        session.close()
        return results

    @staticmethod
    def print_table():
        """
        Print the 'TypeOfOperation' table in a formatted table.
        """
        items = DbTypeOfOperationEdition.read_table()
        table = PrettyTable(
            [
                "ID",
                "Type of Operation",
                "Type of Mission",
                "References",
                "Comments",
                "Phase List"
            ]
        )  # Define the column headers

        for row in items:
            table.add_row(
                [
                    row.id,
                    row.type_of_operation,
                    row.type_of_mission,
                    row.references,
                    row.comments,
                    row.phase_list
                ]
            )
        print(table)

    @staticmethod
    def new_entry(type_of_operation, type_of_mission, references, comments, phase_list):
        """
        Create a new entry in the 'TypeOfOperation' table.

        """
        if phase_list is None:
            phase_list = [] 
        session = Database.get_session()
        operation = TypeOfOperation(type_of_operation, type_of_mission, references, comments, phase_list)
        session.add(operation)
        session.commit()
        session.close()

    @staticmethod
    def delete_entry(ID):
        """
        Delete an entry from the 'TypeOfOperation' table based on the given ID.
        """
        session = Database.get_session()
        session.query(TypeOfOperation).filter(TypeOfOperation.id == ID).delete()
        session.commit()
        session.close()

    @staticmethod
    def change_entry(ID, type_of_operation, type_of_mission, references, comments, phase_list):
        """
        Update an existing entry in the 'TypeOfOperation' table.
        """
        session = Database.get_session()
        session.query(TypeOfOperation).filter(TypeOfOperation.id == ID).update(
            {
                TypeOfOperation.type_of_operation: type_of_operation,
                TypeOfOperation.type_of_mission: type_of_mission,
                TypeOfOperation.references: references,
                TypeOfOperation.comments: comments,
                TypeOfOperation.phase_list: phase_list
            },
            synchronize_session="fetch",
        )
        session.commit()
        session.close()
