#!/usr/bin/env python3

import psutil
import shutil
import math


def byte2human( in_bytes:int|float)->str:
    if not( in_bytes > 0):
        raise(ValueError("input must be positive int or float"))
    
    magnitude = ('K', 'M', 'G', 'T', 'P', 'E')

    id = min( max( 0, int(math.log2(in_bytes)/10) -1), len(magnitude) - 1 )
    scaled_value = f"{in_bytes / (1 << ((1 + id)*10)):.1f}"
    if scaled_value.split('.')[-1] == '0':
        scaled_value = scaled_value[:-2]
    return f"{scaled_value}{magnitude[id]}"

class MachineMonitor():
    def metrics(self):
        pass

    def _get_cpu_usage(self):
        pass

    def _get_disk_usage(self):
        pass

    def _get_network_stats(self):
        #psutil.net_if_stats()
        pass


