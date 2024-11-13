from sqlalchemy.orm import sessionmaker
from Database1 import ProcedureStep, Database
from prettytable import PrettyTable
import sqlite3 
import json


class DbProcedureStepEdition:
    
    @staticmethod
    def read_table():
        session = Database.get_session()
        results = session.query(ProcedureStep).all()
        session.close()
        return results

    @staticmethod
    def print_table():
        steps = DbProcedureStepEdition.read_table()
        table = PrettyTable(
            ["ID", "Object Name", "Action", "Order Step",  "Executed By", "Procedure ID", "Item ID"]
        )  # Define column headers

        for row in steps:  # Populate rows
            table.add_row(
                [row.id, row.object_name,  row.action, row.order_step, row.executed_by, row.procedure_id,row.item_id]
            )  # Write rows into the table

        print(table)

    @staticmethod
    def new_entry(object_name,  action, order_step, executed_by, required_input_state, output_state, physical_features, rationale, comments, change_history, procedure_id,item_id):
        session = Database.get_session()

        procedure_step = ProcedureStep(
            object_name=object_name,
            action=action, 
            order_step=order_step, 
             
            executed_by=executed_by, 
            required_input_state=required_input_state, 
            output_state=output_state, 
            physical_features=physical_features, 
            rationale=rationale, 
            comments=comments, 
            change_history=change_history, 
            procedure_id=procedure_id,
            item_id = item_id
        )  # Create a new ProcedureStep object

        session.add(procedure_step)  # Add object to database
        session.commit()  # Commit changes
        session.close()

    @staticmethod
    def delete_entry(entry_id):
        session = Database.get_session()
        session.query(ProcedureStep).filter(
            ProcedureStep.id == entry_id
        ).delete()  # Delete entry with matching ID
        session.commit()
        session.close()

    @staticmethod
    def change_entry(id, object_name=None, action=None,order_step=None,  executed_by=None, required_input_state=None, output_state=None, physical_features=None, rationale=None, comments=None, change_history=None, procedure_id=None, item_id=None):
        if isinstance(change_history, list):
            change_history = json.dumps(change_history)
        session = Database.get_session()
        print(f"Updating DB entry for ID {id} with OrderStep {order_step}")
        # Define updates for each non-None parameter
        updates = {}
        if object_name is not None: updates[ProcedureStep.object_name] = object_name
        if action is not None: updates[ProcedureStep.action] = action
        if order_step is not None: updates[ProcedureStep.order_step] = order_step
        if executed_by is not None: updates[ProcedureStep.executed_by] = executed_by
        if required_input_state is not None: updates[ProcedureStep.required_input_state] = required_input_state
        if output_state is not None: updates[ProcedureStep.output_state] = output_state
        if physical_features is not None: updates[ProcedureStep.physical_features] = physical_features
        if rationale is not None: updates[ProcedureStep.rationale] = rationale
        if comments is not None: updates[ProcedureStep.comments] = comments
        if change_history is not None: updates[ProcedureStep.change_history] = change_history
        if procedure_id is not None: updates[ProcedureStep.procedure_id] = procedure_id
        if item_id is not None: updates[ProcedureStep.item_id] = item_id
        
        # Apply updates
        session.query(ProcedureStep).filter(ProcedureStep.id == id).update(updates, synchronize_session="fetch")
        session.commit()
        session.close()
    #@classmethod
    #def change_entry(cls, step_id, **kwargs):
        # Establish a database connection
        #connection = sqlite3.connect('your_database_file.db')  # Replace with your database file
        #cursor = connection.cursor()

        # Build the query string
        #query = "UPDATE procedure_steps SET "
        #query += ", ".join([f"{key} = ?" for key in kwargs.keys()])
        #query += " WHERE id = ?"

        #try:
            # Execute the query
            #cursor.execute(query, list(kwargs.values()) + [step_id])
            #connection.commit()  # Commit the changes
            #print(f"Database updated for step {step_id}")
       #except sqlite3.Error as e:
            #print(f"Error updating procedure step: {e}")
        #finally:
            # Always close the cursor and connection
            #cursor.close()
            #connection.close()
    