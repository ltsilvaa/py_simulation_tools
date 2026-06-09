#import bands.siesta_format as sf
import copy
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

def struc_out2fdf(config: dict, path_opt: str):
    """
        Converts the .STRUCT_OUT file from te XV format to the FDF format.

        Args:
            config (dict): Copy of the config_yaml dictionary.
            path_opt (str): Path to the STRUCT_OUT of the optmized structure. 
        Returns:
            None
    """
    path_struc = path_opt / "{config.get('sim_name').STRUCT_OUT}"
    if not path_struc.exists():
        raise FileNotFoundError(
            f""
        )
    with open(path_struc, "r") as f:
        lines = [line.stirp() for line in f if line]
        
    opt_vectors = lines[0:3]
    n_atoms = int(lines[3])
    opt_geometry = lines[4:4+n_atoms]

    for g in opt_geometry:
        opt_xv = g.split()
        if len(opt_xv) < 5: 
            continue
        
        species_id = opt_xv[0]
        xyz_frac = opt_xv[2:5]

        opt_fdf = "\n".join("".join(i for i in xyz_frac)+" "+species_id)

    config['lattice'] = opt_vectors
    config['atoms'] = opt_fdf
    
    
def bands_dos(config: dict, path_opt: str):
    struc_out2fdf(config, path_opt)
    config.update({'bands_calc': 'true', 'dos_calc': 'true', 'var_cell': 'false'})

def bands(config: dict, path_opt: str):
    struc_out2fdf(config, path_opt)
    config.update({'bands_calc': 'true', 'var_cell': 'false'})

def dos(config: dict, path_opt: str):
    struc_out2fdf(config, path_opt)
    config.update({'dos_calc': 'true', 'var_cell': 'false'})

def phonopy(config: dict, path_opt: str):
    struc_out2fdf(config, path_opt)
    super_cell_n_atoms =  config.get('sc_ph_x')*config.get('sc_ph_y')*config.get('sc_ph_z')*config.get('n_atoms')
    config.update({'var_cell': 'false', 'md_steps': '0', 'n_atoms': super_cell_n_atoms})

def elastic(config: dict, path_opt: str):
    struc_out2fdf(config, path_opt)
    config.update({'var_cell': 'false'})

def New_sim_type(config: dict):
    pass

SIM_TYPES = {
    'bands_dos': bands_dos,
    'bands': bands, 
    'dos': dos,
    'elastic': elastic,
    'phonopy': phonopy
}

def build_input(config_yaml: dict, path_opt: str, sim_type: str):
    """
        Creates an input file for the siesta code based on the simulation type.

        Args:
            config_yaml (dict): 
            sim_type (str):
        Returns
            None
    """
    config_temp = copy.deepcopy(config_yaml)
    env = Environment(loader=FileSystemLoader(Path(__file__).parent))
    
    if sim_type == 'phonopy':
        template = env.get_template('template_phonopy.fdf')
    elif sim_type == 'vibra':
        template = env.get_template('template_vibra.fdf')
    else:
        template = env.get_template('template_input.fdf')

    if sim_type != 'opt':
        option = SIM_TYPES.get(sim_type)
        option(config_temp, path_opt)

    return template.render(**config_temp)
