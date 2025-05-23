# `machine-monitor` 

> A Python Tool for Querying Machine Health & Usage (mainly for Linux machines)

## Environment Setup

> Requirements are listed in the [requirements.txt](./requirements.txt)

1. Clone the repo

```bash
git clone https://github.com/mshagirov/machine-monitor.git
```

2. Create a new enviroment using tools such as `venv` or `uv`,

```bash
cd machine-monitor
python3 -m venv .venv
```

3. Activate the enviroment and install the requirements:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

4. Test `monitor.MachineMetric`:


```bash
./main.sh
```

Above should print information about the machine, e.g.:

```
------------------------ Information about the machine -------------------------
{'hostname': 'macair',
 'os': 'macos',
 'version': '15.5',
 'kernel': 'darwin 24.5.0',
 'arch': 'arm64',
 'cpu': 'arm',
 'cpu_count': '8 (8 logical)',
 'mem_tot': '24Gi'}
------------------------------- Machine metrics --------------------------------
{'cpu_usage': '2.5%',
 'cpu_load': '15.7%; 16.5%; 19.8%',
 'mem_usage': '53.5% (11.2Gi avail)',
 'disk_usage': 'root_dir:24.0% (1.4Ti free); does_not_exist:[Errno 2] No such '
               "file or directory: '/error'",
 'network_stats': 'lo0:up,speed=NA; internet(en0):up,speed=NA',
 'connections': 'google-dns(8.8.8.8):53=up'}
-------------------------- Configuration Information ---------------------------
Errors:
''
Storage config-s:
{'append': False,
 'root_dir': {'mountpoint': '/', 'fstype': None},
 'gpfs0': {'mountpoint': '/gpfs0', 'fstype': 'gpfs'},
 'nfsshare': {'mountpoint': '/mynfs', 'fstype': 'nfs'},
 'does_not_exist': {'mountpoint': '/error', 'fstype': None}}
Network config-s:
{'append': False, 'localhost': {'ifname': 'lo*'}, 'internet': {'ifname': 'en0'}}
Connection config-s:
{'google-dns': {'host': '8.8.8.8', 'port': 53}}
```

## Notes

`network_stats` and `connections` metrics work only for Unix machines and are not accurate for MacOS. On Linux, these should correctly detect and show connection or interface as "down" and show errors in the metrics fields (e.g., "timeout") if the interface or connection is down.

On MacOS, `network_stats` only checks if the interface exists and does not detect if it is disconnected. `connections` always shown as "up" even when it should be "down". Hence these functionalities should be reimplemented for MacOS, e.g., using MacOS' `ipconfig` tool. Currently, I do not need this functionality on MacOS and do not plan to work on it, at least in the foreseeable future.

## Future Plans (for Linux)

Future plans to add following functionality

- [ ] Network API to query remote machines
- [ ] CLI monitoring interface

