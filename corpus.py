import re
from pathlib import Path

from pypdf import PdfReader

# Estensioni dei file letti dalla cartella dei testi di riferimento
ESTENSIONI = (".pdf", ".txt")


def nome_fonte(percorso):
    """Ricava un nome leggibile della fonte dal nome del file.
    Es: 'dante_vita-nova.pdf' -> 'Dante - Vita nova'
    """
    nome = Path(percorso).stem              # toglie cartella ed estensione -> 'dante_vita-nova'
    autore, _, opera = nome.partition("_")  # divide su '_' -> 'dante' e 'vita-nova'
    autore = autore.replace("-", " ").capitalize()
    opera = opera.replace("-", " ").capitalize()
    return f"{autore} - {opera}" if opera else autore


def leggi_pdf(percorso_pdf):
    """Legge tutto il testo di un PDF e lo restituisce come un'unica stringa."""
    reader = PdfReader(percorso_pdf)
    return "\n".join((pagina.extract_text() or "") for pagina in reader.pages)


def leggi_txt(percorso_txt):
    """Legge un file di testo. Per gli eBook di Project Gutenberg toglie
    intestazione e licenza e ricava autore e titolo dai metadati.
    Restituisce (testo, fonte); fonte è None se non ricavabile dal file."""
    testo = Path(percorso_txt).read_text(encoding="utf-8", errors="replace")
    fonte = None

    titolo = re.search(r"^Title:\s*(.+)$", testo, re.MULTILINE)
    autore = re.search(r"^Author:\s*(.+)$", testo, re.MULTILINE)
    if titolo and autore:
        cognome = autore.group(1).strip().split()[-1]  # stesso stile dei PDF: "Blake - ..."
        fonte = f"{cognome} - {titolo.group(1).strip()}"

    inizio = re.search(r"^\*\*\* ?START OF (THE|THIS) PROJECT GUTENBERG.*$", testo, re.MULTILINE)
    fine = re.search(r"^\*\*\* ?END OF (THE|THIS) PROJECT GUTENBERG.*$", testo, re.MULTILINE)
    if inizio:
        testo = testo[inizio.end():fine.start() if fine else len(testo)]
    return testo, fonte


def pulisci(testo):
    """Toglie i residui tipici dell'estrazione da PDF."""
    testo = re.sub(r"(\w)[-­]\s*\n\s*(\w)", r"\1\2", testo)       # parole divise a fine riga
    testo = re.sub(r"(\w)- (?=[a-zà-ù])", r"\1", testo)                 # "spin- gendosi" -> "spingendosi"
    testo = re.sub(r"(https?://|www\.)\S+", " ", testo)                 # indirizzi web
    testo = re.sub(r"^\s*\d{1,4}\s*$", " ", testo, flags=re.MULTILINE)  # righe con solo il numero di pagina
    testo = re.sub(r"\[\d+\]", " ", testo)                              # rimandi alle note tipo [12]
    return testo


def costruisci_corpus(cartella="pdf_riferimento"):
    """Legge tutti i PDF e TXT nella cartella e restituisce una lista di blocchi {testo, fonte}."""
    corpus = []
    for percorso in sorted(Path(cartella).iterdir()):
        estensione = percorso.suffix.lower()
        if estensione not in ESTENSIONI:
            continue
        if estensione == ".pdf":
            testo, fonte = leggi_pdf(percorso), None
        else:
            testo, fonte = leggi_txt(percorso)
        corpus.append({
            "testo": pulisci(testo),
            "fonte": fonte or nome_fonte(percorso),
        })
    return corpus


# --- Test ---
if __name__ == "__main__":
    corpus = costruisci_corpus()
    print(f"Blocchi nel corpus: {len(corpus)}\n")
    for blocco in corpus:
        n_caratteri = len(blocco["testo"])
        print(f"Fonte: {blocco['fonte']:<45} | caratteri: {n_caratteri}")
