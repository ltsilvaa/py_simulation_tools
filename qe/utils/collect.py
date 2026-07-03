import re

def collect_optimized_energy(path_output: str):
    """
        collects the total energy in eV from the QuantumEspresso siesta output file.

        Args:
            path_output (str): Path to the output file.
        Returns:
            Total energy of the system after the calculation.
    """
    with open(path_output, "r", errors="ignore") as output_file:
        lines = output_file.readlines()
        for line in reversed(lines):
            if "!" in line:
                final_energy = float(line.split()[4].strip())
                final_energy_eV = final_energy*13.6057039763
                break

    return final_energy_eV 

def collect_optimized_volume(path_output: str):
    """
        collects the volume in Ang**3 from the siesta output file.
    
        Args:
            path_output (str): Path to the output file.
        Returns:
            Volume of the system cell after the calculation.
    """
    with open(path_output, "r", errors="ignore") as output_file:
        lines = output_file.readlines()
        for line in reversed(lines):
            if "new unit-cell volume" in line:
                final_volume = float(line.split()[7].strip())
                break

    return final_volume

def collect_optimized_vectors(path_output: str):
    """
        Args:

        Returns:
            optimized_vectors (string): 
    """
    optimized_vectors_pattern = r"CELL_PARAMETERS\s*\([a-zA-Z]+\).*?\n(.*?)(?=\n\s*\n)"
    with open(path_output, "r", errors="ignore") as output_file:
        text = output_file.read()
        optimized_vectors = re.search(optimized_vectors_pattern, text, re.DOTALL)

    return optimized_vectors.group(1)

def collect_optmized_geometry(path_output: str):
    """
        Args:
            
        Returns:
            optimized_geometry (string): Optimized geometry collectred from the output file 
    """
    optimized_geometry_pattern =  r"ATOMIC_POSITIONS\s*\([a-zA-Z]+\).*?\n(.*?)(?=\n\s*\n|\n\s*End)"
    with open(path_output, "r", errors="ignore") as output_file:
        text = output_file.read()
        optimized_geometry = re.search(optimized_geometry_pattern, text, re.DOTALL)

    return optimized_geometry.group(1)