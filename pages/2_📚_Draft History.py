import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from matplotlib.ticker import MaxNLocator
from PIL import Image

# 🌐 Tema chiaro e stile minimal
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@600&display=swap" rel="stylesheet">
    <style>
        /* Sfondo chiaro dell'app */
        .stApp {
            background-color: #f7f7f7;
        }
        /* Titolo principale */
        h1 {
            font-family: 'Orbitron', sans-serif !important;
            color: #f45208 !important;
            font-size: 2.5rem !important;
        }
        /* Testi generali */
        .streamlit-expanderHeader, .css-18e3th9, .css-10trblm {
            color: #333333 !important;
        }
        /* Separatori più delicati */
        .css-1d391kg hr {
            border-color: #cccccc !important;
        }
    </style>
""", unsafe_allow_html=True)

# Titolo e sottotitolo
st.title("📚 Draft History & Trend")
st.write("Explore historical draft trends and discover every pick year by year.")

# Pulsante per tornare alla home
st.markdown("""
    <form action="/" method="get">
        <button type="submit" style="
            padding: 10px 20px;
            background-color: #f45208;
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: bold;
            font-size: 16px;
            font-family: 'Orbitron', sans-serif;
            cursor: pointer;
            transition: background-color 0.3s ease;">
            ⬅️ Back to Menu
        </button>
    </form>
""", unsafe_allow_html=True)

# Caricamento dati e selezione
try:
    df = pd.read_csv("/workspaces/BozzaEsame/draft_history_fin.csv")
    years = df["Year"].unique().astype(int)
    year = st.selectbox("Select a year", sorted(years))

    filtered_by_year = df[df["Year"] == year]
    round_options = sorted(filtered_by_year["Round Number"].dropna().unique().astype(int))
    round_selected = st.selectbox("Select a Round", round_options, index=0)

    filtered = (
        filtered_by_year[filtered_by_year["Round Number"] == round_selected]
        .drop(columns=["Unnamed: 0", "Round.1"], errors="ignore")
        .sort_values("Overall Pick")
    )

    st.subheader(f"Draft {year} - Round {round_selected}")
    logo_folder = Path("/workspaces/BozzaEsame/logos")

    def find_logo(abbrev):
        for ext in [".png", ".jpg", ".jpeg", ".svg"]:
            p = logo_folder / f"{abbrev}{ext}"
            if p.exists():
                return p
        return None

    for _, r in filtered.iterrows():
        col1, col2, col3 = st.columns([1, 4, 2])

        # 1) Numero di pick (solo testo, font scuro)
        col1.markdown(f"""
            <div style="
                text-align: center;
                font-size:24px;
                color:#333333;
                font-weight:bold;
            ">
                {r['Overall Pick']}
            </div>
        """, unsafe_allow_html=True)

        # 2) Nome e round (solo testo, colore scuro)
        col2.markdown(f"""
            <div style="padding: 4px 8px;">
                <div style="font-size:18px; font-weight:bold; color: #222222;">
                    {r['Player']}
                </div>
                <div style="font-size:14px; color: #555555;">
                    {int(r['Round Number'])}° Round, Pick {int(r['Round Pick'])}
                </div>
            </div>
        """, unsafe_allow_html=True)

        # 3) Logo mantenendo proporzioni
        logo_path = find_logo(r["Team Abbreviation"])
        if logo_path:
            img = Image.open(logo_path)
            img.thumbnail((80, 80), Image.LANCZOS)
            col3.image(img, use_container_width=False)

        else:
            col3.markdown(f"""
                <div style="
                    text-align: center;
                    font-size:16px;
                    color:#333333;
                    padding-top:12px;
                ">
                    {r['Team Abbreviation']}
                </div>
            """, unsafe_allow_html=True)

        # Separatore più delicato
        st.markdown("""<hr style="border-color: #cccccc; margin:10px 0;">""",
                    unsafe_allow_html=True)

except Exception as e:
    st.error(f"An error occurred: {e}")
