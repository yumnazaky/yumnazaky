from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import text
from prettytable import PrettyTable
from Database1 import Item, Database
import json

    #@staticmethodimport sqlalchemy
import importlib

class DbItemEdition:
    @staticmethod
    def read_table():
        """
        Retrieve all entries from the 'Item' table.
        """
        session = Database.get_session()
        results = session.query(Item).all()
        for item in results:
            print(f"Raw Database Values - ID: {item.id}, Provides: {item.provides}, Requires: {item.requires}, Turns Off: {item.turns_off}")

            item.state_list = json.loads(item.state_list) if isinstance(item.state_list, str) else item.state_list
            item.provides = json.loads(item.provides) if isinstance(item.provides, str) else item.provides
            item.requires = json.loads(item.requires) if isinstance(item.requires, str) else item.requires
            item.turns_off = json.loads(item.turns_off) if isinstance(item.turns_off, str) else item.turns_off    
  
        session.close()
        return results

    @staticmethod
    def print_table():
        """
        Print the 'Item' table in a formatted table.
        """
        items = DbItemEdition.read_table()
        table = PrettyTable(
            [
                "ID",
                "Name",
                "State List",
                "Input Param",
                "Output Param",
                "Provides",
                "Requires",
                "Turns Off",
            ]
        )  # Define the column headers

        for row in items:
            state_list = json.loads(row.state_list) if isinstance(row.state_list, str) else row.state_list
            provides = json.loads(row.provides) if isinstance(row.provides, str) else row.provides
            requires = json.loads(row.requires) if isinstance(row.requires, str) else row.requires
            turns_off = json.loads(row.turns_off) if isinstance(row.turns_off, str) else row.turns_off
            table.add_row(
                [
                    row.id,
                    row.name,
                    row.state_list,
                    row.input_param,
                    row.output_param,
                    row.provides,
                    row.requires,
                    row.turns_Off,
                ]
            )
        print(table)

    @staticmethod
    def new_entry(name, state_list, input_param, output_param, provides, requires, turns_off):
        session = Database.get_session()
        serialized_state_list = json.dumps(state_list)
        serialized_provides = json.dumps(provides)
        serialized_requires = json.dumps(requires)
        serialized_turns_off = json.dumps(turns_off)
        item = Item(
            name=name,
            state_list=serialized_state_list,
            input_param=input_param,
            output_param=output_param,
            provides=serialized_provides,
            requires=serialized_requires,
            turns_off=serialized_turns_off
        )
        session.add(item)
        session.commit()
        session.close()

    @staticmethod
    def delete_entry(EntryID):
        """
        Delete an entry from the 'Item' table based on the given ID.
        """
        session = Database.get_session()
        session.query(Item).filter(Item.id == EntryID).delete()
        session.commit()

        session.close()

    @staticmethod
    def change_entry(ID, name, state_list, input_param, output_param, provides, requires, turns_off):
        """
        Update an existing entry in the 'Item' table.
        """
        session = Database.get_session()
        serialized_state_list = json.dumps(state_list)
        serialized_provides = json.dumps(provides)
        serialized_requires = json.dumps(requires)
        serialized_turns_off = json.dumps(turns_off)
        session.query(Item).filter(Item.id == ID).update(
            {
                Item.name: name,
                Item.state_list: serialized_state_list,
                Item.input_param: input_param,
                Item.output_param: output_param,
                Item.provides: serialized_provides,
                Item.requires: serialized_requires,
                Item.turns_off: serialized_turns_off,
            },
            synchronize_session="fetch",
        )
        session.commit()
        session.close()
    #@staticmethod
    #def load_item_states(item_id):
        
        #session = Database.get_session()
        #item = session.query(Item).filter(Item.id == item_id).first()
        #session.close()
        #if item:
            # Deserialize JSON strings to lists if they exist, or default to empty lists
            #return {
                #"provides": json.loads(item.provides) if item.provides else [],
                #"requires": json.loads(item.requires) if item.requires else [],
                #"turns_off": json.loads(item.turns_off) if item.turns_off else []
            #}
        #else:
            #print(f"No item found with ID {item_id}")
            #return None    
   # def clear_table():
      
        #session = Database.get_session()
        
        # Delete all entries in the Item table
        #session.execute(text("DELETE FROM Item"))
        
        # Optional: Only reset `sqlite_sequence` if it exists
        #try:
            #session.execute(text("DELETE FROM sqlite_sequence WHERE name='Item'"))
        #except sqlalchemy.exc.OperationalError:
            #print("sqlite_sequence table not found; skipping reset.")

        #session.commit()
        #session.close()
