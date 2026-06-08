import os
import deformation as df
import build_input as bi
from pathlib import Path
from typing import Callable, Any
from ase.geometry import Cell

def deformations_per_symmetry(R0, config_yaml: dict):
    """
        Verify the symmetry of the structure and returns the correct list of deformations.

        Args:
            R0 (list): Lattice vectors of the optmized structure.
            config_yaml (dict): Configuration file of the simulation.
        Returns:
            List with the necessary deformations fo the structure.
    """
    if config_yaml.get('dim') == "1":
        R0[2,2] = "0.00"
        R0[1,1] = "0.00"
    elif config_yaml.get('dim') == "2":
        R0[2,2] = "0.00"

    cell = Cell(R0)
    cell_type = cell.get_bravais_lattice().name

    if config_yaml.get('bm_only', False):
        return [df.def_isotropic]

    if R0[2,2] != "0.00":
        if cell_type == "CUB":
            return [df.def_11, df.def_12,df.def_44]
        elif cell_type in ["TET","BCT"]:
            return [df.def_11, df.def_12, df.def_13, df.def_16, df.def_33, df.def_44, df.def_66]
        elif cell_type == "RHL":
            return [df.def_11, df.def_12, df.def_13, df.def_14, df.def_15, df.def_33, df.def_44, df.def_66]
        elif cell_type in ["ORC", "ORCF", "ORCC"]:
            return [df.def_11, df.def_12, df.def_13, df.def_22, df.def_23, df.def_33, df.def_44, df.def_55, df.def_66]
        elif cell_type == "HEX":
            return [df.def_11, df.def_12, df.def_13, df.def_33, df.def_44, df.def_66]
        elif cell_type in ["MCL", "MCLC"]:
            return [df.def_11, df.def_12, df.def_13, df.def_15, df.def_22, df.def_23, df.def_25, df.def_33, df.def_35, df.def_44, df.def_46, df.def_55, df.def_66]
        elif cell_type == "TRI":
            return [df.def_11, df.def_12, df.def_13, df.def_14, df.def_15, df.def_16, df.def_22, df.def_23, df.def_24, df.def_25, df.def_26, df.def_33, df.def_34, df.def_35, df.def_36, df.def_44, df.def_45, df.def_46, df.def_55, df.def_56, df.def_66]
    else:
        if cell_type == "SQR":
            return [df.def_11, df.def_12, df.def_66]
        elif cell_type == "HEX2D":
            return [df.def_11, df.def_12]
        elif cell_type in ["RECT","CRECT"]:
            return [df.def_11, df.def_12, df.def_22, df.def_66]
        elif cell_type == "OBL":
            return [df.def_11, df.def_12, df.def_16, df.def_26, df.def_22, df.def_66]

def run_deformations(working_dir: str, config_yaml: dict, run: Callable[..., Any], utils: Callable[..., Any], R0):
    """
        Runs the calculations of the deformed structure with the desired simulation code to compute
        the elastic constants through the energy-strain approach.

        Args:
            working_dir (str): Path to the simulation directory.
            config_yaml (dict): Configuration file of the simulation.
            run (Callable): Correct funtion to run the simulaiton.
            R0 (list): Lattice vectors of the optmized structure.
        Returns:
            List with the necessary deformations fo the structure.
    """
    strain_energy = []
    deformations = deformations_per_symmetry(R0, config_yaml)
    max_deformation = float(config_yaml.get('max_def',0.01))
    deformations_number = int(config_yaml.get('num_def',7))

    eps = [(-max_deformation + (max_deformation/(deformations_number/2))*i) for i in range(deformations_number)]
    for deform in deformations:
        s_e = []
        deform_path = working_dir / str(deform.__name__)
        for j in eps:
            path_eps = deform_path / f"{eps:12.3}"
            path_eps.mkdir(parents=True ,exist_ok=True)
            R = df.deform(R0, j)
            bi.config_yaml('program')(path_eps, R0, config_yaml)
            path_output = run(path_eps)
            total_energy = utils.colect_optimized_energy(path_output)
            s_e.append([str(j), total_energy])

            if j == 0.00:
                e0 = total_energy #unstrained energy
            
        with open(os.path.join(path,f"strain_energy_{deform}.dat"), "w") as outfile:
            for line in s_e:
                outfile.write(f"{line[0]:12.6f} {line[1]-e0:12.6f}\n")

        strain_energy.append(s_e)

    return strain_energy    

            


