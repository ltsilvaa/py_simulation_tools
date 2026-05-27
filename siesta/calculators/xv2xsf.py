import subprocess
from core.binary_chose import binary_chose

def execute_xv2xsf(working_dir: str, input_name: str, binary: str):
    """
        Construct and run the terminal comand to the xv2xsf SIESTA utility.

        Args:
            working_dir (string): Current work directory to run the simulation.
            input_name (string): Name of the input file for the simulation code.
            binary (list): comand line to execute the program.
        Returns: 
            None
    """

    binary_cmd = [binary_chose("siesta","xv2xsf")]

    subprocess.run(
        binary_cmd,
        cwd = working_dir,
        input = input_name,
        text = True,
        stderr=subprocess.STDOUT
        )


