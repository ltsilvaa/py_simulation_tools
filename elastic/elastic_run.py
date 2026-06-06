import os
from core.global_config.config_yaml import config
from core.run.run_sim import execute_simulation_code as run
import deformation as df
from ase.geometry import Cell

def deformations_per_symmetry(R0, dim: str):
    """

    """
    if dim == "1":
        R0[2,2] = "0.00"
        R0[1,1] = "0.00"
    elif dim == "2":
        R0[2,2] = "0.00"

    cell = Cell(R0)
    cell_type = cell.get_bravais_lattice().name

    if config.get('bm_only', False):
        return [df.def_isotropic]

    if R0[2,2] != "0.00":
        if cell_type == "CUB":
            return [df.def_11, df.def_,df.def_df.def_]
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

def run_deformations(R0, working_dir: str, dimension: str):
    """
    
    """
    s_e = []
    deformations = deformations_per_symmetry(R0, dim=dimension)
    max_deformation = float(config.get('max_def',0.01))
    deformations_number = int(config.get('num_def',7))

    eps = [(-max_deformation + (max_deformation/(deformations_number/2))*i) for i in range(deformations_number)]
    for deform in deformations:
        for j in eps:
            path = os.path.join(working_dir,str(deform),f"{eps:1}")
            os.makedirs(path,exist_ok=True)
            R = deform(R0, j)
            build_deformation_input(R0, run)
            #copy pseudo if is siesta
            path_output = run(path)
            total_energy = find_energy()
            s_e.append([str(j), total_energy])

            if j == 0.00:
                e0 = total_energy #unstrained energy
            
        with open(os.path.join(run_path,f"strain_energy_{deform}.dat"), "w") as outfile:
            for line in s_e:
                outfile.write(f"{line[0]:12.6f} {line[1]-e0:12.6f}\n")

        strain_energy.append(s_e)

    return strain_energy    

            


