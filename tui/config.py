from pathlib import Path
import yaml


def read_config(path_to_file: str | Path ='machine-list.yaml'):
    """
    path_to_file : location of YAML configuration file
    """
    if not isinstance(path_to_file, Path):
        path_to_file = Path(path_to_file)
    
    if not path_to_file.is_file():
        raise(FileNotFoundError)
    
    with open(path_to_file, 'r') as f:
        content = yaml.safe_load(f)
    if not isinstance(content, dict):
        raise(ValueError(f"YAML should contain 'monitor' key with machines and their URLs following format below:\nmonitor:\n  NAME: URL"))
    return content


def valid_monitor_list(monitor_list : dict):
    """Checks if dict object and has 'monitor' key entry with hostname entries"""
    if not isinstance(monitor_list.get('monitor'), dict):
        return False
    if len(monitor_list.get('monitor', {})) < 1:
        return False
    return True

