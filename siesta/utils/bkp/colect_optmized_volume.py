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