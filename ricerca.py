def cerca(parola, corpus, parole_contesto=10):
    """Cerca 'parola' (match parziale) in tutti i blocchi del corpus.
    Restituisce un dizionario {fonte: [lista di estratti]} con TUTTI i risultati.
    Il limite di visualizzazione lo gestisce l'interfaccia.
    """
    parola = parola.lower().strip()
    risultati_per_fonte = {}

    if not parola:  # se il campo è vuoto, niente ricerca
        return risultati_per_fonte

    for blocco in corpus:
        testo = blocco["testo"]
        fonte = blocco["fonte"]
        parole = testo.split()

        trovati = []
        for i, p in enumerate(parole):
            if parola in p.lower():
                inizio = max(0, i - parole_contesto)
                fine = min(len(parole), i + parole_contesto + 1)

                prima = " ".join(parole[inizio:i])
                trovata = parole[i]
                dopo = " ".join(parole[i+1:fine])

                trovata_evidenziata = f"<mark style='background-color:#fff176'>{trovata}</mark>"
                estratto = f"{prima} {trovata_evidenziata} {dopo}".strip()
                trovati.append(estratto)

        if trovati:  # aggiungiamo la fonte solo se ha almeno un risultato
            risultati_per_fonte[fonte] = trovati

    return risultati_per_fonte


# --- Test ---
if __name__ == "__main__":
    from corpus import costruisci_corpus

    print("Costruisco il corpus...")
    corpus = costruisci_corpus()

    parola_test = "amor"
    print(f"\nCerco: '{parola_test}'\n")

    risultati = cerca(parola_test, corpus)
    for fonte, estratti in risultati.items():
        print(f"\n===== {fonte}: {len(estratti)} risultati =====")
        # nel test mostriamo solo i primi 3 per autore, per non riempire lo schermo
        for estratto in estratti[:3]:
            print(f"  • {estratto}")