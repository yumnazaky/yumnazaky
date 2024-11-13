from sqlalchemy.orm import sessionmaker
from Database1 import Procedure, Database
from prettytable import PrettyTable

class DbProcedureEdition:
    
    @staticmethod
    def read_table():
        session = Database.get_session()
        results = session.query(Procedure).all()
        session.close()
        return results

    @staticmethod
    def print_table():
        procedures = DbProcedureEdition.read_table()
        table = PrettyTable(
            [
                "ID", 
                "Name", 
                "Input State", 
                "Output State", 
                "Procedure Step List", 
                "References", 
                "Comments", 
                "Phase ID"
            ]
        )  # Define column headers

        for row in procedures:  # Populate rows
            table.add_row(
                [
                    row.id, 
                    row.name, 
                    row.input_state, 
                    row.output_state, 
                    str(row.procedure_step_list),  # Convert JSON list to string
                    row.references_procedure, 
                    row.comments_procedure, 
                    row.phase_id
                ]
            )
        print(table)

    @staticmethod
    def new_entry(name, input_state, output_state, procedure_step_list, references_procedure, comments_procedure, phase_id):
        session = Database.get_session()

        # Create a new Procedure object
        procedure = Procedure(
            name=name, 
            input_state=input_state, 
            output_state=output_state, 
            procedure_step_list=procedure_step_list,  # This should be a list (stored as JSON)
            references_procedure=references_procedure, 
            comments_procedure=comments_procedure, 
            phase_id=phase_id
        )

        session.add(procedure)  # Add object to the database
        session.commit()  # Commit changes
        session.close()

    @staticmethod
    def delete_entry(entry_id):
        session = Database.get_session()
        session.query(Procedure).filter(Procedure.id == entry_id).delete()
        session.commit()
        session.close()

    @staticmethod
    def change_entry(id, name=None, input_state=None, output_state=None, procedure_step_list=None, references_procedure=None, comments_procedure=None, phase_id=None):
        session = Database.get_session()

        # Define updates for each non-None parameter
        updates = {}
        if name: updates[Procedure.name] = name
        if input_state: updates[Procedure.input_state] = input_state
        if output_state: updates[Procedure.output_state] = output_state
        if procedure_step_list: updates[Procedure.procedure_step_list] = procedure_step_list
        if references_procedure: updates[Procedure.references_procedure] = references_procedure
        if comments_procedure: updates[Procedure.comments_procedure] = comments_procedure
        if phase_id: updates[Procedure.phase_id] = phase_id

        # Apply updates
        session.query(Procedure).filter(Procedure.id == id).update(updates, synchronize_session="fetch")
        session.commit()
        session.close()
