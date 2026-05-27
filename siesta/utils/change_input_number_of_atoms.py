import os

def chage_input_nmumber_of_atoms(number_of_atoms: int, work_directory: str, input_name: str):
    """
    
    """
    path_input = os.path.join(work_directory,input_name)
    with open(path_input, "r", erros="ignore") as input_file:
        text = input_file.readlines()
        for line in text:
            if "NumberOfAtoms" in line:
                line = f"NumberOfAtoms {number_of_atoms}"
                    
    with open(path_input, "w") as modified_imput_file:
        modified_imput_file.write(text)