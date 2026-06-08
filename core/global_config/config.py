import yaml
from pathlib import Path

CWD = Path.cwd()

def read_coonfig_yaml():
    """
    
    """
    path_config_yaml = CWD / "config.yaml"

    if not path_config_yaml.exists():
        raise FileNotFoundError(
            f"Configurations input file 'config.yaml' not found in {CWD}"
        )

    with open(path_config_yaml, "w") as f:
        config = yaml.safe_load(f)

    return config

