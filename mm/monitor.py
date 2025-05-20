#!/usr/bin/env python3

import psutil
import shutil
import math
import platform
from collections import namedtuple


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

def machine_info():
    """Provides machine information as a dict of strings with following keys:
    
    - hostname : hostname of the machine on the network,
    - os : name of the operating system (OS),
    - version : OS version,
    - kernel : Linux kernel version (only on Linux),
    - arch : CPU architecture, e.g., x64, arm64, etc..
    - cpu : processor name
    - cpu_count : number of physical CPU cores and logical in parentheses, e.g. "32 (64 logical)".

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
            'cpu_count' : f"{psutil.cpu_count(logical=False)} ({psutil.cpu_count()} logical)",}


class MachineMonitor():
    @staticmethod
    def info():
        "Calls monitor.machine_info()"
        return machine_info()

    @staticmethod
    def metrics():
        machine_metrics = {
            'cpu_usage': MachineMonitor._get_cpu_usage(),
            'mem_usage': MachineMonitor._get_memory_usage(),
            'disk_usage': MachineMonitor._get_disk_usage(),
            'network_stats': MachineMonitor._get_network_stats(),
        }
        return machine_metrics

    @staticmethod
    def _get_cpu_usage():
        cpu_use = map(lambda c: f"{c:.1f}", psutil.cpu_percent(interval=.2, percpu=True))
        return " ".join(cpu_use)
        

    @staticmethod
    def _get_memory_usage():
        return None

    @staticmethod
    def _get_disk_usage():
        # byte2human(1024**3) -> 1Gi
        return None

    @staticmethod
    def _get_network_stats():
        #psutil.net_if_stats()
        return None


