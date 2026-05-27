import re

def colect_optmized_geometry(path_output: str):
    """
    
    """
    optimized_geometry_pattern =  r'outcoor: Relaxed.*?\n(.*?)\noutcell: Unit'
    with open(path_output, "r", errors="ignore") as output_file:
        text = output_file.read()
        optimized_geometry = re.search(optimized_geometry_pattern, text, re.DOTALL)

    return optimized_geometry.group(1)