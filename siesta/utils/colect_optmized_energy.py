def colect_optimized_energy(path_output: str):
    """
    
        Args:
            path_output (string):
        Return:
            final_energy (float):
    """
    with open(path_output, "r", errors="ignore") as output_file:
        lines = output_file.readlines()
        for line in reversed(lines):
            if "siesta:         Total =" in line:
                final_energy = float(line.split("Total =")[1].strip())
                break

    return final_energy 