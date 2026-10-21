import streamlit as st
from corpus import costruisci_corpus
from ricerca import cerca

# Quanti risultati mostrare per autore prima del bottone "mostra tutti"
LIMITE_VISIBILE = 5

# --- Configurazione pagina ---
st.set_page_config(page_title="Assistente Poesia", layout="wide")

# --- Carichiamo il corpus UNA volta sola (con cache) ---
@st.cache_data
def carica_corpus():
    return costruisci_corpus()

corpus = carica_corpus()

# --- Titolo ---
st.title("Assistente di scrittura poetica")

# --- Due colonne: sinistra (scrittura) e destra (suggerimenti) ---
col_sinistra, col_destra = st.columns(2)

with col_sinistra:
    st.subheader("La tua poesia")
    testo_utente = st.text_area(
        "Scrivi qui:",
        height=400,
        placeholder="Inizia a scrivere...",
        label_visibility="collapsed",
    )

with col_destra:
    st.subheader("Suggerimenti dai poeti")

    # Prendiamo l'ultima parola che l'utente sta scrivendo
    parole = testo_utente.split()
    ultima_parola = parole[-1] if parole else ""

    if len(ultima_parola) < 3:
        st.info("Scrivi almeno 3 lettere per vedere i suggerimenti.")
    else:
        risultati = cerca(ultima_parola, corpus)

        if not risultati:
            st.write(f"Nessun risultato per '{ultima_parola}'.")
        else:
            # Una sezione per autore, una sotto l'altra
            for fonte, estratti in risultati.items():
                st.markdown(f"**{fonte}** ({len(estratti)} risultati)")

                # Mostriamo i primi LIMITE_VISIBILE
                for estratto in estratti[:LIMITE_VISIBILE]:
                    st.markdown(f"{estratto}", unsafe_allow_html=True)

                # Se ce ne sono di più, bottone per vederli tutti
                if len(estratti) > LIMITE_VISIBILE:
                    with st.expander(f"Mostra gli altri {len(estratti) - LIMITE_VISIBILE} risultati"):
                        for estratto in estratti[LIMITE_VISIBILE:]:
                            st.markdown(f"{estratto}", unsafe_allow_html=True)

                st.divider()