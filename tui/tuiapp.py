from asyncio import sleep

from textual import work
from textual.app import App, ComposeResult
from textual.widgets import Footer, Static, DataTable
from textual.binding import Binding
from getrequest import http_get
from columns import column_names_, make_row


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
                Binding('q', 'quit', 'Quit', show=True, priority=True)]

    monitor = {}
    delay_in_seconds = 5

    def compose(self) -> ComposeResult:
        self.theme = "catppuccin-mocha"
        yield Static(' ≡≡ Machine Monitor ≡≡ ', id='title')
        yield DataTable()
        yield Footer()

    
    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.cursor_type = "row"
        table.zebra_stripes = True
        self.load_data()

    @work
    async def load_data(self) -> None:
        if len(self.monitor) <1:
            return
        table = self.query_one(DataTable)
        column_keys = dict(zip( column_names_, table.add_columns(*column_names_)))
        row_keys = {}
        for k, host in self.monitor.items():
            row_template = make_row(info = http_get(host,"info") )
            row = [row_template[col_i] for col_i in column_names_]
            row_keys[k] = table.add_row(*row, key=k, label=k)
        while True:
            for k, host in self.monitor.items():
                row_k = row_keys[k]
                for col_idx, value in make_row(
                    info = http_get(host, "info"),
                    metrics = http_get(host, "metrics"),
                    template = True
                ).items():
                    col_k = column_keys[col_idx]
                    table.update_cell(row_key=row_k,
                                      column_key=col_k,
                                      value=value,
                                      update_width=True)
                table.refresh_row(table.get_row_index(row_k))
            await sleep(self.delay_in_seconds)

    def action_toggle_dark(self) -> None:
        self.theme = (
            "catppuccin-mocha" if self.theme == "catppuccin-latte" else "catppuccin-latte"
        )

