import streamlit as st

# Applica font Orbitron e stile globale petrolio + testo bianco
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@600&display=swap" rel="stylesheet">
    <style>
        .stApp {
            background-color: #2f6974 !important;
        }

        div, p, span, label {
            color: #ffffff !important;
        }

        input {
            background-color: #2f6974 !important;
            color: #ffffff !important;
            border: 1px solid #ffffff !important;
        }

        h3 {
            font-family: 'Orbitron', sans-serif !important;
            color: #f45208 !important;
        }

        .info-box {
            background-color: #2f6974;
            padding: 20px;
            border-radius: 10px;
            color: white;
            font-family: 'Arial', sans-serif;
        }
    </style>
""", unsafe_allow_html=True)

# Box informativo con stile coerente
st.markdown("""
<div class="info-box">
    <h3>📌 Project Information</h3>
    <p>
        Questo progetto è stato sviluppato nell’ambito di un corso di laurea del 
        <strong>Politecnico di Milano</strong>. I dati utilizzati provengono dai siti ufficiali della 
        <strong>NBA</strong> e sono stati impiegati esclusivamente per finalità didattiche e di ricerca.
    </p>
    <p>
        Di seguito sono riportati i contatti dei membri del team di sviluppo.
    </p>
    <p>
        Cecilia Mazzola: cecilia.mazzola@mail.polimi.it<br>
        Filippo Toniolo: filippo.toniolo@mail.polimi.it
    </p>
</div>
""", unsafe_allow_html=True)
