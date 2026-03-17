import unicodedata
from .api.bolls_client import PT_CODES

def _n(s):
    return "".join(c for c in unicodedata.normalize("NFD",s.lower()) if unicodedata.category(c)!="Mn")

BOOKS = [
    (1,"Génesis","Gênesis",50),(2,"Éxodo","Êxodo",40),(3,"Levítico","Levítico",27),
    (4,"Números","Números",36),(5,"Deuteronomio","Deuteronômio",34),(6,"Josué","Josué",24),
    (7,"Jueces","Juízes",21),(8,"Rut","Rute",4),(9,"1 Samuel","1 Samuel",31),
    (10,"2 Samuel","2 Samuel",24),(11,"1 Reyes","1 Reis",22),(12,"2 Reyes","2 Reis",25),
    (13,"1 Crónicas","1 Crônicas",29),(14,"2 Crónicas","2 Crônicas",36),
    (15,"Esdras","Esdras",10),(16,"Nehemías","Neemias",13),(17,"Ester","Ester",10),
    (18,"Job","Jó",42),(19,"Salmos","Salmos",150),(20,"Proverbios","Provérbios",31),
    (21,"Eclesiastés","Eclesiastes",12),(22,"Cantares","Cantares",8),
    (23,"Isaías","Isaías",66),(24,"Jeremías","Jeremias",52),
    (25,"Lamentaciones","Lamentações",5),(26,"Ezequiel","Ezequiel",48),
    (27,"Daniel","Daniel",12),(28,"Oseas","Oséias",14),(29,"Joel","Joel",3),
    (30,"Amós","Amós",9),(31,"Abdías","Obadias",1),(32,"Jonás","Jonas",4),
    (33,"Miqueas","Miquéias",7),(34,"Nahúm","Naum",3),(35,"Habacuc","Habacuque",3),
    (36,"Sofonías","Sofonias",3),(37,"Hageo","Ageu",2),(38,"Zacarías","Zacarias",14),
    (39,"Malaquías","Malaquias",4),(40,"Mateo","Mateus",28),(41,"Marcos","Marcos",16),
    (42,"Lucas","Lucas",24),(43,"Juan","João",21),(44,"Hechos","Atos",28),
    (45,"Romanos","Romanos",16),(46,"1 Corintios","1 Coríntios",16),
    (47,"2 Corintios","2 Coríntios",13),(48,"Gálatas","Gálatas",6),
    (49,"Efesios","Efésios",6),(50,"Filipenses","Filipenses",4),
    (51,"Colosenses","Colossenses",4),(52,"1 Tesalonicenses","1 Tessalonicenses",5),
    (53,"2 Tesalonicenses","2 Tessalonicenses",3),(54,"1 Timoteo","1 Timóteo",6),
    (55,"2 Timoteo","2 Timóteo",4),(56,"Tito","Tito",3),(57,"Filemón","Filemom",1),
    (58,"Hebreos","Hebreus",13),(59,"Santiago","Tiago",5),(60,"1 Pedro","1 Pedro",5),
    (61,"2 Pedro","2 Pedro",3),(62,"1 Juan","1 João",5),(63,"2 Juan","2 João",1),
    (64,"3 Juan","3 João",1),(65,"Judas","Judas",1),(66,"Apocalipsis","Apocalipse",22),
]

def get_books_for_lang(lang):
    return [{"bookid":b,"name":es if lang=="es" else pt,"chapters":ch} for b,es,pt,ch in BOOKS]

def lang_for_translation(code):
    return "pt" if code in PT_CODES else "es"

_ES, _PT = {}, {}
for _bid,_nes,_npt,_ in BOOKS:
    _ES[_n(_nes)]=_bid; _PT[_n(_npt)]=_bid

_ES.update({"gn":1,"gen":1,"ex":2,"lv":3,"lev":3,"nm":4,"num":4,"dt":5,"jos":6,"jue":7,"rt":8,
    "1sm":9,"1sa":9,"2sm":10,"2sa":10,"1re":11,"2re":12,"1cr":13,"2cr":14,"esd":15,"ne":16,
    "neh":16,"est":17,"jb":18,"sal":19,"sl":19,"ps":19,"pr":20,"prov":20,"ec":21,"ecl":21,
    "ct":22,"is":23,"isa":23,"jr":24,"jer":24,"lm":25,"ez":26,"dn":27,"dan":27,"os":28,
    "jl":29,"am":30,"ab":31,"jon":32,"mi":33,"na":34,"hab":35,"sof":36,"sf":36,"hag":37,
    "zac":38,"mal":39,"mt":40,"mc":41,"mr":41,"lc":42,"jn":43,"hch":44,"act":44,"ro":45,
    "rom":45,"1co":46,"2co":47,"gl":48,"ga":48,"ef":49,"fp":50,"col":51,"1ts":52,"2ts":53,
    "1tm":54,"1ti":54,"2tm":55,"2ti":55,"tt":56,"flm":57,"he":58,"heb":58,"stg":59,"sg":59,
    "1pe":60,"2pe":61,"1jn":62,"1j":62,"2jn":63,"3jn":64,"jud":65,"ap":66,"apoc":66})
_PT.update({"gn":1,"ex":2,"lv":3,"nm":4,"dt":5,"js":6,"jz":7,"rt":8,"1sm":9,"2sm":10,
    "1rs":11,"2rs":12,"1cr":13,"2cr":14,"ed":15,"ne":16,"et":17,"sl":19,"pv":20,"ec":21,
    "ct":22,"is":23,"jr":24,"lm":25,"ez":26,"dn":27,"os":28,"jl":29,"am":30,"ob":31,
    "mq":33,"na":34,"hc":35,"sf":36,"ag":37,"zc":38,"ml":39,"mt":40,"mc":41,"lc":42,
    "jo":43,"at":44,"rm":45,"1co":46,"2co":47,"gl":48,"ef":49,"fp":50,"cl":51,"1ts":52,
    "2ts":53,"1tm":54,"2tm":55,"tt":56,"fm":57,"hb":58,"tg":59,"1pe":60,"2pe":61,
    "1jo":62,"2jo":63,"3jo":64,"jd":65,"ap":66})

_EN = {"gn":1,"gen":1,"ex":2,"lv":3,"lev":3,"nm":4,"num":4,"dt":5,"jos":6,"jue":7,"rt":8,
    "1sm":9,"1sa":9,"2sm":10,"2sa":10,"1re":11,"2re":12,"1cr":13,"2cr":14,"esd":15,"ne":16,
    "est":17,"jb":18,"sal":19,"sl":19,"ps":19,"pr":20,"prov":20,"ec":21,"ecl":21,
    "ct":22,"is":23,"isa":23,"jr":24,"jer":24,"lm":25,"ez":26,"dn":27,"dan":27,"os":28,
    "jl":29,"am":30,"ab":31,"jon":32,"mi":33,"na":34,"hab":35,"sof":36,"sf":36,"hag":37,
    "zac":38,"mal":39,"mt":40,"mc":41,"mr":41,"lc":42,"jn":43,"hch":44,"act":44,"ro":45,
    "rom":45,"1co":46,"2co":47,"gl":48,"ga":48,"ef":49,"fp":50,"col":51,"1ts":52,"2ts":53,
    "1tm":54,"1ti":54,"2tm":55,"2ti":55,"tt":56,"flm":57,"he":58,"heb":58,"stg":59,"sg":59,
    "1pe":60,"2pe":61,"1jn":62,"1j":62,"2jn":63,"3jn":64,"jud":65,"ap":66,"apoc":66,
    "genesis":1,"exodus":2,"leviticus":3,"numbers":4,"deuteronomy":5,"joshua":6,"judges":7,"ruth":8,
    "1 samuel":9,"2 samuel":10,"1 kings":11,"2 kings":12,"1 chronicles":13,"2 chronicles":14,
    "ezra":15,"nehemiah":16,"esther":17,"job":18,"psalms":19,"proverbs":20,"ecclesiastes":21,
    "song of songs":22,"isaiah":23,"jeremiah":24,"lamentations":25,"ezekiel":26,"daniel":27,
    "hosea":28,"joel":29,"amos":30,"obadiah":31,"jonah":32,"micah":33,"nahum":34,"habakkuk":35,
    "zephaniah":36,"haggai":37,"zechariah":38,"malachi":39,"matthew":40,"mark":41,"luke":42,
    "john":43,"acts":44,"romans":45,"1 corinthians":46,"2 corinthians":47,"galatians":48,
    "ephesians":49,"philippians":50,"colossians":51,"1 thessalonians":52,"2 thessalonians":53,
    "1 timothy":54,"2 timothy":55,"titus":56,"philemon":57,"hebrews":58,"james":59,"1 peter":60,
    "2 peter":61,"1 john":62,"2 john":63,"3 john":64,"jude":65,"revelation":66}

def resolve_book(name, lang="es"):
    n = _n(name.strip())
    if lang == "es": return _ES.get(n) or _EN.get(n)
    if lang == "pt": return _PT.get(n) or _EN.get(n)
    return _EN.get(n)