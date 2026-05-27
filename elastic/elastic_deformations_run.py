import os
import deformation as df
import copy_imput_files
from siesta.utils import 
from ase.geometry import Cell

calculators = {
    "siesta": siesta_run,
    "quantumespresso": qe_run,
    "cp2k": cp2k_run,
    "onetep": onetep_run,
    "castep": castep_run,
    "vasp": vasp_run,
}

def siesta_run(input_path):
    import siesta.calculators.siesta as c
    return c(input_path,)

def qe_run():
    import qe.calculators.pw as c
    return c()

def cp2k_run():
    import cp2k.calculators. as c
    return c()

def onetep_run():
    import onetep.calculators.onetep as c
    return c()

def vasp_run():
    import vasp.calculators. as c
    return c()

def castep_run():
    import castep.calculators. as c
    return c()

def deformations_per_symmetry(R0):
    cell = Cell(R0)
    cell_type = cell.get_bravais_lattice().name
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

def run_deformations(R0, max_deformation: float, deformations_number: int, run_type: str, calculation_path: str, dimension: str):
    """
    
    """
    deformations_energies = []
    deformations = deformations_per_symmetry(R0)

    eps = [(-max_deformation + (max_deformation/(deformations_number/2))*i) for i in range(deformations_number)]
    for deform in deformations:
        for j in eps:
            strain_energy = []
            os.makedirs(os.path.join(calculation_path,str(deform),f"{eps:1}"),exist_ok=True)
            R = deform(R0, j)

            ##find replace R na variavel de imput
            #copy_input_files(path_deformation)
            path_output = calculators[run_type](calculation_path)
            total_energy = find_energy()
            strain_energy.append([j,total_energy])
            
        with open(os.path.join(calculation_path,f"strain_energy_{deform}.dat"), "w") as outfile:
            for line in strain_energy:
                outfile.write(f"{line[0]:12.6f} {line[1]:12.6f}\n")

        deformations_energies.append(strain_energy)

    return deformations_energies    

            


