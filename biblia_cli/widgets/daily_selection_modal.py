from textual import on
from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Label, ListItem, ListView, Button
from textual.containers import Vertical, Horizontal

class DailySelectionModal(ModalScreen):
    DEFAULT_CSS = """
    DailySelectionModal { align: center middle; }
    #ds-box { width: 50; height: auto; background: $surface; border: thick $primary; padding: 1 2; }
    #ds-title { text-style: bold; color: $accent; text-align: center; width: 100%; margin-bottom: 1; }
    #ds-list { height: auto; border: solid $primary; margin-bottom: 1; }
    #ds-foot { height: 3; align: right middle; }
    """

    def __init__(self, readings: list[dict]):
        super().__init__()
        self.readings = readings

    def compose(self) -> ComposeResult:
        with Vertical(id="ds-box"):
            yield Label("📅 Lecturas de hoy", id="ds-title")
            with ListView(id="ds-list"):
                for i, r in enumerate(self.readings):
                    li = ListItem(Label(f"[bold]{r['label']}[/bold]  [dim]({r['source']})[/dim]"))
                    li.reading_index = i
                    yield li
            with Horizontal(id="ds-foot"):
                yield Button("Cancelar", id="ds-cancel")

    def on_mount(self):
        self.query_one("#ds-list", ListView).focus()

    @on(ListView.Selected, "#ds-list")
    def on_select(self, event):
        if event.item:
            idx = getattr(event.item, "reading_index", None)
            if idx is not None:
                self.dismiss(self.readings[idx])

    @on(Button.Pressed, "#ds-cancel")
    def cancel(self):
        self.dismiss(None)
