from pathlib import Path
from typing import Callable, Any

def input_extension(config: dict):
    """
        Returns the correct exetension for the input file.

        Args: 
            config (dict): Configuration file of the simulation.
        Returns:
            Input file name with the correct extension.
    """        
    SIM_INPUT_NAME = {
        'siesta': 'input.fdf',
        'qe': 'input.in',
        'castep': '',
        'onetep': '',
        'cp2k': '',
        'dftb': ''
    }
    return SIM_INPUT_NAME.get(config.get('sim_code'))     

def opt(work_dir: str, config_yaml, run: Callable[..., Any], build_input: Callable[..., Any]):
    """
        Build the input and runs a simple geometry optmization simulation.

        Args: 
            work_dir (str): Path to the simulation directory.
            config_yaml (dict): Configuration file of the simulation.
            run (Callable): Correct funtion to run the simulaiton.
            build_input (Callable): Correct funtion to build the simulation input.
        Returns:
            Simulation output path.
    """

    path_opt = work_dir / 'opt'
    path_opt.mkdir(parents = True, exist_ok=True)
  
    path_inp = path_opt / input_extension(config_yaml) 
    with open(path_inp, "w") as f:
        f.write(build_input(config_yaml, work_dir, sim_type = 'opt'))

    path_output = run(path_opt)

    return path_output
