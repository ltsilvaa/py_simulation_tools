import os

def chage_input_cell_optmization_type(is_cell_relax: bool, work_directory: str, input_name: str):
    """
    
    """
    path_input = os.path.join(work_directory,input_name)
    with open(path_input, "r", erros="ignore") as input_file:
        text = input_file.readlines()
        for line in text:
            if "MD.VariableCell" in line:
                if is_cell_relax:
                    line = "MD.VariableCell true"
                else:
                    line = "MD.VariableCell false"

    with open(path_input, "w") as modified_imput_file:
        modified_imput_file.write(text)