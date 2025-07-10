from tuiapp import MachineMonitor 
from pathlib import Path
import sys

from config import read_config, valid_monitor_list

if __name__ == "__main__":
    if len(sys.argv) > 1:
        path_to_list = sys.argv[1]
    else:
        path_to_list = Path(__file__).resolve().parent / "list.yaml"

    if len(sys.argv) > 2:
        delay = int(sys.argv[2])
    else:
        delay = 5

    try:
        nodes = read_config(path_to_list)
    except Exception as e:
        print(e)
        sys.exit(1)

    if not valid_monitor_list(nodes):
        print(f"Monitoring list is empty:\n\t{path_to_list}")
        sys.exit(1)
    app = MachineMonitor()
    
    app.monitor = nodes['monitor']
    app.delay_in_seconds = delay

    app.run()

