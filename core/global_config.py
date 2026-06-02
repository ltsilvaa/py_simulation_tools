from dataclasses import dataclass

@dataclass
class Global_Config:
    """
        Global variables for general use in the lib.
    """
    nprocs: int = 1
    pseudo_path: str = "/home/ltsilva/Pseudopotentials/"
    input_file: str = "inp"
    output_file: str = "log.out"
    ...

config = Global_Config()

def Init_Global_Config(input_yaml: dict):
    """
        Configure the global variables for the program.
    """
    global config

    config.nprocs = input_yaml.get('nprocs', 1)
    config.pseudo_path = input_yaml.get('pseudo_path', '/home/ltsilva/Pseudopotentials/')
    config.input_file = input_yaml.get('input_files', 'inp')
    config.output_file = input_yaml.get('output_files', 'log.out')