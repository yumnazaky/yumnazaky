import configparser
import os
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import subqueryload
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey,
    Sequence,
    JSON,
)

from sqlalchemy.orm import declarative_base

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))
# Navigate up one directory
parent_dir = os.path.dirname(current_dir)
# Specify the relative path to the "Databases" directory
databases_dir = os.path.join(parent_dir, "databases1")

Base = declarative_base()

# Class representing TypeOfOperation
class TypeOfOperation(Base):
    __tablename__ = 'type_of_operation'
    id = Column(Integer, Sequence('type_of_operation_id_seq'), primary_key=True)

    type_of_operation = Column(String)
    type_of_mission = Column(String)
    references = Column(String)
    comments = Column(String)
    phase_list = Column(JSON)

    # Stores a list of phases (one-to-many relationship)
    phases = relationship('Phase', order_by='Phase.id', back_populates='type_of_operation', cascade="all, delete-orphan")
    #phases = relationship('Phase', order_by='Phase.id', back_populates='type_of_operation', lazy='joined')
    def __init__(self, type_of_operation, type_of_mission, references, comments, phase_list):
        self.type_of_operation = type_of_operation
        self.type_of_mission = type_of_mission
        self.references = references
        self.comments = comments
        self.phase_list = phase_list

    def __repr__(self):
        return f"TypeOfOperation(id={self.id}, type_of_operation={self.type_of_operation}, type_of_mission={self.type_of_mission})"


# Class representing Phase
class Phase(Base):
    __tablename__ = 'phase'
    id = Column(Integer, Sequence('phase_id_seq'), primary_key=True)
    name = Column(String)
    order_number = Column(String)
    input_state = Column(String)
    output_state = Column(String)
    procedure_list = Column(JSON)  # Stores a list of procedures
    type_of_operation_id = Column(Integer, ForeignKey('type_of_operation.id'))
    type_of_operation = relationship('TypeOfOperation', back_populates='phases')

    def __init__(self, name, order_number,input_state, output_state, procedure_list, type_of_operation_id):
        self.name = name
        self.order_number = order_number
        self.input_state = input_state
        self.output_state = output_state
        self.procedure_list = procedure_list
        self.type_of_operation_id = type_of_operation_id

    def __repr__(self):
        return f"Phase(id={self.id}, name={self.name}, order_number ={self.order_number},input_state={self.input_state}, output_state={self.output_state}, procedure_list={self.procedure_list})"


# Class representing Procedure
class Procedure(Base):
    __tablename__ = 'procedure'
    id = Column(Integer, Sequence('procedure_id_seq'), primary_key=True)
    name = Column(String)
    input_state = Column(String)
    output_state = Column(String)
    procedure_step_list = Column(JSON)  # Stores a list of procedure steps
    references_procedure = Column(String)
    comments_procedure = Column(String)
    phase_id = Column(Integer, ForeignKey('phase.id'))
    phase = relationship('Phase', back_populates='procedures')

    def __init__(self, name, input_state, output_state, procedure_step_list, references_procedure, comments_procedure, phase_id):
        self.name = name
        self.input_state = input_state
        self.output_state = output_state
        self.references_procedure = references_procedure
        self.procedure_step_list = procedure_step_list
        self.comments_procedure = comments_procedure
        self.phase_id = phase_id

    def __repr__(self):
        return f"Procedure(id={self.id}, name={self.name}, input_state={self.input_state}, output_state={self.output_state})"


Phase.procedures = relationship('Procedure', order_by=Procedure.id, back_populates='phase')


# Class representing ProcedureStep
class ProcedureStep(Base):
    __tablename__ = 'procedure_step'
    id = Column(Integer, Sequence('procedure_step_id_seq'), primary_key=True)
    object_name = Column(String)
    
    action = Column(String)
    order_step = Column(String)
    executed_by = Column(String)
    required_input_state = Column(String)
    output_state = Column(String)
    physical_features = Column(String)
    rationale = Column(String)
    comments = Column(String)
    change_history = Column(String)
    procedure_id = Column(Integer, ForeignKey('procedure.id'))
    procedure = relationship('Procedure', back_populates='procedure_steps')

    item_id = Column(Integer, ForeignKey('item.id'))
    item = relationship('Item', back_populates='steps')

    # Relationship with Checkpoint
    checkpoints = relationship('Checkpoint', back_populates='procedure_step', cascade="all, delete-orphan")

    def __init__(self, object_name,  action, order_step, executed_by, required_input_state, output_state, physical_features, rationale, comments, change_history, procedure_id, item_id):
        self.object_name = object_name
        
        self.action = action
        self.order_step = order_step
        self.executed_by = executed_by
        self.required_input_state = required_input_state
        self.output_state = output_state
        self.physical_features = physical_features
        self.rationale = rationale
        self.comments = comments
        self.change_history = change_history
        self.procedure_id = procedure_id
        self.item_id = item_id

    def __repr__(self):
        return f"ProcedureStep(id={self.id}, object_name={self.object_name},  action={self.action}, order_step={self.order_step}, executed_by={self.executed_by})"


Procedure.procedure_steps = relationship('ProcedureStep', order_by=ProcedureStep.id, back_populates='procedure')


# Class representing Item
class Item(Base):
    __tablename__ = 'item'
    
    id = Column(Integer, primary_key=True,autoincrement=True)
    name = Column(String)
    state_list = Column(String)
    input_param = Column(String)
    output_param = Column(String)
    provides = Column(String)
    requires = Column(String)
    turns_off = Column(String)


    # Add cascade='all, delete-orphan' to automatically delete associated ProcedureStep records
    steps = relationship('ProcedureStep', back_populates='item', cascade="all, delete-orphan")

    def __init__(self, name, state_list, input_param, output_param, provides, requires, turns_off):
        self.name = name
        self.state_list = state_list
        self.input_param = input_param
        self.output_param = output_param
        self.provides = provides
        self.requires = requires
        self.turns_off = turns_off

    def __repr__(self):
        return f"Item(id={self.id}, name={self.name}, input_param={self.input_param}, output_param={self.output_param}, provides={self.provides}, requires={self.requires}, turns_Off={self.turns_off})"

    


# Class representing Checkpoint
class Checkpoint(Base):
    __tablename__ = 'checkpoint'
    id = Column(Integer, Sequence('checkpoint_id_seq'), primary_key=True)
    name = Column(String)
    item_state = Column(String)
    person_state = Column(String)
    procedure_step_id = Column(Integer, ForeignKey('procedure_step.id'))  # Proper ForeignKey linking to ProcedureStep.id

    # Relationship with ProcedureStep (correctly defining the back_populates)
    procedure_step = relationship('ProcedureStep', back_populates='checkpoints')

    def __init__(self, name, item_state, person_state, procedure_step_id):
        self.name = name
        self.item_state = item_state
        self.person_state = person_state
        self.procedure_step_id = procedure_step_id

    def __repr__(self):
        return f"Checkpoint(id={self.id}, name={self.name}, item_state={self.item_state}, person_state={self.person_state})"


# Class representing Person
class Person(Base):
    __tablename__ = 'person'
    id = Column(Integer, Sequence('person_id_seq'), primary_key=True)
    role = Column(String)
    position = Column(String)
    callout_list = Column(JSON)
    action_list = Column(JSON)

    def __init__(self, role, position, callout_list, action_list):
        self.role = role
        self.position = position
        self.callout_list = callout_list
        self.action_list = action_list

    def __repr__(self):
        return f"Person(id={self.id}, role={self.role}, position={self.position})"


# Class representing SystemState
class SystemState(Base):
    __tablename__ = 'system_state'
    id = Column(Integer, Sequence('system_state_id_seq'), primary_key=True)
    name = Column(String)
    item_state = Column(String)
    person_state = Column(String)

    def __init__(self, name, item_state, person_state):
        self.name = name
        self.item_state = item_state
        self.person_state = person_state

    def __repr__(self):
        return f"SystemState(name={self.name}, item_state={self.item_state}, person_state={self.person_state})"
class System(Base):
    __tablename__ = 'system'
    id = Column(Integer, Sequence('system_id_seq'), primary_key=True)
    name = Column(String)
    def __init__(self, name, item_state, person_state):
        self.name = name
    def __repr__(self):
        return f"SystemState(name={self.name})"    
    

class Database:
    engine = None
    config_path = os.path.join(databases_dir, "config.ini")  # Update with the actual path to your config file
    

    @classmethod
    def modify_db_config(cls, db_name):
        """Update the configuration to point to a new or existing database."""
        config = configparser.ConfigParser()
        config.read(cls.config_path)
        if not config.has_section("Database"):
            config.add_section("Database")
        config["Database"]["Name"] = db_name
        with open(cls.config_path, "w") as config_file:
            config.write(config_file)
        print(f"Database configuration updated to {db_name}")
    @classmethod
    def create_new_database(cls, db_name):
        """Create a new SQLite database file with the required tables."""
        # Construct the full path for the new database file
        db_path = os.path.join(os.path.dirname(cls.config_path), db_name)
        
        # Create the SQLite engine with the specified path
        engine = create_engine(f"sqlite:///{db_path}")
        
        # Create all tables in the database based on the Base metadata
        Base.metadata.create_all(engine)
        print(f"New database created at {db_path} with the required structure.")

    @classmethod
    def create_engine(cls):
        """Initialize the database engine from the configuration file."""
        config = configparser.ConfigParser()
        config.read(cls.config_path)
        
        if "Database" in config and "Name" in config["Database"]:
            database_name = config["Database"]["Name"]
            database_path = os.path.join(os.path.dirname(cls.config_path), database_name)
            
            # Initialize the engine
            cls.engine = create_engine(f"sqlite:///{database_path}")
            print(f"Database engine created for {database_path}")
        else:
            raise ValueError("Database name not found in config.ini")

    @classmethod
    def get_session(cls):
        if cls.engine is None:
            cls.create_engine()  # Initialize the engine if not already created
        Session = sessionmaker(bind=cls.engine)
        return Session()  # Return a new session
    #@staticmethod
    #def save_operation(operation_type, mission_type):
        """Save the operation type and mission into the database."""
        #session = Database.get_session()
        #references = ""  # Default to empty string or fetch from the appropriate UI element
        #comments = ""  
        #new_operation = TypeOfOperation(
            #type_of_operation=operation_type,
            #type_of_mission=mission_type,
            #references=references,
            #comments=comments,
            #phase_list=[]
        #)
        #session.add(new_operation)
        #session.commit()
        #print(f"Operation '{operation_type}' with mission '{mission_type}' saved to the database.")    
    #@staticmethod
    #def delete_operation(operation_type):
        #"""Delete an operation type from the database."""
        #session = Database.get_session()
        # Query to find the operation by its type
        #operation_to_delete = session.query(TypeOfOperation).filter_by(type_of_operation=operation_type).first()
        
        #if operation_to_delete:
            #session.delete(operation_to_delete)
            #session.commit()
            #print(f"Operation '{operation_type}' deleted from the database.")
        #else:
            #print(f"Operation '{operation_type}' not found in the database.")
        #session.close()

#if __name__ == "__main__":
    # Example usage
    #Database.create_engine()


    # Create a session
    #session = Database.get_session()

    # Example query (fetch all phases)
    #phases = session.query(Phase).all()
    #for phase in phases:
    #    print(phase)

    # Close the session
    #session.close()