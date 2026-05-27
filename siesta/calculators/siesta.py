import os
import subprocess
from core.binary_chose import binary_chose

def execute_siesta(processors_number: int, working_dir: str, input_name: str, binary: str):
    """
        Contruct the terminal comand to run the SIESTA code.

        Args:
            processors_number (integer): Number of processors to run te desired code.
            working_dir (string): Current work directory to run the simulation.
            input_name (string): Name of the input file for the simulation code.
            binary (list): comand line to execute the program.
        Returns: 
            path_output (string): path to the output file to further analisys.
    """
    host_file = os.path.join(working_dir,"host.txt")
    with open(host_file, "w") as f:
            f.write(f"localhost slots= {processors_number}")

    binary_cmd = binary_chose("siesta","siesta")

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
