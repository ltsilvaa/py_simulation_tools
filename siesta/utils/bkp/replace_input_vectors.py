import os
import re

def replace_input_vectors(work_directory: str,  input_name: str, new_vectors: str):
    """

    """
    path_input = os.path.join(work_directory, input_name)
    input_vectors_pattern = r"%block LatticeVectors\n.*?(.*?)%endblock LatticeVectors"
    with open(path_input, "r", errors="ignore") as input_file:
        text = input_file.read()
        input_vectors = re.search(input_vectors_pattern, text, re.DOTALL)
        text = text.replace(input_vectors.group(1), new_vectors)

    with open(path_input, "w") as input_file_new:
        input_file_new.write(text)