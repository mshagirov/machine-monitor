#!/usr/bin/env python3

import psutil
import shutil
from pprint import pformat

from constants import *
from read_config import read_config
from convert import byte2human
from info import machine_info

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
            for mpname in self.storage_config:
                if mpname == 'append':
                    continue
                if 'fstype' not in self.storage_config[mpname]:
                    self.storage_config[mpname]['fstype'] = None

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
        try:
            all_fstype = {p.mountpoint:p.fstype for p in psutil.disk_partitions(all=True)}
            phys_mps = [p.mountpoint for p in psutil.disk_partitions(all=False)]
        except Exception as e:
            return f"Unexpected {e} when getting partitions"

        append = True
        mountpoints = {}
        if (self.storage_config != None) and isinstance(self.storage_config, dict):
            if "append" in self.storage_config:
                append = self.storage_config["append"]
            for mpname in self.storage_config:
                if mpname == "append":
                    continue
                mp = self.storage_config[mpname]['mountpoint']
                if self.storage_config[mpname]['fstype'] is None:
                    # no need to check is not specified
                    mountpoints[mpname] = mp
                    continue

                # fstype != None, then check if mountpoint exists & has correct fstype
                fstype = all_fstype.get(mp, None)
                if (fstype != None) and (fstype == self.storage_config[mpname]['fstype']):
                    mountpoints[mpname] = mp
        if append:
            for p in phys_mps:
                mountpoints[p] = p

        if not mountpoints:
            return MP_ERROR
        
        disk_usage = []
        for p in mountpoints:
            try:
                p_tot, _, p_free = shutil.disk_usage(mountpoints[p])
                p_used = 100*(p_tot - p_free)/p_tot
                disk_usage.append(f"{p}:{p_used:.1f}% ({byte2human(p_free)} free)")
            except Exception as e:
                disk_usage.append(f"{p}:{e}")
        return "; ".join(disk_usage)

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
        return "; ".join(load_str)

    @staticmethod
    def _get_cpu_percent(percpu):
        if percpu:
            return " ".join(map(lambda c: f"{c:.1f}%", psutil.cpu_percent(interval=.2, percpu=True)))
        return f"{psutil.cpu_percent(interval=.2,percpu=False):.1f}%"

    @staticmethod
    def _get_network_stats():
        #psutil.net_if_stats()
        return None


