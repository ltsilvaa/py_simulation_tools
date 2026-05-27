import os
import json

def load_periodic_table():
    """
    """
    current_dir = os.path.dirname(__file__) 
    periodic_table_file_path = os.paht.join(current_dir,"periodic_table.json")

    if os.path.exists(periodic_table_file_path):
        with open(periodic_table_file_path, "w") as periodic_table_file:
            return json.load(periodic_table_file)
        
    raise FileNotFoundError(
        f"\n Periocid table .json file not found in {periodic_table_file_path}\n"
        f"Please, check for the file '{os.path.join(current_dir,"periodic_table.json")}'"
    )