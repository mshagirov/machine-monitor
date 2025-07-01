#!/usr/bin/env python3

import psutil
import shutil
from pprint import pformat
from pathlib import Path

from constants import *
from network import check_connection
from config import get_network_config, read_config, get_storage_config, get_connection_config
from convert import byte2human
from info import machine_info

class MachineMetric():
    _NUM_CPU =  psutil.cpu_count() # logical CPUs

    def __init__(self, config : None | str | Path =None) -> None:
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
            self.storage_config, storage_errors = get_storage_config(configs)
            if storage_errors != None:
                self.errors += f"; storage:{storage_errors}"
        if "network" in configs:
            self.network_config, if_errors = get_network_config(configs)
            if if_errors != None:
                self.errors += f"; net:{if_errors}"
        if "connection" in configs:
            self.connection_config, conn_errors = get_connection_config(configs)
            if conn_errors != None:
                self.errors += f"; conn:{conn_errors}"

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
        - disk_usage : check storage usage of the partitions, output depends on the *optional* "storage" configuration
                       section of the input config.yaml file.
        - network_stats : check network interfaces, output depends on the *optional* "network" configuration section of
                          the input config.yaml file.
        - connections : check connections to hosts on the network, *requires* (host, port) pairs to be specified in the
                        input config.yaml.
        network_stats and connections metrics show accurate information about the interface/connection ONLY in Linux OS. 

        """
        machine_metrics = {
            'cpu_usage': self._get_cpu_percent(percpu),
            'cpu_load' : self._get_cpu_load(),
            'mem_usage': self._get_memory_usage(),
            'disk_usage':self._get_disk_usage(),
            'network_stats': self._get_network_stats(),
            'connections': self._get_check_connection(),
        }
        return machine_metrics

    def _get_check_connection(self):
        if self.connection_config == None:
            return ""
        connections = []
        for alias, props in self.connection_config.items():
            try:
                conn_name = alias if alias == props.get('host') else f"{alias}({props.get('host')})"

                ok, err = check_connection(props.get('host'), props.get('port'), 3)
                res = "up" if ok else "down"
                
                res_fmt = f"{conn_name}:{props.get('port')}={res}"
                if err != None:
                    res_fmt += f" {err}"
                connections.append(res_fmt)
            except Exception as e:
                connections.append(f"{alias}:error {e}{type(e)}")

        if not connections:
            return CONN_ERROR

        return "; ".join(connections)

    def _get_network_stats(self):
        try:
            if_stats = psutil.net_if_stats()
        except Exception as e:
            return f"Error {e}{type(e)} when getting net_if_stats" 
        
        append = True # default
        net_ifs = {}
        if self.network_config != None:
            if "append" in self.network_config:
                append = self.network_config["append"]
            for iname in self.network_config:
                if iname == "append":
                    continue
                ifname = self.network_config[iname].get('ifname')
                if (ifname is None) or (ifname in net_ifs.values()):
                    continue
                elif ifname.endswith('*'):
                    for i in if_stats:
                        if i in net_ifs.values():
                            continue
                        if i.startswith(ifname[:-1]):
                            net_ifs[i] = i
                    continue
                net_ifs[iname] = ifname
                
        if append:
            for i in if_stats:
                if i in net_ifs.values():
                    continue
                net_ifs[i] = i
        if not net_ifs:
            return IF_ERROR
        if_info = []
        for ifname, i in net_ifs.items():
            ifalias = i if i==ifname else f"{ifname}({i})"
            try:
                isup = "up" if if_stats[i].isup else "down"
                ifspeed = if_stats[i].speed if if_stats[i].speed>0 else 'NA'
                if_info.append(f"{ifalias}:{isup},speed={ifspeed}")
            except Exception as e:
                if_info.append(f"{ifalias}:{e}")
        return "; ".join(if_info)

    def _get_disk_usage(self):
        try:
            all_fstype = {p.mountpoint:p.fstype for p in psutil.disk_partitions(all=True)}
            phys_mps = [p.mountpoint for p in psutil.disk_partitions(all=False)]
        except Exception as e:
            return f"Unexpected {e} when getting partitions"

        append = True # default
        mountpoints = {}
        if self.storage_config != None:
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
                fstype = all_fstype.get(mp)
                if (fstype != None) and (fstype == self.storage_config[mpname]['fstype']):
                    mountpoints[mpname] = mp
        if append:
            for p in phys_mps:
                if p in mountpoints.values():
                    continue
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

