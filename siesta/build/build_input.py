#import bands.siesta_format as sf
import copy
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

def bands_dos(config: dict):
    config.update({'bands_calc': 'true', 'dos_calc': 'true', 'var_cell': 'false'})

def bands(config: dict):
    config.update({'bands_calc': 'true', 'var_cell': 'false'})

def dos(config: dict):
    config.update({'dos_calc': 'true', 'var_cell': 'false'})

def phonopy(config: dict):
    super_cell_natoms =  config.get('sc_ph_x')*config.get('sc_ph_y')*config.get('sc_ph_z')*config.get('n_atoms')
    config.update({'var_cell': 'false', 'md_steps': '0', 'n_atoms': super_cell_natoms})

def build_input(config_yaml: dict, sim_type: str):
    """
    
    """
    config_temp = copy.deepcopy(config_yaml)
    env = Environment(loader=FileSystemLoader(Path(__file__).parent))
    template = env.get_template('template_input.fdf')

    return template.render(**config_temp)
