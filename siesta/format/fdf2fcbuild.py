from utils.colect import colect_optmized_geometry, colect_optmized_vectors
from utils.replace import replace_input_geometry, replace_input_vectors
from utils.change import chage_input_number_of_atoms
from core.load_periodic_table import load_periodic_table

def fdf2fcbuild(working_dir: str, input_name: str, path_output: str): 
    """
    
    """
    element = load_periodic_table()
    optimized_geometry = colect_optmized_geometry(path_output)
    optimized_vectors = colect_optmized_vectors(path_output)

    n = 0

    for line in optimized_geometry.splitlines():
        geometry_line = line.strip().split()
        geo_fc += f'{geometry_line[1]} {geometry_line[2]} {geometry_line[3]} {geometry_line[4]} {element[geometry_line[6]]["atomic_mass"]} \n'
        n += 1

    #tenho que fazer uma forma de copiar o input generico do fcbuild para a pasta de execução do codigo

    chage_input_number_of_atoms(working_dir, input_name, n)
    replace_input_geometry(working_dir, input_name, optimized_geometry)
    replace_input_vectors(working_dir, input_name, optimized_vectors)