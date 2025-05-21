#!/usr/bin/env python3

import psutil
import shutil
import math
import platform
from pprint import pformat
from pathlib import Path
import yaml


FILE_ERROR = "FILE_NOT_FOUND"
CONFIG_FORMAT_ERROR = "CONFIG_NOT_DICT" 

def byte2human( in_bytes:int|float)->str:
    """Converts `int` and `float` bytes to human-readable string

    E.g.:
        >> print(byte2human(1024))
        1Ki
    """
    if not( in_bytes > 0):
        raise(ValueError("input must be positive int or float"))
    magnitude = ('Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei')

    id = min( max( 0, int(math.log2(in_bytes)/10) -1), len(magnitude) - 1 )
    scaled_value = f"{in_bytes / (1 << ((1 + id)*10)):.1f}"
    
    if scaled_value.split('.')[-1] == '0':
        scaled_value = scaled_value[:-2]
    
    return f"{scaled_value}{magnitude[id]}"

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



def machine_info():
    """Provides machine information as a dict of strings with following keys:
    
    - hostname : hostname of the machine on the network,
    - os : name of the operating system (OS),
    - version : OS version,
    - kernel : Linux kernel version (only on Linux),
    - arch : CPU architecture, e.g., x64, arm64, etc..
    - cpu : processor name,
    - cpu_count : number of physical CPU cores and logical in parentheses, e.g. "32 (64 logical)",
    - mem_tot : total physical memory (excludes swap).

    """
    ver = ''
    kernel = ''
    os_name = ''

    match platform.system():
        case 'Linux':
            try:
                os_ver_info = platform.freedesktop_os_release()
                os_name = os_ver_info.get('ID', 'Linux')
                ver = f"{os_ver_info.get('VERSION_ID', 'UNKNOWN')}"
                if 'VARIANT_ID' in os_ver_info:
                    ver = f"{ver} ({os_ver_info['VARIANT_ID']})"
            except OSError:
                os_name = "Linux"
                ver = 'Unknown'
            kernel = f'linux {platform.release()}'
        case 'Darwin':
            os_name = 'macos'
            ver = platform.mac_ver()[0]
            kernel = f"darwin {platform.release()}"
        case 'Windows':
            os_name = 'windows'
            ver = platform.release()
            kernel = platform.win32_ver()[1]

    return {'hostname' : platform.node(),
            'os' : os_name,
            'version' : ver,
            'kernel' : kernel,
            'arch' : platform.machine(),
            'cpu' : platform.processor(),
            'cpu_count' : f"{psutil.cpu_count(logical=False)} ({psutil.cpu_count()} logical)",
            'mem_tot' : byte2human(psutil.virtual_memory().total),
            }


class MachineMetric():
    _NUM_CPU =  psutil.cpu_count() # logical CPUs

    def __init__(self, config=None) -> None:
        self.info = machine_info()
        self.errors = ""
        self.storage_config = None

        if config == None:
            return
        try:
            configs = read_config(config)
        except Exception as e:
            self.errors = str(e)
            return

        if "storage" in configs:
            self.storage_config = configs["storage"]
            if not isinstance(configs["storage"], dict):
                self.errors += f"; MachineMetric storage_config:{CONFIG_FORMAT_ERROR}"

    def __str__(self) -> str:
        return f'{self.__class__.__name__}:'+pformat(self.info, sort_dicts=False)

    def __repr__(self) -> str:
        info = ','.join(map( lambda i: f"{i[0]}={i[1]}", self.info.items()))
        return f"{self.__class__.__name__}: {info}"

    def metrics(self, percpu=False):
        """Returns dict of strings with keys:
        
        - cpu_usage : CPU utilisation as a percentage; set "percpu=True" to get usage for cores
        - cpu_load : Average CPU load over last 1, 5 and 15 minutes as a percentage. 
        - mem_usage : Physical memory utilisation as a percentage. Available free memory is included in parentheses. 
        - disk_usage :
        - network_stats :

        """
        machine_metrics = {
            'cpu_usage': self._get_cpu_percent(percpu),
            'cpu_load' : self._get_cpu_load(),
            'mem_usage': self._get_memory_usage(),
            'disk_usage':self._get_disk_usage(),
            'network_stats': self._get_network_stats(),
        }
        return machine_metrics

    def _get_disk_usage(self):
        append = True
        if (self.storage_config != None) and isinstance(self.storage_config, dict):
            if "append" in self.storage_config:
                append = self.storage_config["append"]
        return f"append:{append}"

    @staticmethod
    def _get_memory_usage():
        try:
            mem_usage = psutil.virtual_memory()
            return f"{mem_usage.percent:.1f}% ({byte2human(mem_usage.available)} avail)"
        except Exception as err:
            return f"Unexpected {err} when getting memory usage"

    def _get_cpu_load(self):
        ncpus = self._NUM_CPU
        if ncpus is None:
            return ""

        load = psutil.getloadavg()
        if (len(load) < 3) or (None in load):
            return ""
        
        load_str = map( lambda x: f"{(100 * x / ncpus) :.1f}%" , psutil.getloadavg() )
        return " ".join(load_str)

    @staticmethod
    def _get_cpu_percent(percpu):
        if percpu:
            return " ".join(map(lambda c: f"{c:.1f}%", psutil.cpu_percent(interval=.2, percpu=True)))
        return f"{psutil.cpu_percent(interval=.2,percpu=False):.1f}%"

    @staticmethod
    def _get_network_stats():
        #psutil.net_if_stats()
        return None


