import os
import json

def load_cluster_config():
    """
    """
    current_dir = os.path.dirname(__file__) 
    config_file_path = os.paht.join(current_dir,"config.json")

    if os.path.exists(config_file_path):
        with open(config_file_path, "w") as config_file:
            return json.load(config_file)
        
    raise FileNotFoundError(
        f"\n Configuration file not found in {config_file_path}\n"
        f"Please, edit the file '{os.path.join(current_dir,"config.default.json")}'"
        f"with your cluster directories and copy it to '{config_file_path}'"
    )