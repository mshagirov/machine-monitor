from asyncio import sleep

from textual import work
from textual.reactive import reactive
from textual.app import App, ComposeResult, RenderResult
from textual.widget import Widget
from textual.widgets import Footer, Static, DataTable #Header
from textual.binding import Binding
from getrequest import http_get
from columns import column_names_, make_row

class Rows(Widget):
    content = reactive("metrics")

    def render(self) -> RenderResult:
        return f"{self.content}"

class Table(Widget):
    columns = reactive("column names")


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
        yield DataTable()
        yield Footer()

    
    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.cursor_type = "row"
        table.zebra_stripes = True
        table.add_columns(*column_names_)
        self.load_data()

    @work
    async def load_data(self) -> None:
        if len(self.monitor) <1:
            return
        table = self.query_one(DataTable)
        row_keys = []
        row_info = {}
        for k, v in self.monitor.items():
            row_info[k] = http_get(v,"info")
            row_keys.append(
                table.add_row(*make_row(row_info[k]), key=k, label=k)
            )
        print(row_keys)
        # while True:
        #     for k, v in self.monitor.items():
        #         self.query_one(Rows).content = f"{k} :\n\t{http_get(v, "metrics")}"
        #         break
        #     await sleep(5)

    def action_toggle_dark(self) -> None:
        self.theme = (
            "catppuccin-mocha" if self.theme == "catppuccin-latte" else "catppuccin-latte"
        )

