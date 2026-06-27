from pypdf import PdfReader
from pathlib import Path


def nome_fonte(percorso_pdf):
    """Ricava un nome leggibile della fonte dal nome del file.
    Es: 'dante_vita-nova.pdf' -> 'Dante - Vita nova'
    """
    nome = Path(percorso_pdf).stem          # toglie cartella ed estensione -> 'dante_vita-nova'
    autore, _, opera = nome.partition("_")  # divide su '_' -> 'dante' e 'vita-nova'
    autore = autore.capitalize()            # 'dante' -> 'Dante'
    opera = opera.replace("-", " ").capitalize()  # 'vita-nova' -> 'Vita nova'
    return f"{autore} - {opera}"


def leggi_pdf(percorso_pdf):
    """Legge tutto il testo di un PDF e lo restituisce come un'unica stringa."""
    reader = PdfReader(percorso_pdf)
    pagine_testo = []
    for pagina in reader.pages:
        pagine_testo.append(pagina.extract_text())
    return "\n".join(pagine_testo)


def costruisci_corpus(cartella="pdf_riferimento"):
    """Legge tutti i PDF nella cartella e restituisce una lista di blocchi {testo, fonte}."""
    corpus = []
    cartella_pdf = Path(cartella)
    for percorso_pdf in sorted(cartella_pdf.glob("*.pdf")):
        blocco = {
            "testo": leggi_pdf(percorso_pdf),
            "fonte": nome_fonte(percorso_pdf),
        }
        corpus.append(blocco)
    return corpus


# --- Test ---
if __name__ == "__main__":
    corpus = costruisci_corpus()
    print(f"Blocchi nel corpus: {len(corpus)}\n")
    for blocco in corpus:
        n_caratteri = len(blocco["testo"])
        print(f"Fonte: {blocco['fonte']:<30} | caratteri: {n_caratteri}")