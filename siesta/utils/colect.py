import re

def colect_optimized_vectors(path_output: str):
    """
        Args:

        Returns:
            optimized_vectors (string): 
    """
    optimized_vectors_pattern = r"outcell: Unit.*?\n(.*?)\noutcell: Cell vector"
    with open(path_output, "r", errors="ignore") as output_file:
        text = output_file.read()
        optimized_vectors = re.findall(optimized_vectors_pattern, text, re.DOTALL)

    return optimized_vectors.group(1)

def colect_optmized_geometry(path_output: str):
    """
        Args:
            
        Returns:
            optimized_geometry (string): Optimized geometry colectred from the output file 
    """
    optimized_geometry_pattern =  r'outcoor: Relaxed.*?\n(.*?)\noutcell: Unit'
    with open(path_output, "r", errors="ignore") as output_file:
        text = output_file.read()
        optimized_geometry = re.search(optimized_geometry_pattern, text, re.DOTALL)

    return optimized_geometry.group(1)

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

def colect_optimized_volume(path_output: str):
    """
    
        Args:
            path_output (string):
        Return:
            final_volume (float):
    """
    with open(path_output, "r", errors="ignore") as output_file:
        lines = output_file.readlines()
        for line in reversed(lines):
            if "outcell: Cell volume" in line:
                final_volume = float(line.split()[-1].strip())
                break

    return final_volume