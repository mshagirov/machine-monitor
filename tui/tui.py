from pathlib import Path
from re import S
import sys
import requests

from textual.app import App, ComposeResult
from textual.widgets import Footer, Static #Header
from textual.binding import Binding

from config import get_list

exp_char_ = "┣"
col_char_ = "╠"

def get_info(hostname : str):
    try:
        res = requests.get("http://" + hostname + "/info", headers={"accept": "application/json"})
        return res.json()
    except Exception as e:
        return {'error':str(e)}

def get_metrics(hostname : str):
    try:
        res = requests.get("http://" + hostname + "/metrics", headers={"accept": "application/json"})
        return res.json()
    except Exception as e:
        return {'error':str(e)}

def valid_list(nodes):
    if not isinstance(nodes.get('monitor'), dict):
        return False
    if len(nodes.get('monitor')) < 1:
        return False
    return True

class MachineMonitor(App):
    """A Terminal app to monitor machines over the network via requests API"""

    CSS = """\
#title {
    content-align-horizontal: center;
    text-style: reverse;
}
"""
    # Key bindings
    BINDINGS = [('d', 'toggle_dark', 'Toggle dark mode'),
                Binding('q', 'quit', 'Quit', show=False, priority=True)]

    def compose(self) -> ComposeResult:
        self.theme = "catppuccin-mocha"
        # yield Header(name='Machines', show_clock=True)
        yield Static(' Machine Monitor ', id='title')
        yield Footer()

    def action_toggle_dark(self) -> None:
        self.theme = (
            "catppuccin-mocha" if self.theme == "catppuccin-latte" else "catppuccin-latte"
        )




if __name__ == "__main__":
    if len(sys.argv) > 1:
        path_to_list = sys.argv[1]
    else:
        path_to_list = Path(__file__).resolve().parent / "list.yaml"

    try:
        nodes = get_list(path_to_list)
    except Exception as e:
        print(e)
        sys.exit(1)

    if not valid_list(nodes):
        print(f"Monitoring list is empty:\n\t{path_to_list}")
        sys.exit(1)

    for node_name, url in nodes['monitor'].items():
        print(node_name)
        print(get_info(url))
        print(get_metrics(url))
    app = MachineMonitor()
    app.run()

