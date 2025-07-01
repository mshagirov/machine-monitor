from pathlib import Path
import yaml

from constants import *

def read_config(path_to_file : str | Path ='config.yaml'):
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

def get_storage_config(configs : dict):
    storage_config = configs.get("storage", None)
    if not isinstance(storage_config, dict):
        return None, f"storage_config:{CONFIG_FORMAT_ERROR}"

    for mpname in storage_config:
        if mpname == 'append':
            continue
        if 'fstype' not in storage_config[mpname]:
            storage_config[mpname]['fstype'] = None
    return storage_config, None

def get_network_config(configs : dict):
    network_config = configs.get("network", None)
    if not isinstance(network_config, dict):
        return None, f"network_config:{CONFIG_FORMAT_ERROR}"

    return network_config, None

def get_connection_config(configs : dict):
    connection_config = configs.get("connection", None)
    if not isinstance(connection_config, dict):
        return None, f"connection_config:{CONFIG_FORMAT_ERROR}"
    
    return connection_config, None

