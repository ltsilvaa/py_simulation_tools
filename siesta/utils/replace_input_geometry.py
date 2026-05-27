import os
import re

def replace_input_geometry(work_directory: str, input_name: str, new_geometry: str):
    """
    
    """
    path_input = os.path.join(work_directory,input_name)
    input_geometry_pattern = r"%block AtomicCoordinatesAndAtomicSpecies.*?\n(.*?)%endblock AtomicCoordinatesAndAtomicSpecies"
    with open(path_input, "r", errors="ignore") as input_file:
        text = input_file.read()
        old_input_geometry = re.search(input_geometry_pattern, text, re.DOTALL)
        text = text.replace(old_input_geometry.group(1), new_geometry)

    with open(path_input, "w") as input_file_new:
        input_file_new.write(text) 