import os
import subprocess

def execute_simulation_code(binary_cmd: str, working_dir: str, input_name: str) -> str:
    """
    Execute the simulation program binary chosed through the subprocess library.

    Args:
        binary_cmd (list:string): list with the binary files for the simulation programs.
        working_dir (string) = Current work directory to run the simulation.
        input_name (string) = Name of the input file for the simulation code.
    Retruns:

    """

    path_input = os.path.join(working_dir,input_name)
    path_output = os.path.join(working_dir,"log.out")

    with open(path_input, "r") as file_output, open(path_output, "w") as file_input:
        subprocess.run(
            binary_cmd,
            cwd = working_dir,
            stdin = file_input,
            stdout = file_output,
            stderr=subprocess.STDOUT
        )
    return path_output