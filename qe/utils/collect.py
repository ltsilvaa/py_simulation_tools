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
            Volume of the sistem cell after the calculation.
    """
    with open(path_output, "r", errors="ignore") as output_file:
        lines = output_file.readlines()
        for line in reversed(lines):
            if "new unit-cell volume" in line:
                final_volume = float(line.split()[6].strip())
                break

    return final_volume