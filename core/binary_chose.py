from load_cluster_config import load_cluster_config

def binary_chose(simulation_code: str, run_type: str):
    """
        

        Args:
            simulation_code (string):
            run_type (string):
        Returns: 
            config_file[simulation_code.upper()][run_type.lower()] (string): 
        
        Raises:
            ValueError: If the simulation code or the run option aren't found in the config.json.
    """
    config_file = load_cluster_config()

    if not config_file.get(simulation_code.upper()):
        avaliable = list(config_file.keys())
        raise ValueError(
            f"Simulation code {simulation_code.upper()} not found in config.json\n"
            f"Avaliable options {avaliable}\n"
        )
    
    if not config_file.get(simulation_code.upper()).get(run_type.lower()):
        avaliable = list(config_file[simulation_code.upper()].keys())
        raise ValueError(
            f"Run option {run_type.lower()} not found in config.json\n"
            f"Avaliable options {avaliable}\n"
        )
    
    return config_file[simulation_code.upper()][run_type.lower()]