from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from database_item import DbItemEdition
from operatio_type_database import DbTypeOfOperationEdition
from procedure_step_database import DbProcedureStepEdition
from flightphase_database import DbPhaseEdition
from checkpoint_database import DbCheckpointEdition
from procedure_database import  DbProcedureEdition
from system_state_db import DbSystemStateEdition
import math
import traceback
from prettytable import PrettyTable
import json 
import time

class ItemObject:
    item_list = []
    _defaults_initialized = False
    id_counter = 1 
    item_state_list = {}  # List of ItemObjects
    default_systems = [
        {"name": "Altitude Indicator", "item_state": "", "person_state": ""},
        {"name": "Anti Collision Light", "item_state": "", "person_state": ""},
        {"name": "Autopilot", "item_state": "", "person_state": ""},
        {"name": "Avionics Master", "item_state": "", "person_state": ""},
        {"name": "Brakes", "item_state": "", "person_state": ""},
        {"name": "Cabin Pressure", "item_state": "", "person_state": ""},
        {"name": "Flaps", "item_state": "", "person_state": ""},
        {"name": "Fuel Pump", "item_state": "", "person_state": ""},
        {"name": "Fuel Switch", "item_state": "", "person_state": ""},
        {"name": "Generator", "item_state": "", "person_state": ""},
        {"name": "Landing Gear", "item_state": "", "person_state": ""},
        {"name": "Avionics Master", "item_state": "", "person_state": ""},
        {"name": "Magnets", "item_state": "", "person_state": ""},
        {"name": "Master", "item_state": "", "person_state": ""},
        {"name": "Mixture", "item_state": "", "person_state": ""},
        {"name": "Navigation Lights", "item_state": "", "person_state": ""},
        {"name": "Oil Pressure and Temprature", "item_state": "", "person_state": ""},
        {"name": "Parking Brake", "item_state": "", "person_state": ""},
        {"name": "Position-Light", "item_state": "", "person_state": ""},
        {"name": "Power Lever", "item_state": "", "person_state": ""},
        {"name": "Propeller", "item_state": "", "person_state": ""},
        {"name": "Radio", "item_state": "", "person_state": ""},
        {"name": "Starter", "item_state": "", "person_state": ""},
        {"name": "Stick", "item_state": "", "person_state": ""},
        {"name": "Tailwheel Lock", "item_state": "", "person_state": ""},
        {"name": "Transponder", "item_state": "", "person_state": ""},
        {"name": "Trim", "item_state": "", "person_state": ""},# Add more default systems as required
    ]

    def __init__(self, ID=None, name="", state_list=None, input_param="", output_param="", provides=None, requires=None, turns_off=None):
        
        

        self.id = ID if ID is not None else ItemObject.id_counter
        ItemObject.id_counter += 1 if ID is None else 0
        # Increment the counter for the next object
        self.name = name
        self.state_list = state_list or {"provides": provides, "requires": requires, "turns_off": turns_off}  
        #self.state_list = state_list
        self.input_param = input_param
        self.output_param = output_param
        self.provides = provides if isinstance(provides, list) else []
        self.requires = requires if isinstance(requires, list) else []
        self.turns_off = turns_off if isinstance(turns_off, list) else []
        if not any(item.name == self.name for item in ItemObject.item_list):
            ItemObject.item_list.append(self)

    def __repr__(self):
        return f"({self.id}, {self.name}, {self.state_list}, {self.input_param}, {self.output_param}, {self.provides}, {self.requires}, {self.turns_off})"
    # List of default systems
    @classmethod
    def add_unique_item(cls, new_item):
        if not any(item.name == new_item.name for item in cls.item_list):
            cls.item_list.append(new_item)
            print(f"Added unique item: {new_item.name}")
        else:
            print(f"Item '{new_item.name}' already exists, skipping addition.")
    
    # Ensure each default system is unique and added only once
    @classmethod
    def initialize_default_systems(cls):
        if cls._defaults_initialized:
            return
        cls._defaults_initialized = True
        unique_items = {}
        for system in cls.default_systems:
            if system['name'] not in unique_items:    
                new_item = cls(
                    ID=None,
                    name=system['name'],
                    state_list={"provides": [], "requires": [], "turns_off": []},
                    input_param="",
                    output_param="",
                    provides=[],
                    requires=[],
                    turns_off=[]
                )
                unique_items[system['name']] = new_item

        # Set item_list to only unique values from unique_items
        cls.item_list = list(unique_items.values())
        
        print("Initialized default systems in ItemObject.item_list")

        print("Final state of ItemObject.item_list:", [(item.id, item.name) for item in cls.item_list])
    def get_provides(self):
        return self.provides

    def get_requires(self):
        return self.requires

    def get_turns_off(self):
        return self.turns_off

    
    @classmethod
    def new_entry(cls, name, state_list, input_param, output_param, provides, requires, turns_off):
        """Create a new ItemObject entry with a unique ID."""
        new_item = cls(
            ID=cls.id_counter,  # Assign a new ID automatically
            name=name,
            state_list=state_list,
            input_param=input_param,
            output_param=output_param,
            provides=provides,
            requires=requires,
            turns_off=turns_off
        )
        cls.id_counter += 1  # Increment id_counter for the next entry
        cls.item_list.append(new_item)
        print(f"New item added: {new_item}")
    def save_state(self, provides, requires, turns_off):
        """Save the checkbox states to the state_list for persistence."""
        self.state_list.update({"provides": provides, "requires": requires, "turns_off": turns_off})
        ItemObject.item_state_list[self.name] = self.state_list 

    @classmethod
    def load_state(cls, name):
        """Load the state for a given item name from item_state_list if available."""
        return cls.item_state_list.get(name, {"provides": False, "requires": False, "turns_off": False})
  
    
    def delete(self):
        if self.id is not None:
            DbItemEdition.delete_entry(self.id)
            ItemObject.classlist_delete(self.id)
        else:
            print("Object doesn't exist")

    @classmethod
    def classlist_delete(cls, ID):
        cls.item_list = list(filter(lambda x: x.id != ID, cls.item_list))

    @classmethod
    def create_item_list(cls):
        """Load items from the database and initialize item_list."""
        db_item_list = DbItemEdition.read_table()  # Load directly from DB
        cls.item_list = []
        for item in db_item_list:
            cls.item_list.append(cls(
                ID=item.id,
                name=item.name,
                state_list=item.state_list,
                input_param=item.input_param,
                output_param=item.output_param,
                provides=item.provides,
                requires=item.requires,
                turns_off=item.turns_off
            ))
            print(f"Loaded item - ID: {item.id}, Name: {item.name}")


    @classmethod
    def edit_item(cls, ID, name, state_list, input_param, output_param, provides, requires, turns_off):
    # Find the item in item_list by ID
        filtered_item = [item for item in cls.item_list if item.id == ID]
        for item in filtered_item:
        # Update the item fields
            item.name = name
            item.state_list = state_list
            item.input_param = input_param
            item.output_param = output_param
        
        # Ensure provides, requires, and turns_off are stored as comma-separated strings
            item.provides = provides if isinstance(provides, list) else json.loads(provides)
            item.requires = requires if isinstance(requires, list) else json.loads(requires)
            item.turns_off = turns_off if isinstance(turns_off, list) else json.loads(turns_off)
        
        # Debug statement to confirm updates
            print(f"Updated item - ID: {item.id}, Name: {item.name}, Provides: {item.provides}, Requires: {item.requires}, Turns Off: {item.turns_off}")
        
        # Update in the database
            DbItemEdition.change_entry(
                ID, 
                name, 
                state_list, 
                input_param, 
                output_param, 
                json.dumps(item.provides),   # Store as JSON string
                json.dumps(item.requires),   # Store as JSON string
                json.dumps(item.turns_off)  # Convert list to string for DB
            )
        #else:
            #print(f"Item with ID {ID} not found for editing.")
    @classmethod
    def print_table(cls):
        table = PrettyTable(
            [
                "ID",
                "Name",
                "State List",
                "Input Param",
                "Output Param",
                "Provides",
                "Requires",
                "TurnsOff",
            ],
            name="Item Table",
        )

        for row in cls.item_list:
            table.add_row(
                [
                    row.id,
                    row.name,
                    row.state_list,
                    row.input_param,
                    row.output_param,
                    row.provides,
                    row.requires,
                    row.turns_off,
                ]
            )
        print(table)
    @classmethod
    def clear_item_list(cls):
        """Clears the item list to reset the object, useful for testing."""
        cls.item_list.clear()
        cls.id_counter = 1 
    @staticmethod
    def return_item(item_id):
        return next((item for item in ItemObject.item_list if item.id == item_id), None)
class ProcedureObject:
    procedure_list = []  # List to store ProcedureObject instances

    def __init__(self, ID, Name, InputState, OutputState, ProcedureStepList, ReferencesProcedure, CommentsProcedure, PhaseID):
        self.id = ID
        self.name = Name
        self.input_state = InputState
        self.output_state = OutputState
        self.procedure_step_list = ProcedureStepList
        self.references_procedure = ReferencesProcedure
        self.comments_procedure = CommentsProcedure
        self.phase_id = PhaseID

    def delete(self):
        if self.id is not None:
            DbProcedureEdition.delete_entry(self.id)  # Deletes the Procedure from the database
            ProcedureObject.list_delete(self.id)  # Removes Procedure from procedure_list
        else:
            print("Object doesn't exist")

    @classmethod
    def list_delete(cls, ID):
        cls.procedure_list = list(filter(lambda x: x.id != ID, cls.procedure_list))  # Removes the procedure from the list

    def __repr__(self):
        return f"({self.id}, {self.name}, {self.input_state}, {self.output_state}, {self.procedure_step_list}, {self.references_procedure}, {self.comments_procedure}, {self.phase_id})"

    @classmethod
    def create_procedure_list(cls):
        db_procedure_list = DbProcedureEdition.read_table()  # Reads all procedures from the database
        cls.procedure_list = []
        for procedure in db_procedure_list:
            cls.procedure_list.append(
                ProcedureObject(
                    procedure.id,
                    procedure.name,
                    procedure.input_state,
                    procedure.output_state,
                    procedure.procedure_step_list,
                    procedure.references_procedure,
                    procedure.comments_procedure,
                    procedure.phase_id
                )
            )

    @classmethod
    def edit_procedure(cls, ID, Name, InputState, OutputState, ProcedureStepList, ReferencesProcedure, CommentsProcedure, PhaseID):
        filtered_procedure = [procedure for procedure in cls.procedure_list if procedure.id == ID]
        now = datetime.now()
        timestamp = now.strftime("%m/%d/%Y, %H:%M:%S")
        for procedure in filtered_procedure:
            procedure.name = Name
            procedure.input_state = InputState
            procedure.output_state = OutputState
            procedure.procedure_step_list = ProcedureStepList
            procedure.references_procedure = ReferencesProcedure
            procedure.comments_procedure = f"{procedure.comments_procedure}\n{timestamp}: {CommentsProcedure}"
            procedure.phase_id = PhaseID

        DbProcedureEdition.change_entry(ID, Name, InputState, OutputState, ProcedureStepList, ReferencesProcedure, CommentsProcedure, PhaseID)

    @classmethod
    def new_entry(cls, Name, InputState, OutputState, ProcedureStepList, ReferencesProcedure, CommentsProcedure, PhaseID):
        #DbProcedureEdition.new_entry(Name, InputState, OutputState, ProcedureStepList, ReferencesProcedure, CommentsProcedure, PhaseID)
        cls.create_procedure_list()
        new_procedure_id = DbProcedureEdition.new_entry(Name, InputState, OutputState, ProcedureStepList, ReferencesProcedure, CommentsProcedure, PhaseID)

    # Create a new ProcedureObject with the newly generated ID
        new_procedure = ProcedureObject(
            new_procedure_id,  # Pass the new ID retrieved from the database
            Name,
            InputState,
            OutputState,
            ProcedureStepList,
            ReferencesProcedure,
            CommentsProcedure,
            PhaseID
        )
        cls.procedure_list.append(new_procedure)   # Update the list after adding a new entry

    @classmethod
    def print_table(cls):
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
            ],
            name="Procedure List",
        )

        for row in cls.procedure_list:
            table.add_row(
                [
                    row.id,
                    row.name,
                    row.input_state,
                    row.output_state,
                    str(row.procedure_step_list),
                    row.references_procedure,
                    row.comments_procedure,
                    row.phase_id
                ]
            )
        print(table)

    @classmethod
    def return_procedure(cls, ID):
        try:
            for procedure in cls.procedure_list:
                if procedure.id == ID:
                    return procedure
        except:
            print(f"No Procedure with ID {ID} found.")


class ProcedureStepObject:
    procedure_step_list = []  # List to hold ProcedureStep objects

    def __init__(
        self, ID, ObjectName, Action, OrderStep, ExecutedBy, 
        RequiredInputState=None, OutputState="", PhysicalFeatures="", 
        Rationale="", Comments="", ChangeHistory=None, ProcedureID=-1, ItemID=None
    ):
        # Initialize default systems if item_list is empty
        #if not ItemObject.item_list:
            #ItemObject.initialize_default_systems()
        
        # Assign item_id based on provided ID or default if none
        #self.item_id = ItemID if ItemID is not None and ItemID != -1 else (ItemObject.item_list[0].id if ItemObject.item_list else -1)
        
        # Check if assigned item_id is valid in ItemObject
        #item = ItemObject.return_item(self.item_id)
        #if not item:
           # print(f"Warning: Item with ID {self.item_id} not found. Setting item_id to -1.")
            #self.item_id = -1
        #self.load_item_states()
        # Initialize all other attributes
        self.id = ID
        self.object_name = ObjectName
        self.action = Action
        self.order_step = OrderStep
        self.executed_by = ExecutedBy
        self.required_input_state = RequiredInputState if RequiredInputState is not None else ""
        self.output_state = OutputState
        self.physical_features = PhysicalFeatures
        self.rationale = Rationale
        self.comments = Comments
        self.change_history = ChangeHistory if ChangeHistory is not None else []  # Initialize change_history

        self.procedure_id = ProcedureID
        self.item_id =ItemID
        
        # Debug print to confirm object creation
        print(f"Initialized ProcedureStepObject with item_id: {self.item_id}, ID: {self.id}, order_step: {self.order_step}")
    def __repr__(self):
        return f"(ID: {self.id}, Object Name: {self.object_name},  Action: {self.action},Order Step: {self.order_step}, Executed By: {self.executed_by})"
    @classmethod
    def generate_id(cls):
        """Generates a new unique ID for a ProcedureStepObject."""
        if cls.procedure_step_list:
            return max(step.id for step in cls.procedure_step_list) + 1
        else:
            return 1   
    #def load_item_states(self):
        # Fetch the associated item from ItemObject by item_id
        #item = ItemObject.return_item(self.item_id)
        #if item:
            # Assign states from the Item instance to ProcedureStepObject
            #self.provides = item.provides
            #self.requires = item.requires
            #self.turns_off = item.turns_off
        #else:
            # Display a warning if item is not found
            #print(f"Warning: Item with ID {self.item_id} not found.")
    #def assign_default_item_id(self):
        # Assuming you want to assign the first item as default if no ItemID is provided
        #return ItemObject.item_list[0].id if ItemObject.item_list else -1   
    
    def delete(self):
        if self.id is not None:
            DbProcedureStepEdition.delete_entry(self.id)  # Deletes the ProcedureStep from the database
            self.list_harmonisation_delete()  # Harmonizes the order numbers after deletion
            ProcedureStepObject.list_delete(self.id)  # Removes the ProcedureStep from the list
        else:
            print("Object doesn't exist")

    @classmethod
    def list_delete(cls, ID):
        cls.procedure_step_list = list(filter(lambda x: x.id != ID, cls.procedure_step_list))

    

    @classmethod
    def create_procedure_step_list(cls):
        cls.procedure_step_list.clear()
        db_procedure_step_list = DbProcedureStepEdition.read_table()  # Reads all procedure steps from the database
        cls.procedure_step_list = []
        for procedure_step in db_procedure_step_list:
            cls.procedure_step_list.append(
                ProcedureStepObject(
                    procedure_step.id,
                    procedure_step.object_name,
                    procedure_step.action,
                    procedure_step.order_step,
                    procedure_step.executed_by,
                    procedure_step.required_input_state,
                    procedure_step.output_state,
                    procedure_step.physical_features, 
                    procedure_step.rationale,
                    procedure_step.comments,
                    procedure_step.change_history,
                    procedure_step.procedure_id,
                    procedure_step.item_id
                )
            )
            print(f"Initialized ProcedureStepObject with item_id: {procedure_step.item_id}")
    @classmethod
    def edit_procedure_step(cls, ID, ObjectName,  Action,OrderStep, ExecutedBy, RequiredInputState, OutputState, PhysicalFeatures, Rationale, Comments, ChangeHistory, ProcedureID, ItemID):
        print(f"Updating Procedure Step with ID: {ID}")
        print(f" - ObjectName: {ObjectName}")
        print(f" - OrderStep: {OrderStep} (Type: {type(OrderStep)})")
        print(f" - Action: {Action} (Type: {type(Action)})")
        print(f" - ExecutedBy: {ExecutedBy}")

        filtered_step = [step for step in cls.procedure_step_list if step.id == ID]
        for step in filtered_step:
            step.object_name = ObjectName
            
            step.action = Action
            step.order_step = OrderStep
            step.executed_by = ExecutedBy
            step.required_input_state = RequiredInputState
            step.output_state = OutputState
            step.physical_features = PhysicalFeatures
            step.rationale = Rationale
            step.comments = Comments
            step.change_history = ChangeHistory
            step.procedure_id = ProcedureID
            step.item_id = ItemID

        DbProcedureStepEdition.change_entry(ID, ObjectName, Action, OrderStep,  ExecutedBy, RequiredInputState, OutputState, PhysicalFeatures, Rationale, Comments, ChangeHistory, ProcedureID, ItemID)

    @classmethod
    def new_entry(cls, ObjectName,  Action, OrderStep, ExecutedBy, RequiredInputState, OutputState, PhysicalFeatures, Rationale, Comments, ChangeHistory, ProcedureID, ItemID):
     # Add new entry to the database
        physical_features_str = json.dumps(PhysicalFeatures)

        new_id = cls.generate_id()
        DbProcedureStepEdition.new_entry(ObjectName,  Action, OrderStep,ExecutedBy, RequiredInputState, OutputState, physical_features_str, Rationale, Comments, ChangeHistory, ProcedureID, ItemID)
        new_step = ProcedureStepObject(
            ID=new_id,  # Use the generated ID
            ObjectName=ObjectName,
            
            Action=Action,
            OrderStep=OrderStep,
            ExecutedBy=ExecutedBy,
            RequiredInputState=RequiredInputState,
            OutputState=OutputState,
            PhysicalFeatures=PhysicalFeatures,
            Rationale=Rationale,
            Comments=Comments,
            ChangeHistory=ChangeHistory,
            ProcedureID=ProcedureID,
            ItemID=ItemID
        )

       # Update the list and harmonize the order
        cls.create_procedure_step_list()  # Updates the list after adding a new entry
        cls.list_harmonisation_new_entry()

    # Save the newly created step to JSON
        #new_step = cls.procedure_step_list[-1]
        return new_step  # Get the most recently added step
        #new_step.save_to_json("new_procedure_step_data.json")  # Save to JSON file

    @classmethod
    def print_table(cls):
        table = PrettyTable(
            ["ID", "Object Name", "Action", "Order Step","Executed By", "Procedure ID", "Item ID"],
            name="Procedure Step Table"
        )

        for row in cls.procedure_step_list:
            table.add_row(
                [
                    row.id,
                    row.object_name,
                    row.action,
                    row.order_step,
                    row.executed_by,
                    row.procedure_id,
                    row.item_id
                ]
            )
        print(table)

    @classmethod
    def return_procedure_step(cls, ID):
        procedure_step = next((step for step in cls.procedure_step_list if step.id == ID), None)
        if procedure_step is None:
            print(f"No Procedure Step with ID {ID} found.")
            return None
    
    # Ensure item_id is set if it wasn't assigned before
        if procedure_step.item_id == -1 and ItemObject.item_list:
            procedure_step.item_id = ItemObject.item_list[0].id  # Assign the first available item as default
            print(f"Assigned default item_id {procedure_step.item_id} to Procedure Step ID {ID}")
    
        return procedure_step


    @classmethod
    def move_step_up(cls, ON, PID):
        try:
            current_step = [
                step for step in cls.procedure_step_list
                if step.order_step == ON and step.procedure_id == PID
            ]

            upper_step = [
                step for step in cls.procedure_step_list
                if step.order_step == ON - 1 and step.procedure_id == int(PID)
            ]
            if not current_step:
                print(f"No step found at order {ON} for procedure_id {PID}")
                return
            if not upper_step:
                print(f"No step found at order {ON - 1} for procedure_id {PID}")
                return
            current_step[0].edit_procedure_step(
                current_step[0].id, current_step[0].object_name, ON - 1, current_step[0].action,
                current_step[0].executed_by, current_step[0].required_input_state,
                current_step[0].output_state, current_step[0].physical_features,
                current_step[0].rationale, current_step[0].comments, current_step[0].change_history,
                PID, current_step[0].item_id
            )

            upper_step[0].edit_procedure_step(
                upper_step[0].id, upper_step[0].object_name, ON, upper_step[0].action,
                upper_step[0].executed_by, upper_step[0].required_input_state,
                upper_step[0].output_state, upper_step[0].physical_features,
                upper_step[0].rationale, upper_step[0].comments, upper_step[0].change_history,
                PID, upper_step[0].item_id
            )
            print(f"Swapped order of steps {current_step[0].id} and {upper_step[0].id}")
        except Exception:
            traceback.print_exc()

    @classmethod
    def move_step_down(cls, ON, PID):
        try:
            current_step = [
                step for step in cls.procedure_step_list
                if step.order_step == ON and step.procedure_id == PID
            ]

            lower_step = [
                step for step in cls.procedure_step_list
                if step.order_step == ON + 1 and step.procedure_id == PID
            ]
            if not current_step:
                print(f"No step found at order {ON} for procedure_id {PID}")
                return  # Exit if current_step is not found

            if not lower_step:
                print(f"No step found at order {ON + 1} for procedure_id {PID}")
                return 
            current_step[0].edit_procedure_step(
                current_step[0].id, current_step[0].object_name, ON + 1, current_step[0].action,
                current_step[0].executed_by, current_step[0].required_input_state,
                current_step[0].output_state, current_step[0].physical_features,
                current_step[0].rationale, current_step[0].comments, current_step[0].change_history,
                PID, current_step[0].item_id
            )

            lower_step[0].edit_procedure_step(
                lower_step[0].id, lower_step[0].object_name, ON, lower_step[0].action,
                lower_step[0].executed_by, lower_step[0].required_input_state,
                lower_step[0].output_state, lower_step[0].physical_features,
                lower_step[0].rationale, lower_step[0].comments, lower_step[0].change_history,
                PID, lower_step[0].item_id
            )

        except Exception:
            traceback.print_exc()
    #@classmethod
    def list_harmonisation_delete(self):
        """Adjusts the order of remaining steps after a deletion."""
        for step in ProcedureStepObject.procedure_step_list:
            if step.procedure_id == self.procedure_id and int(step.order_step) > int(self.order_step):
                # Decrement the order step
                new_order_step = int(step.order_step) - 1
                step.order_step = new_order_step
                change_history = step.change_history
                if isinstance(change_history, list):
                    change_history = json.dumps(change_history)
                
                # Update each affected step's order in the database
                step.edit_procedure_step(
                    step.id,
                    object_name=step.object_name,
                    action=step.action,
                    order_step=new_order_step,
                    executed_by=step.executed_by,
                    required_input_state=step.required_input_state,
                    output_state=step.output_state,
                    physical_features=step.physical_features,
                    rationale=step.rationale,
                    comments=step.comments,
                    change_history=step.change_history,
                    procedure_id=step.procedure_id,
                    item_id=step.item_id
                )

    @classmethod
    def list_harmonisation_new_entry(cls):
        last_step = cls.procedure_step_list[-1] if cls.procedure_step_list else None
        if not last_step:
            print("[Error] No procedure steps available for harmonisation.")
            return

        procedure_id = last_step.procedure_id
        order_step = last_step.order_step
        id = last_step.id

        print(f"Harmonizing new entry at {time.time()}: procedure_id = {procedure_id}, initial order_step = {order_step}")

        for step in cls.procedure_step_list:
            if step is not None and step.procedure_id == procedure_id:
                if step.order_step >= order_step and step.id != id:
                    step.edit_procedure_step(
                        step.id, step.object_name, step.action, step.order_step + 1,
                        step.executed_by, step.required_input_state, step.output_state,
                        step.physical_features, step.rationale, step.comments,
                        step.change_history, step.procedure_id, step.item_id
                    )
                    print(f"Order Number in new Entry harmonized: {step.order_step}, ID: {step.id}")


    @classmethod
    def edit_procedure_step(cls, step_id, **kwargs):
        step = cls.return_procedure_step(step_id)
        if step:
            for key, value in kwargs.items():
                if hasattr(step, key):
                   setattr(step, key, value)  # Update the attributes
            step.physical_features = kwargs.get('physical_features', step.physical_features)

          # Save changes to the database
            DbProcedureStepEdition.change_entry(step_id, **kwargs)
            print(f"Step {step_id} updated with: {kwargs}")
    def add_change_log(self, change):
        """Add change log entry with timestamp."""
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.change_history.append({"time": timestamp, "change": change})
        print(f"Change logged: {change} at {timestamp}")  
    @classmethod
    def get_procedure_steps_by_id(cls, procedure_id):
        """Fetches and returns a sorted list of procedure steps for a specific procedure_id."""
    
    # Print the full procedure step list before filtering for debugging
        print(f"Full procedure step list: {cls.procedure_step_list}")
    
    # Filter out None entries and select the procedure steps with the matching procedure_id
        procedure_steps = [step for step in cls.procedure_step_list if step is not None and step.procedure_id == procedure_id]
    
    # Add a debug print to show the filtered list of procedure steps
        print(f"Filtered procedure steps for procedure_id {procedure_id}: {procedure_steps}")
    
        return procedure_steps

          


class TypeOfOperationObject:
    # List to hold TypeOfOperation objects
    type_of_operation_list = []

    def __init__(self, ID=None, TypeOfOperation="Untitled Operation", TypeOfMission="", References="", Comments="", PhaseList=None):
        self.id = ID
        self.type_of_operation = TypeOfOperation if TypeOfOperation else "Untitled Operation"
        self.type_of_mission = TypeOfMission if TypeOfMission else ""
        self.references = References if References else ""
        self.comments = Comments if Comments else ""
        self.phase_list = PhaseList if PhaseList is not None else []
    def delete(self):
        if self.id is not None:
            DbTypeOfOperationEdition.delete_entry(self.id)  # Deletes the TypeOfOperation from the database
            TypeOfOperationObject.list_delete(self.id)  # Removes from the in-memory list
        else:
            print("Object doesn't exist")

    @classmethod
    def list_delete(cls, ID):
        cls.type_of_operation_list = list(filter(lambda x: x.id != ID, cls.type_of_operation_list))

    def __repr__(self):
        return f"({self.id}, {self.type_of_operation}, {self.type_of_mission}, {self.references}, {self.comments}, {self.phase_list})"

    @classmethod
    def create_type_of_operation_list(cls):
        db_type_of_operation_list = DbTypeOfOperationEdition.read_table()  # Reads all TypeOfOperation from the database
        cls.type_of_operation_list = []
        for operation in db_type_of_operation_list:
            cls.type_of_operation_list.append(
                TypeOfOperationObject(
                    operation.id,
                    operation.type_of_operation,
                    operation.type_of_mission,
                    operation.references,
                    operation.comments,
                    operation.phase_list
                )
            )

    @classmethod
    def edit_type_of_operation(cls, ID, TypeOfOperation, TypeOfMission, References, Comments, PhaseList):
        filtered_operation = [operation for operation in cls.type_of_operation_list if operation.id == ID]
        for operation in filtered_operation:
            operation.type_of_operation = TypeOfOperation
            operation.type_of_mission = TypeOfMission
            operation.references = References
            operation.comments = Comments
            operation.phase_list = PhaseList

        DbTypeOfOperationEdition.change_entry(ID, TypeOfOperation, TypeOfMission, References, Comments, PhaseList)

    @classmethod
    def new_entry(cls, TypeOfOperation, TypeOfMission, References, Comments, PhaseList):
        DbTypeOfOperationEdition.new_entry(TypeOfOperation, TypeOfMission, References, Comments, PhaseList)
        cls.create_type_of_operation_list()

    @classmethod
    def print_table(cls):
        table = PrettyTable(
            ["ID", "Type Of Operation", "Type Of Mission", "References", "Comments", "Phase List"],
            name="Type Of Operation Table"
        )

        for row in cls.type_of_operation_list:
            table.add_row(
                [
                    row.id,
                    row.type_of_operation,
                    row.type_of_mission,
                    row.references,
                    row.comments,
                    str(row.phase_list)
                ]
            )
        print(table)

    @classmethod
    def return_type_of_operation(cls, ID):
        try:
            for operation in cls.type_of_operation_list:
                if operation.id == ID:
                    return operation
        except:
            print(f"No Type Of Operation with ID {ID} found.")
    #@classmethod
    #def new_entry(cls, session, type_of_operation, type_of_mission, references="", comments="", phase_list="[]"):
        #"""Inserts a new entry into the database."""
        #new_operation = cls(
            #type_of_operation=type_of_operation,
            #type_of_mission=type_of_mission,
            #references="",
            #comments="",
            #phase_list=[]
        #)
        #session.add(new_operation)
        #session.commit()   
    #@staticmethod
    #def save_operation(operation_type, mission_type):
        """Saves an operation and mission type in the database."""
        #session = Database.get_session()
        #try:
            #new_operation = TypeOfOperationObject(
                #TypeOfOperation=operation_type,
                #TypeOfMission=mission_type,
                #References="",  # Empty if not provided
                #Comments="",    # Empty if not provided
                #PhaseList=[]    # Empty list if not applicable
            #)
            #session.add(new_operation)
            #session.commit()
        #except Exception as e:
            #session.rollback()
            #print(f"Error saving operation: {e}")
        #finally:
            #session.close()         
class SystemStateObject:
    # List to store SystemState objects
    system_state_list = []

    def __init__(self, ID, Name, ItemState, PersonState):
        self.id = ID
        self.name = Name
        self.item_state = ItemState
        self.person_state = PersonState

    def delete(self):
        if self.id is not None:
            DbSystemStateEdition.delete_entry(self.id)  # Deletes the SystemState from the database
            SystemStateObject.list_delete(self.id)  # Removes from the in-memory list
        else:
            print("Object doesn't exist")

    @classmethod
    def list_delete(cls, ID):
        cls.system_state_list = list(filter(lambda x: x.id != ID, cls.system_state_list))

    def __repr__(self):
        return f"({self.id}, {self.name}, {self.item_state}, {self.person_state})"

    @classmethod
    def create_system_state_list(cls):
        db_system_state_list = DbSystemStateEdition.read_table()  # Reads all SystemState entries from the database
        cls.system_state_list = []
        for system_state in db_system_state_list:
            cls.system_state_list.append(
                SystemStateObject(
                    system_state.id,
                    system_state.name,
                    system_state.item_state,
                    system_state.person_state
                )
            )

    @classmethod
    def edit_system_state(cls, ID, Name, ItemState, PersonState):
        filtered_system_state = [system_state for system_state in cls.system_state_list if system_state.id == ID]
        for system_state in filtered_system_state:
            system_state.name = Name
            system_state.item_state = ItemState
            system_state.person_state = PersonState

        DbSystemStateEdition.change_entry(ID, Name, ItemState, PersonState)

    @classmethod
    def new_entry(cls, Name, ItemState, PersonState):
        DbSystemStateEdition.new_entry(Name, ItemState, PersonState)
        cls.create_system_state_list()

    @classmethod
    def print_table(cls):
        table = PrettyTable(
            ["ID", "Name", "Item State", "Person State"],
            name="System State Table"
        )

        for row in cls.system_state_list:
            table.add_row(
                [
                    row.id,
                    row.name,
                    row.item_state,
                    row.person_state
                ]
            )
        print(table)

    @classmethod
    def return_system_state(cls, ID):
        try:
            for system_state in cls.system_state_list:
                if system_state.id == ID:
                    return system_state
        except:
            print(f"No System State with ID {ID} found.")


class PhaseObject:
    id = math.nan
    name = "Empty"
    input_state = "Empty"
    output_state = "Empty"
    order_number = -1
    type_of_operation_id = math.nan
    # List to store Phase objects
    phase_list = []

    def __init__(self, ID, Name, OrderNumber, InputState, OutputState, ProcedureList, TypeOfOperationID):
        self.id = ID
        self.name = Name
        self.order_number = int(OrderNumber)
        self.input_state = InputState
        self.output_state = OutputState
        self.procedure_list = ProcedureList
        self.type_of_operation_id = TypeOfOperationID

    def delete(self):
        if self.id is not None:
            DbPhaseEdition.delete_entry(self.id)  # Deletes the Phase from the database
            PhaseObject.list_delete(self.id)  # Removes from the in-memory list
            self.list_harmonisation_delete()
        else:
            print("Object doesn't exist")

    @classmethod
    def list_delete(cls, ID):
        cls.phase_list = list(filter(lambda x: x.id != ID, cls.phase_list))

    def __repr__(self):
        return f"({self.id}, {self.name}, {self.order_number}, {self.input_state}, {self.output_state}, {self.procedure_list}, {self.type_of_operation_id})"

    @classmethod
    def create_phase_list(cls):
        db_phase_list = DbPhaseEdition.read_table() 
        # Reads all phases from the database
        cls.phase_list = []
        for phase in db_phase_list:
            cls.phase_list.append(
                PhaseObject(
                    phase.id,
                    phase.name,
                    phase.order_number,
                    phase.input_state,
                    phase.output_state,
                    phase.procedure_list,
                    phase.type_of_operation_id
                )
            )
            print(f"Order in DB: {phase.order_number}") 
    @classmethod
    def edit_phase(cls, ID, Name, OrderNumber, InputState, OutputState, ProcedureList, TypeOfOperationID):
        filtered_phase = [phase for phase in cls.phase_list if phase.id == ID]
        for phase in filtered_phase:
            phase.name = Name
            phase.order_number = OrderNumber
            phase.input_state = InputState
            phase.output_state = OutputState
            phase.procedure_list = ProcedureList
            phase.type_of_operation_id = TypeOfOperationID

        DbPhaseEdition.change_entry(ID, Name, OrderNumber, InputState, OutputState, ProcedureList, TypeOfOperationID)

    #@classmethod
    #def new_entry(cls, Name, OrderNumber, InputState, OutputState, ProcedureList, TypeOfOperationID):
        #DbPhaseEdition.new_entry(Name, OrderNumber, InputState, OutputState, ProcedureList, TypeOfOperationID)
        #cls.create_phase_list()
    @classmethod
    def new_entry(cls, Name, OrderNumber, InputState, OutputState, ProcedureList, TypeOfOperationID):
        """
        Adds a new phase and then harmonizes the list of phases.
        """
        # Add the new phase to the database
        DbPhaseEdition.new_entry(Name, OrderNumber, InputState, OutputState, ProcedureList, TypeOfOperationID)

        # Refresh the in-memory list
        cls.create_phase_list()

        # Harmonize the order numbers for the phases
        cls.list_harmonisation_new_entry()
        #cls.list_harmonisation_delete()
    @classmethod
    def list_harmonisation_new_entry(cls):
        """
        Harmonizes order numbers when a new phase is added.
        Shifts the order numbers for existing phases that come after the new one.
        """
        new_phase = cls.phase_list[-1]  # Get the last added phase
        order_number = int(new_phase.order_number)
        type_of_operation_id = new_phase.type_of_operation_id

        for phase in cls.phase_list:
            phase_order_number = int(phase.order_number)

            if phase.type_of_operation_id == type_of_operation_id:
                if phase.order_number >= order_number and phase.id != new_phase.id:
                    phase.order_number = phase_order_number + 1
                    # Update the phase in the database
                    PhaseObject.edit_phase(
                        phase.id,
                        phase.name,
                        phase.order_number,
                        phase.input_state,
                        phase.output_state,
                        phase.procedure_list,
                        phase.type_of_operation_id
                    )
                    print(f"Order number harmonized: {phase.order_number} for Phase ID: {phase.id}")
    
    def list_harmonisation_delete(self):
    
        deleted_phase_order = self.order_number  # Order number of the deleted phase
        for phase in self.phase_list:
        # Adjust only phases in the same operation with a higher order number than the deleted one
            if (
                phase.type_of_operation_id == self.type_of_operation_id
                and int(phase.order_number) > deleted_phase_order
            ):
                phase.order_number -= 1  # Decrement the order number by 1
            # Update the phase in the database or list to reflect the new order
                PhaseObject.edit_phase(
                    phase.id,
                    phase.name,
                    phase.order_number,
                    phase.input_state,
                    phase.output_state,
                    phase.procedure_list,
                    phase.type_of_operation_id
                )

    @classmethod
    def print_table(cls):
        table = PrettyTable(
            ["ID", "Name", "Order Number", "Input State", "Output State", "Procedure List", "Type Of Operation ID"],
            name="Phase Table"
        )

        for row in cls.phase_list:
            table.add_row(
                [
                    row.id,
                    row.name,
                    row.order_number,
                    row.input_state,
                    row.output_state,
                    str(row.procedure_list),
                    row.type_of_operation_id
                ]
            )
        print(table)

    @classmethod
    def return_phase(cls, ID):
        try:
            for phase in cls.phase_list:
                if phase.id == ID:
                    return phase
        except:
            print(f"No Phase with ID {ID} found.")
            return None
    @classmethod
    def move_up(cls, phase_id):
        current_phase = cls.return_phase(phase_id)
        if not current_phase:
            return False

    # Prevent moving up if the phase is already at the top
        if current_phase.order_number == 1:
            print("Phase is already at the top. Cannot move up.")
            return False

        order_number = current_phase.order_number
        type_of_operation_id = current_phase.type_of_operation_id

    # Find the phase directly above
        upper_phase = [
            phase
            for phase in cls.phase_list
            if phase.order_number == (order_number - 1) and phase.type_of_operation_id == type_of_operation_id
        ]
    
        if not upper_phase:
            return False  # No phase to swap with

    # Swap order numbers
        upper_phase[0].order_number, current_phase.order_number = current_phase.order_number, upper_phase[0].order_number

    # Save changes to the database
        cls.edit_phase(
            current_phase.id, current_phase.name, current_phase.order_number,
            current_phase.input_state, current_phase.output_state,
            current_phase.procedure_list, current_phase.type_of_operation_id
        )
        cls.edit_phase(
            upper_phase[0].id, upper_phase[0].name, upper_phase[0].order_number,
            upper_phase[0].input_state, upper_phase[0].output_state,
            upper_phase[0].procedure_list, upper_phase[0].type_of_operation_id
        )

        return True


    @classmethod
    def move_down(cls, phase_id):
        current_phase = cls.return_phase(phase_id)
        if not current_phase:
            return False

        order_number = current_phase.order_number
        type_of_operation_id = current_phase.type_of_operation_id

    # Find the phase directly below
        lower_phase = [
            phase
            for phase in cls.phase_list
            if phase.order_number == (order_number + 1) and phase.type_of_operation_id == type_of_operation_id
        ]
    
        if not lower_phase:
            print("Phase is already at the bottom. Cannot move down.")
            return False  # No phase to swap with

    # Swap order numbers
        lower_phase[0].order_number, current_phase.order_number = current_phase.order_number, lower_phase[0].order_number

    # Save changes to the database
        cls.edit_phase(
            current_phase.id, current_phase.name, current_phase.order_number,
            current_phase.input_state, current_phase.output_state,
            current_phase.procedure_list, current_phase.type_of_operation_id
        )
        cls.edit_phase(
            lower_phase[0].id, lower_phase[0].name, lower_phase[0].order_number,
            lower_phase[0].input_state, lower_phase[0].output_state,
            lower_phase[0].procedure_list, lower_phase[0].type_of_operation_id
        )

        return True

class CheckpointObject:
    # List to store Checkpoint objects
    checkpoint_list = []

    def __init__(self, ID, Name, ItemState,  PersonState, ProcedureStepID):
        self.id = ID
        self.name = Name
        self.item_state = ItemState
        #self.set_req_input = SetReqInput
        self.person_state = PersonState
        self.procedure_step_id = ProcedureStepID

    def delete(self):
        if self.id is not None:
            DbCheckpointEdition.delete_entry(self.id)  # Deletes the Checkpoint from the database
            CheckpointObject.list_delete(self.id)  # Removes from the in-memory list
        else:
            print("Object doesn't exist")

    @classmethod
    def list_delete(cls, ID):
        cls.checkpoint_list = list(filter(lambda x: x.id != ID, cls.checkpoint_list))

    def __repr__(self):
        return f"({self.id}, {self.name}, {self.item_state}, {self.person_state}, {self.procedure_step_id})"

    @classmethod
    def create_checkpoint_list(cls):
        db_checkpoint_list = DbCheckpointEdition.read_table()  # Reads all Checkpoints from the database
        cls.checkpoint_list = []
        for checkpoint in db_checkpoint_list:
            cls.checkpoint_list.append(
                CheckpointObject(
                    checkpoint.id,
                    checkpoint.name,
                    checkpoint.item_state,
                    #checkpoint.set_req_input,
                    checkpoint.person_state,
                    checkpoint.procedure_step_id
                )
            )

    @classmethod
    def edit_checkpoint(cls, ID, Name, ItemState,  PersonState, ProcedureStepID):
        filtered_checkpoint = [checkpoint for checkpoint in cls.checkpoint_list if checkpoint.id == ID]
        for checkpoint in filtered_checkpoint:
            checkpoint.name = Name
            checkpoint.item_state = ItemState
            #checkpoint.set_req_input = SetReqInput
            checkpoint.person_state = PersonState
            checkpoint.procedure_step_id = ProcedureStepID

        DbCheckpointEdition.change_entry(ID, Name, ItemState, PersonState, ProcedureStepID)

    @classmethod
    def new_entry(cls, Name, ItemState, PersonState, ProcedureStepID):
        DbCheckpointEdition.new_entry(Name, ItemState,  PersonState, ProcedureStepID)
        cls.create_checkpoint_list()

    @classmethod
    def print_table(cls):
        table = PrettyTable(
            ["ID", "Name", "Item State",  "Person State", "Procedure Step ID"],
            name="Checkpoint Table"
        )

        for row in cls.checkpoint_list:
            table.add_row(
                [
                    row.id,
                    row.name,
                    row.item_state,
                    #row.set_req_input,
                    row.person_state,
                    row.procedure_step_id
                ]
            )
        print(table)

    @classmethod
    def return_checkpoint(cls, ID):
        try:
            for checkpoint in cls.checkpoint_list:
                if checkpoint.id == ID:
                    return checkpoint
        except:
            print(f"No Checkpoint with ID {ID} found.")
    #@classmethod
    #def clear_all_checkpoints(cls):
        """Deletes all checkpoints from the database and clears in-memory list."""
        # Clear in-memory list
        #cls.checkpoint_list.clear()
        #print("In-memory checkpoints cleared.")

        # Clear database entries
        #DbCheckpointEdition.delete_all_entries()

        #print("Checkpoint list after clearing:", cls.checkpoint_list)