from pathlib import Path
import yaml

from constants import *

def read_config(path_to_file='config.yaml'):
    """
    path_to_file : location of YAML configuration file
    """
    if not isinstance(path_to_file, Path):
        path_to_file = Path(path_to_file)
    
    if not path_to_file.is_file():
        raise(Exception(f"read_config:{FILE_ERROR}"))
    
    with open(path_to_file, 'r') as f:
        content = yaml.safe_load(f)
    if not isinstance(content, dict):
        raise(Exception(f"read_config:{CONFIG_FORMAT_ERROR}"))
    return content


