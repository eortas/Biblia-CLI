from textual import on
from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Button, Label, ListView, ListItem
from textual.containers import Vertical, Horizontal
from ..favorites import all_favorites

class FavoritesModal(ModalScreen):
    DEFAULT_CSS="""
    FavoritesModal { align: center middle; }
    #f-box { width: 62; height: auto; max-height: 36; background: $surface; border: thick $primary; padding: 1 2; }
    #f-title { text-style: bold; color: $accent; text-align: center; width: 100%; margin-bottom: 1; }
    #f-list  { height: 20; border: solid $primary; }
    #f-empty { text-align: center; color: $text-muted; padding: 2 0; }
    #f-foot  { height: 3; margin-top: 1; align: right middle; }
    """
    def compose(self) -> ComposeResult:
        self._favs=all_favorites()
        with Vertical(id="f-box"):
            yield Label("⭐ Marcadores",id="f-title")
            if self._favs: yield ListView(id="f-list")
            else: yield Label("No tienes marcadores.\nPulsa Ctrl+F en cualquier capítulo.",id="f-empty")
            with Horizontal(id="f-foot"):
                if self._favs: yield Button("Ir al capítulo",id="f-go",variant="primary")
                yield Button("Cerrar",id="f-close",variant="error")
    def on_mount(self):
        if not self._favs: return
        lv=self.query_one("#f-list",ListView)
        for f in self._favs:
            lv.append(ListItem(Label(f"[bold]{f['book_name']} {f['chapter']}[/bold]  [{f['translation']}]  {f['added_at'][:10]}")))
    @on(Button.Pressed,"#f-go")
    def go(self):
        idx=self.query_one("#f-list",ListView).index
        self.dismiss(self._favs[idx] if idx is not None and idx<len(self._favs) else None)
    @on(Button.Pressed,"#f-close")
    def close(self): self.dismiss(None)