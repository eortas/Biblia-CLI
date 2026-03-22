from __future__ import annotations
from textual import on, work
import httpx
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.reactive import reactive
from textual.screen import ModalScreen
from textual.widgets import Button, Footer, Header, Input, Label, ListItem, ListView, Static
from .api.bolls_client import BollsClient
from .book_names import get_books_for_lang, lang_for_translation
from .config import Config
from .favorites import toggle as fav_toggle, is_favorite
from .notes import get_chapter_notes
from .annotations import get_chapter as ann_get_chapter
from .themes import next_theme, LABELS
from .widgets.annotation_modal import AnnotationReadModal
from .widgets.favorites_modal import FavoritesModal
from .widgets.note_modal import NoteModal
from .widgets.search_modal import SearchModal
from .widgets.splash_screen import SplashScreen
from .widgets.translation_modal import TranslationModal

class BibliaApp(App):
    CSS_PATH = "css/app.tcss"
    ENABLE_COMMAND_PALETTE = False
    BINDINGS = [
        Binding("q",      "quit",         "Salir"),
        Binding("t",      "switch_lang",  "[T] Idioma"),
        Binding("ctrl+t", "cycle_theme",  "[^T] Tema"),
        Binding("/",      "open_search",  "[/] Buscar"),
        Binding("ctrl+f", "toggle_fav",   "[^F] ★"),
        Binding("f",      "open_favs",    "[F] Marcadores"),
        Binding("n",      "add_note",     "[N] Nota"),
        Binding("h",      "read_ann",     "[H] ✦ Leer"),
        Binding("d",      "daily",        "[D] Lectura hoy"),
        Binding("escape", "clear_filter", "Limpiar"),
    ]
    translation: reactive[str] = reactive("RV1960")
    biblia_theme: reactive[str] = reactive("dark")

    def __init__(self):
        super().__init__()
        self.cfg = Config(); self.client = BollsClient()
        self.books: list[dict] = []; self.book: dict | None = None
        self.chapter: int = 1; self._verses_cache: list[dict] = []

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Horizontal(id="main"):
            with Vertical(id="books-panel"):
                yield Label("📚 LIBROS", classes="panel-title")
                yield Input(placeholder="🔍 Filtrar...", id="books-filter")
                yield ListView(id="books-list")
            with Vertical(id="chapters-panel"):
                yield Label("📖 CAP.", classes="panel-title")
                yield ListView(id="chapters-list")
            with VerticalScroll(id="scripture-panel"):
                yield Label("", id="scripture-title")
                yield Label("", id="fav-indicator")
                yield Static("", id="scripture-content", markup=True)
        yield Footer()

    def on_mount(self):
        self.push_screen(SplashScreen())
        self._start()

    def _start(self, _=None):
        s = self.cfg.load(); self.translation = s["translation"]; self.biblia_theme = s.get("theme","dark")
        self._set_title()
        self.load_books(s.get("last_book_id"), s.get("last_chapter",1))

    def _set_title(self):
        self.title = f"📖 Biblia CLI  ·  {self.translation}  ·  {LABELS[self.biblia_theme]}"

    def watch_biblia_theme(self, t: str):
        self._apply_theme(t)

    def on_screen_resume(self) -> None:
        self._apply_theme(self.biblia_theme)

    def _apply_theme(self, t):
        for o in [self, self.screen]:
            for c in list(o.classes):
                if c.startswith("theme-"): o.remove_class(c)
            o.add_class(f"theme-{t}")
    @work(exclusive=True)
    async def load_books(self, restore_id=None, restore_ch=1):
        bl = self.query_one("#books-list", ListView); bl.clear()
        try: self.books = await self.client.get_books(self.translation)
        except Exception:
            self.books = get_books_for_lang(lang_for_translation(self.translation))
            self.notify("Sin conexión — lista offline", timeout=3)
        seen = set()
        for b in self.books:
            bid = b["bookid"]
            if bid in seen: continue
            seen.add(bid)
            li = ListItem(Label(b["name"]))
            li.book_id = bid
            bl.append(li)
        if restore_id:
            tgt = next((b for b in self.books if b["bookid"]==restore_id), None)
            if tgt: self.book=tgt; self._fill_chapters(tgt["chapters"],restore_ch); self.load_scripture()

    def _fill_chapters(self, total, highlight=1):
        cl = self.query_one("#chapters-list", ListView); cl.clear()
        for i in range(1, total+1): cl.append(ListItem(Label(str(i))))
        if highlight <= total: self.chapter=highlight; cl.index=highlight-1

    @work(exclusive=True)
    async def load_scripture(self):
        if not self.book: return
        tw=self.query_one("#scripture-title",Label); cw=self.query_one("#scripture-content",Static); fw=self.query_one("#fav-indicator",Label)
        tw.update("⏳ Cargando..."); cw.update(""); fw.update("")
        try: raw = await self.client.get_chapter(self.translation, self.book["bookid"], self.chapter)
        except Exception as e: tw.update(f"[red]❌ {e}[/red]"); return
        self._verses_cache = raw
        verses = raw
        notes  = get_chapter_notes(self.translation, self.book["bookid"], self.chapter)
        ann    = await ann_get_chapter(self.translation, self.book["bookid"], self.chapter)
        tw.update(f"[bold #d4a017]{self.book['name']}[/bold #d4a017]  [bold cyan]Cap. {self.chapter}[/bold cyan]  [dim]{self.translation}[/dim]")
        fw.update("[bold #d4a017]⭐ Marcado[/bold #d4a017]" if is_favorite(self.translation,self.book["bookid"],self.chapter) else "")
        lines=[]
        for v in verses:
            vn=v["verse"]
            note_icon  = " [bold #d4a017]✏[/bold #d4a017]"  if vn in notes else ""
            ann_marker = "  [bold #aaaaaa]***[/bold #aaaaaa]" if vn in ann   else ""
            lines.append(f"[bold cyan]{vn:>3}[/bold cyan]{note_icon}  {v['text']}{ann_marker}")
            if vn in notes:
                for nl in notes[vn].splitlines(): lines.append(f"     [italic #d4a017]│ {nl}[/italic #d4a017]")
                lines.append("")
        cw.update("\n".join(lines))
        self.cfg.save({"translation":self.translation,"last_book_id":self.book["bookid"],"last_chapter":self.chapter,"theme":self.biblia_theme})

    @on(ListView.Selected,"#books-list")
    def on_book(self,event):
        if event.item and hasattr(event.item, "book_id"):
            bid = event.item.book_id
            self.book=next((b for b in self.books if b["bookid"]==bid),None)
            if self.book: self._fill_chapters(self.book["chapters"]); self.chapter=1; self.load_scripture(); self.query_one("#chapters-list",ListView).focus()

    @on(ListView.Selected,"#chapters-list")
    def on_chapter(self,_):
        idx=self.query_one("#chapters-list",ListView).index
        if idx is not None: self.chapter=idx+1; self.load_scripture()

    @on(Input.Changed,"#books-filter")
    def filter_books(self,event):
        q=event.value.strip().lower(); bl=self.query_one("#books-list",ListView); bl.clear()
        seen = set()
        for b in self.books:
            bid = b["bookid"]
            if q in b["name"].lower() and bid not in seen:
                seen.add(bid)
                li = ListItem(Label(b["name"]))
                li.book_id = bid
                bl.append(li)

    def action_switch_lang(self): self.push_screen(TranslationModal(),self._on_trans)
    def _on_trans(self,t):
        if t: self.translation=t; self.cfg.save({"translation":t}); self._set_title(); self.load_books()
    def action_cycle_theme(self):
        self.biblia_theme=next_theme(self.biblia_theme); self._set_title(); self.cfg.save({"theme":self.biblia_theme}); self.notify(f"Tema: {LABELS[self.biblia_theme]}",timeout=1.5)
    def action_open_search(self):
        if self.books: self.push_screen(SearchModal(self.translation,self.books),self._on_search)
    def _on_search(self,r):
        if r:
            bid,ch=r; b=next((x for x in self.books if x["bookid"]==bid),None)
            if b: self.book=b; self.chapter=ch; self._fill_chapters(b["chapters"],ch); self.load_scripture()
    def action_toggle_fav(self):
        if not self.book: self.notify("Abre un capítulo primero.",timeout=2); return
        added=fav_toggle(self.translation,self.book["bookid"],self.book["name"],self.chapter)
        self.notify("⭐ Marcado" if added else "★ Eliminado",timeout=2)
        self.query_one("#fav-indicator",Label).update("[bold #d4a017]⭐ Marcado[/bold #d4a017]" if added else "")
    def action_open_favs(self): self.push_screen(FavoritesModal(),self._on_fav)
    def _on_fav(self,fav):
        if fav:
            b=next((x for x in self.books if x["bookid"]==fav["book_id"]),None)
            if b: self.book=b; self.chapter=fav["chapter"]; self._fill_chapters(b["chapters"],fav["chapter"]); self.load_scripture()
    def action_add_note(self):
        if not self.book: self.notify("Abre un capítulo primero.",timeout=2); return
        self.push_screen(_VP(self.book["name"],self.chapter,"✏️  Nota en"),self._open_note)
    def _open_note(self,v):
        if v: self.push_screen(NoteModal(self.translation,self.book["bookid"],self.book["name"],self.chapter,v),lambda c: self.load_scripture() if c else None)
    def action_read_ann(self):
        if not self.book: self.notify("Abre un capítulo primero.",timeout=2); return
        self.push_screen(_VP(self.book["name"],self.chapter,"✦  Ver nota de"),self._open_ann_read)
    def _open_ann_read(self,verse):
        if verse: self._do_read_ann(verse)
    @work
    async def _do_read_ann(self,verse:int):
        ann=await ann_get_chapter(self.translation,self.book["bookid"],self.chapter)
        if verse in ann: self.push_screen(AnnotationReadModal(self.book["name"],self.chapter,verse,ann[verse]))
        else: self.notify(f"No hay nota ✦ en el versículo {verse}.",timeout=2)
    def action_daily(self): self._do_daily()
    @work(exclusive=True)
    async def _do_daily(self):
        if not self.books: return
        self.notify("⏳ Obteniendo lectura litúrgica...", timeout=2)
        try:
            from .daily_reading import get_daily_readings
            from .widgets.daily_selection_modal import DailySelectionModal
            
            readings = await get_daily_readings()
            
            if len(readings) == 1:
                self._apply_daily(readings[0])
            else:
                self.push_screen(DailySelectionModal(readings), self._apply_daily)
                
        except Exception as e:
            self.notify(f"Error lectura: {e}", severity="error")

    def _apply_daily(self, selection):
        if not selection: return
        bid, ch, src = selection["book_id"], selection["chapter"], selection["source"]
        tgt = next((b for b in self.books if b["bookid"]==bid), None)
        if not tgt:
            self.notify(f"Libro {bid} no disponible en esta traducción", severity="error")
            return
            
        self.book=tgt; self.chapter=ch; self._fill_chapters(tgt["chapters"],ch); self.load_scripture()
        self.notify(f"📖 {src}", timeout=3)
    def action_clear_filter(self):
        f=self.query_one("#books-filter",Input)
        if f.value: f.value=""; self.filter_books(Input.Changed(f,""))
        else: self.query_one("#books-list",ListView).focus()

class _VP(ModalScreen):
    DEFAULT_CSS="""
    _VP { align: center middle; }
    #vp-box { width: 46; height: auto; background: $surface; border: thick $primary; padding: 1 2; }
    #vp-title { text-style: bold; color: $accent; text-align: center; width: 100%; margin-bottom: 1; }
    #vp-foot  { height: 3; margin-top: 1; align: right middle; }
    """
    def __init__(self,book_name,chapter,label): super().__init__(); self._label=f"{label} {book_name} {chapter}"
    def compose(self) -> ComposeResult:
        with Vertical(id="vp-box"):
            yield Label(self._label,id="vp-title"); yield Input(placeholder="Número de versículo...",id="vp-input")
            with Horizontal(id="vp-foot"): yield Button("Aceptar",id="vp-ok",variant="primary"); yield Button("Cancelar",id="vp-no")
    def on_mount(self): self.query_one("#vp-input",Input).focus()
    @on(Button.Pressed,"#vp-ok")
    @on(Input.Submitted,"#vp-input")
    def accept(self,_=None):
        val=self.query_one("#vp-input",Input).value.strip(); self.dismiss(int(val) if val.isdigit() else None)
    @on(Button.Pressed,"#vp-no")
    def cancel(self): self.dismiss(None)

def main(): BibliaApp().run()