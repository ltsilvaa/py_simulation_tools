import os
import json
import yaml
import subprocess
from core.global_config.config_yaml import config

def yaml_read():
    """
        Loads the config.yaml file.

        Args: None.
        Retruns: None.
    """
    yaml_path = os.path.join(os.getcwd(),"config.yaml")
    if os.path.exists(yaml_path):
        with open(yaml_path, "r") as f:
            config = yaml.safe_load(f)
        return config
    else:
        raise FileNotFoundError(
        f"\n config.yaml file not found in {os.getcwd()}"
    )

def load_cluster_config():
    """
        Load the .json file with the program binaries for the current cluster.
    
        Args: None
        Returns: None
    """
    current_dir = os.path.dirname(__file__) 
    config_file_path = os.paht.join(current_dir,"config.json")

    if os.path.exists(config_file_path):
        with open(config_file_path, "w") as config_file:
            return json.load(config_file)
    else: 
        raise FileNotFoundError(
            f"\n Configuration file not found in {config_file_path}\n"
            f"Please, edit the file '{os.path.join(current_dir,"config.default.json")}'"
            f"with your cluster directories and copy it to '{config_file_path}'"
        )

#def binary_chose(simulation_code: str, run_type: str):
#    """
#        Select binary for chosed simulation code.
#
#        Args:
#            simulation_code (string):
#            run_type (string):
#        Returns: 
#            config_file[simulation_code.upper()][run_type.lower()] (string): 
#        
#        Raises:
#            ValueError: If the simulation code or the run option aren't found in the config.json.
#    """
#    config_file = load_cluster_config()
#
#    if not config_file.get(simulation_code.upper()):
#        avaliable = list(config_file.keys())
#        raise ValueError(
#            f"Simulation code {simulation_code.upper()} not found in config.json\n"
#            f"Avaliable options {avaliable}\n"
#        )
#    
#    if not config_file.get(simulation_code.upper()).get(run_type.lower()):
#        avaliable = list(config_file[simulation_code.upper()].keys())
#        raise ValueError(
#            f"Run option {run_type.lower()} not found in config.json\n"
#            f"Avaliable options {avaliable}\n"
#        )
#    
#    return config_file[simulation_code.upper()][run_type.lower()]

def cmd_build():
    """
        Build the cmd list for the simulation.

        Args:  
            binary(str): Simulation program path.
        Returns:
            CMD list for subprocessrun.
    """
    config = yaml_read()
    np = config.get('nprocs','1')
    program = config.get('program')
    
    return ["nohup", "mpirun", np, program]

def execute_simulation_code(working_dir: str):
    """
    Execute the simulation program binary chosed through the subprocess library.

    Args:
        binary_cmd (list:string): list with the binary files for the simulation programs.
        working_dir (string) = Current work directory to run the simulation.
        input_name (string) = Name of the input file for the simulation code.
    Retruns:

    """
    cmd = cmd_build()
    config = yaml_read()

    input_name = config.get('sim_name', 'inp')

    path_input = os.path.join(working_dir,input_name)
    path_output = os.path.join(working_dir,"log.out")

    with open(path_input, "r") as file_output, open(path_output, "w") as file_input:
        subprocess.run(
            cmd,
            cwd = working_dir,
            stdin = file_input,
            stdout = file_output,
            stderr=subprocess.STDOUT
        )
    return path_output