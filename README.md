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
./example.sh
```

Above should print information about the machine, e.g.:

```sh
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

## Configuring Storage, Network, and Connection Metrics

Use the above example script and edit `mm/config.yaml` by following the comments
to configure storage, network and connection metrics reporting.

## Notes

`network_stats` and `connections` metrics work only for Unix machines and are
not accurate for MacOS. On Linux, these should correctly detect and show
connection or interface as "down" and show errors in the metrics fields (e.g.,
"timeout") if the interface or connection is down.

On MacOS, `network_stats` only checks if the interface exists and does not
detect if it is disconnected. `connections` always shown as "up" even when it
should be "down". Hence these functionalities should be reimplemented for MacOS,
e.g., using MacOS' `ipconfig` tool. Currently, I do not need this functionality
on MacOS and do not plan to work on it, at least in the foreseeable future.

## API

> Uses FastAPI to serve machine information (`/info`) and metrics (`/metrics`)
over network

### Testing and Development

To test API, run `dev.sh`:

```bash
./dev.sh
```

then open `http://127.0.0.1:8000/info` or `http://127.0.0.1:8000/metrics` to
view machine information and metrics respectively. Also, FastAPI automatically
builds documentation for these functions. The documentation can be viewed at `http://127.0.0.1:8000/docs`.

### Running API

To run API using the default port 8000, run `run.sh`:

```bash
./run.sh
```

or specify a port number to expose with `-p PORT`, e.g.,

```bash
./run.sh -p 8888
```

If your system blocks Python from using the port (i.e. MacOS), try using curl to
get the metrics/info from CLI, e.g. in terminal run:

```bash
curl -X 'GET' 'http://IP_ADDRESS:PORT/' -H 'accept: application/json'
```

where `IP_ADDRESS` is your machine's IP address on the network and `PORT` is the
port that the API is running on. This should prompt the system to request for
permission to allow Python to expose the service to the network. Then, you
should be able to go to `http://IP_ADDRESS:PORT/info` and
`http://IP_ADDRESS:PORT/metrics` to view machine information and metrics respectively.

### Running API in Detached Mode

Use `-d` option to run the API server in the background.

```bash
./run.sh -d
```

Check the PID of the parent process (bash) by reading `current_run.out`

```bash
# read the parent process' PID and API's IP:PORT
cat current_run.out
# obtain fastapi process id (PID)
pgrep -P PARENT
```

The last command prints the PID of the FastAPI server running in the background.
You can kill this process with `kill -9 PID` when you do not need it any longer.
In case if you accidentally close the parent process, you can search the child's
PID with `ps aux | grep fastapi`. Closing the parent process does not close the child
API server.

## TUI (Terminal User Interface) for Monitoring Machines

> Monitoring localhost: you can run `./dev.sh` and in another terminal
`./monitor_remote.sh` to monitor localhost (you may need to edit the "tui/list.yaml")

Edit `tui/list.yaml` by adding `HOST_NAME: "IP:PORT"` key-value pairs under the
`monitor:` key. Alternatively, create a new config or copy the host list to a new
location, and then add its path to the `monitor_remote.sh` before running the TUI.

To start the TUI app run:

```bash
./monitor_remote.sh
```

## Future Plans (for Linux)

Future plans to add following functionality

- [ ] Add GPU information
- [ ] Container image (for runnning as a service)
