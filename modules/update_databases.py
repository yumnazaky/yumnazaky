import sys, os

current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# get the directory of GUI (which is in a sibling folder)
src_path = os.path.join(current_dir, "src")
# add GUI path to the system path
modules_path = os.path.join(current_dir, "modules")
sys.path.append(src_path)
sys.path.append(modules_path)
# print("Path Modules: ", modules_path))





from define_object_classes import (
    ItemObject,
    PhaseObject,
    ProcedureObject,
    ProcedureStepObject,
    TypeOfOperationObject,
    SystemStateObject,
    CheckpointObject,
)


def update_lists():
    # Updating all objects' lists
    
    #ItemObject.create_item_list()
    if not ItemObject.item_list:  # Initialize only if item_list is empty
        ItemObject.create_item_list()
    else:
        print("ItemObject.item_list already initialized, skipping re-initialization.")
    item_list = []
    item_list = ItemObject.item_list
    ProcedureObject.create_procedure_list()
    procedure_list=[]
    procedure_list = ProcedureObject.procedure_list
    ProcedureStepObject.create_procedure_step_list()
    TypeOfOperationObject.create_type_of_operation_list()
    SystemStateObject.create_system_state_list()
    PhaseObject.create_phase_list()
    CheckpointObject.create_checkpoint_list()
  
   
    
    procedure_step_list =[]
    type_of_operation_list =[]
    system_state_list = []
    phase_list = []
    checkpoint_list = []
    
    
    
    procedure_step_list = ProcedureStepObject.procedure_step_list
    type_of_operation_list = TypeOfOperationObject.type_of_operation_list
    system_state_list = SystemStateObject.system_state_list
    phase_list = PhaseObject.phase_list
    checkpoint_list = CheckpointObject.checkpoint_list

    #initial_item_cache = [(item.id, item.provides, item.requires, item.turns_off) for item in ItemObject.item_list]
    #print("Temporary cache before calling update_lists():", initial_item_cache)
    return (
        item_list,
        procedure_list,
        procedure_step_list,
        type_of_operation_list,
        system_state_list,
        phase_list,
        checkpoint_list,
    )
    #updated_item_cache = [(item.id, item.provides, item.requires, item.turns_off) for item in ItemObject.item_list]
    
    #print("Updated cache after calling update_lists():", updated_item_cache)


# Call this before generating warnings for a new step.

def create_requirements_list( type_of_operation_id, selected_procedure_id):
    #ItemObject.item_list.clear()
    #temp_cache = [(item.id, item.provides, item.requires, item.turns_off) for item in ItemObject.item_list]
    #print("Temporary cache before calling update_lists():", temp_cache)
    # Get the updated lists
    (
        item_list,
        procedure_list,
        procedure_step_list,
        type_of_operation_list,
        system_state_list,
        phase_list,
        checkpoint_list,
    ) = update_lists()
    print("Updated ItemObject.item_list before processing in create_requirements_list:")
    for item in item_list:
        print(f"Item ID: {item.id}, Name: {item.name}, Provides: {item.provides}, Requires: {item.requires}, Turns Off: {item.turns_off}")
    provided_list = []
    warning_list = []
    #required_list = []

    class WarningObject:
        def __init__(self, PhaseName, PhaseOrderNo, ProcedureName,  StepOrderNo, ProcedureStepID, OperationID, Provides, Requires, TurnsOff):
            self.phase_name = PhaseName
            self.phase_order_number = PhaseOrderNo
            self.procedure_name = ProcedureName
            self.procedure_step_id = ProcedureStepID
            self.step_order_number = StepOrderNo
            self.type_of_operation_id = OperationID
            self.provides = Provides
            self.requires = Requires
            self.turns_off = TurnsOff

        def __repr__(self):
            return (f"WarningObject(PhaseName: {self.phase_name}, PhaseOrderNo: {self.phase_order_number}, "
                    f"ProcedureName: {self.procedure_name}, StepOrderNo: {self.step_order_number}, "
                    f"OperationID: {self.type_of_operation_id}, Provides: {self.provides}, "
                    f"Requires: {self.requires}, ProcedureStepID:{self.procedure_step_id},TurnsOff: {self.turns_off})\n")


    #filtered_procedure_list = [p for p in procedure_list if p.phase_id == type_of_operation_id]

# Sort procedure list by order_number
    #sorted_procedure_list = sorted(filtered_procedure_list, key=lambda x: x.order_number)
    filtered_procedure_list = [
        p for p in procedure_list if p.id == selected_procedure_id and p.phase_id in [
            phase.id for phase in phase_list if phase.type_of_operation_id == type_of_operation_id
        ]
    ]

    # Sort filtered procedure list by order_number
    sorted_procedure_list = sorted(
        filtered_procedure_list,
        key=lambda p: next((phase.order_number for phase in PhaseObject.phase_list if phase.id == p.phase_id), 0)
    )
    print("Filtered Procedures:", filtered_procedure_list)
    print("Sorted Procedures:", sorted_procedure_list)
    #sorted_procedure_list = sorted(filtered_procedure_list, key=lambda x: x.order_number)
    #sorted_procedure_list = sorted(filtered_procedure_list, key=lambda x: x.sequence)

    for procedure in sorted_procedure_list:
        phase = next((ph for ph in phase_list if ph.id == procedure.phase_id), None)
        
        # Check if phase exists
        if not phase:
            print(f"Skipping procedure '{procedure.name}' due to missing phase data.")
            continue  # Skip this iteration if phase is not found

        print(f"Processing phase '{phase.name}' for procedure '{procedure.name}'")
    # Get procedure steps associated with this procedure
        filtered_procedure_steps = [step for step in procedure_step_list if step.procedure_id == procedure.id]
       
        sorted_procedure_steps = sorted(filtered_procedure_steps, key=lambda x: x.order_step)
       
        for procedure_step in sorted_procedure_steps:
            
            
            step = ProcedureStepObject.return_procedure_step(procedure_step.id)
            item = ItemObject.return_item(step.item_id)
            if not step or not item:
                print(f"Skipping step ID {procedure_step.id} due to missing data.")
                continue    

            #if step is None:

               # print(f"Skipping missing step ID {procedure_step.id}")
               # continue  # Skip if step is not found
            #print(f"Procedure Step ID {procedure_step.id} has item_id {procedure_step.item_id}")
            
            #print("Current items in ItemObject.item_list:", [(item.id, item.name) for item in ItemObject.item_list])
            #if item is None:
               # print(f"Skipping missing item for step ID {procedure_step.id}")
                #continue  # Skip if item is not found
            provides = item.provides if isinstance(item.provides, list) else []
            requires = item.requires if isinstance(item.requires, list) else []
            turns_off = item.turns_off if isinstance(item.turns_off, list) else []
            missing_systems = [req for req in requires if req not in provides]

            #provided_list_copy = provided_list.copy()
            print(f"Retrieved for Step {procedure_step.id} - Provides: {provides}, Requires: {requires}, TurnsOff: {turns_off}")
            print(f"Creating warning for step ID {procedure_step.id}")

            print(f" - Provides: {provides}")
            print(f" - Requires: {requires}")
            # Track provided items
            provided_list_copy = provided_list.copy()
            #print(f"Provided List Before Turns Off: {provided_list_copy}")
            for provide in provides:
                if provide not in provided_list:
                    provided_list.append(provide)
                if provide not in provided_list_copy:
                    provided_list_copy.append(provide)

            # Remove any items that are turned off
            for t_off in turns_off:
                if t_off in provided_list_copy:
                    provided_list_copy.remove(t_off)
            #for require in requires:
                #if require not in required_list:
                    #required_list.append(require)        
            #missing_items = [require for require in required_list if require not in provided_list_copy]

            # Create warning object
            if missing_systems:
                warning = WarningObject(
                    PhaseName=phase.name,               # PhaseName
                    PhaseOrderNo=phase.order_number,    # PhaseOrderNo
                    ProcedureName=procedure.name,
                    StepOrderNo=procedure_step.order_step,  # StepOrderNo
                    OperationID=phase.type_of_operation_id,  # OperationID
                    Provides=item.provides,
                    ProcedureStepID=procedure_step.id,             # Provides
                    Requires= item.requires,                       # Requires
                    TurnsOff=item.turns_off             #TurnsOff
                )

                warning_list.append(warning)
            else:
                print(f"No missing systems for step ID {procedure_step.id}. Skipping warning creation.")
    
    print("Final Warning List:", warning_list)
    return warning_list
       
