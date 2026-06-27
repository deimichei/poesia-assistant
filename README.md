# Assistente di scrittura poetica

Un'applicazione che, mentre scrivi una poesia, ti suggerisce citazioni dai grandi
poeti contenenti le parole che stai usando — come ispirazione alla scrittura.

Mentre digiti nel pannello di sinistra, a destra appaiono estratti dai testi di
riferimento che contengono l'ultima parola scritta, raggruppati per autore ed
evidenziati.

## Come funziona

- **Corpus**: legge i PDF nella cartella `pdf_riferimento/` ed estrae il testo.
- **Ricerca**: cerca la parola digitata (match parziale, es. "amor" trova
  "amore", "amorosa") e mostra ~10 parole di contesto attorno a ogni occorrenza.
- **Interfaccia**: split-layout in Streamlit — scrittura a sinistra, suggerimenti
  a destra, raggruppati per autore con un'opzione per vedere tutti i risultati.

## Struttura del progetto

- `corpus.py` — legge i PDF e costruisce il corpus (testo + fonte per ciascun file)
- `ricerca.py` — la logica di ricerca con match parziale ed evidenziazione
- `app.py` — l'interfaccia Streamlit
- `pdf_riferimento/` — i testi di riferimento in PDF (non inclusi nel repository)

## Requisiti

- [uv](https://docs.astral.sh/uv/) (gestisce ambiente e dipendenze)
- Python 3.13 (gestito da uv)

## Installazione

git clone <url-del-repository>

cd poesia-assistant

uv sync

## I testi di riferimento

I PDF dei testi **non sono inclusi** nel repository (per ragioni di copyright).
Per usare l'app, crea la cartella `pdf_riferimento/` e mettici i tuoi PDF di
poesia, con nomi nello schema `autore_titolo.pdf` (es. `dante_vita-nova.pdf`).
La fonte mostrata nei suggerimenti viene ricavata automaticamente dal nome del file.

Usa preferibilmente testi di dominio pubblico.

## Avvio

uv run streamlit run app.py


L'app si apre nel browser. Per fermarla, premi `Ctrl+C` nel terminale.