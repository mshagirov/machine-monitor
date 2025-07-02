from asyncio import sleep
from pathlib import Path
import sys

from textual import work
from textual.reactive import reactive
from textual.app import App, ComposeResult, RenderResult
from textual.widget import Widget
from textual.widgets import Footer, Static #Header
from textual.binding import Binding

from config import read_config, valid_monitor_list
from getrequest import http_get


class Rows(Widget):
    content = reactive("metrics")

    def render(self) -> RenderResult:
        return f"{self.content}"

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

    monitor = {}

    def compose(self) -> ComposeResult:
        self.theme = "catppuccin-mocha"
        yield Static(' Machine Monitor ', id='title')
        yield Rows()
        yield Footer()

    
    def on_mount(self) -> None:
        self.load_data()

    @work
    async def load_data(self) -> None:
        while True:
            if len(self.monitor) < 1:
                self.query_one(Rows).content = "hosts list is empty"
            else:
                for k, v in self.monitor.items():
                    self.query_one(Rows).content = f"{k} :\n\t{http_get(v, "metrics")}"
                    break
            await sleep(5)

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
        nodes = read_config(path_to_list)
    except Exception as e:
        print(e)
        sys.exit(1)

    if not valid_monitor_list(nodes):
        print(f"Monitoring list is empty:\n\t{path_to_list}")
        sys.exit(1)

    # for node_name, url in nodes['monitor'].items():
    #     print(node_name)
    #     print(http_get(url, 'info'))
    #     print(http_get(url, 'metrics'))
    app = MachineMonitor()
    app.monitor = nodes['monitor']
    app.run()

