from textual import on, work
from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label, ListView, ListItem
from textual.containers import Vertical, Horizontal
from ..api.bolls_client import BollsClient
from ..book_names import BOOKS, lang_for_translation

class SearchModal(ModalScreen):
    DEFAULT_CSS="""
    SearchModal { align: center middle; }
    #s-box  { width: 82; height: 32; background: $surface; border: thick $primary; padding: 1 2; }
    #s-title{ text-style: bold; color: $accent; text-align: center; width: 100%; margin-bottom: 1; }
    #s-input{ margin-bottom: 1; }
    #s-list { height: 1fr; border: solid $primary; }
    #s-foot { height: 3; margin-top: 1; align: right middle; }
    """
    def __init__(self,translation,books):
        super().__init__(); self.translation=translation
        self.lang=lang_for_translation(translation)
        self.names={bid:(es if self.lang=="es" else pt) for bid,es,pt,_ in BOOKS}
        self.client=BollsClient(); self.results=[]
    def compose(self) -> ComposeResult:
        with Vertical(id="s-box"):
            yield Label("🔍 Buscar en la Biblia",id="s-title")
            yield Input(placeholder="ej: de tal manera amó Dios...",id="s-input")
            yield Label("",id="s-count"); yield ListView(id="s-list")
            with Horizontal(id="s-foot"):
                yield Button("Ir al versículo",id="s-go",variant="primary"); yield Button("Cerrar",id="s-close",variant="error")
    def on_mount(self): self.query_one("#s-input",Input).focus()
    @on(Input.Submitted,"#s-input")
    def do_search(self,event):
        if event.value.strip(): self._search(event.value.strip())
    @work
    async def _search(self,query):
        lbl=self.query_one("#s-count",Label); lbl.update("⏳ Buscando...")
        lv=self.query_one("#s-list",ListView); lv.clear(); self.results=[]
        try:
            data=await self.client.search(self.translation,query,limit=50)
            self.results=data.get("results",[])
            lbl.update(f"✅ {len(self.results)} de {data.get('total',0)} resultados")
            for r in self.results:
                nm=self.names.get(r["book"],str(r["book"]))
                lv.append(ListItem(Label(f"[bold]{nm} {r['chapter']}:{r['verse']}[/bold]  {r['text'][:70]}…")))
        except Exception as e: lbl.update(f"❌ {e}")
    @on(Button.Pressed,"#s-go")
    def go(self):
        idx=self.query_one("#s-list",ListView).index
        if idx is not None and idx<len(self.results): r=self.results[idx]; self.dismiss((r["book"],r["chapter"]))
        else: self.dismiss(None)
    @on(Button.Pressed,"#s-close")
    def close(self): self.dismiss(None)