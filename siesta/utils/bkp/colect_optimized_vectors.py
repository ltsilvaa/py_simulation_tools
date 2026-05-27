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
