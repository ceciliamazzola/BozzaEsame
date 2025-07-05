import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os
import base64
# ----------------------
# Page Configuration
# ----------------------
st.set_page_config(
    page_title="PLAYER CAREER",
    layout="wide"
)

# 🌐 Tema chiaro personalizzato
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@600&display=swap" rel="stylesheet">
    <style>
        .stApp { background-color: #f7f7f7; }
        h1 { font-family: 'Orbitron', sans-serif !important; color: #f45208 !important; font-size: 2.5rem !important; }
        .streamlit-expanderHeader, .css-18e3th9, .css-10trblm { color: #333 !important; }
        .css-1d391kg hr { border-color: #ccc !important; }
        label, .stSelectbox label { color: #000 !important; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)


# Bottone indietro
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
            cursor: pointer;">
            ⬅️ Back to Menu
        </button>
    </form>
""", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)  # Una riga vuota
# ----------------------
# Data Loading
# ----------------------
@st.cache_data

def load_data(path: str):
    df = pd.read_csv(path)
    df = df[df['season'] >= 2000].copy()

    df['fg_mul'] = df['fg_percent'] * df['g']
    df['ft_mul'] = df['ft_percent'] * df['g']

    games_df = df.groupby('player_x', as_index=False).agg(TotalGames=('g','sum'))

    fg_df = df.groupby('player_x', as_index=False).agg(
        FGSum=('fg_mul','sum'),
        Games=('g','sum')
    )
    fg_df['FG%'] = fg_df['FGSum'] / fg_df['Games'] * 100

    pct_df = (
        df.drop_duplicates('player_x')
          .loc[:, ['player_x','career_x2p_percent','career_x3p_percent','career_ft_percent','career_e_fg_percent']]
          .rename(columns={
              'career_x2p_percent':'2P%',
              'career_x3p_percent':'3P%',
              'career_ft_percent':'FT%',
              'career_e_fg_percent':'eFG%'
          })
    )

    pg_df = (
        df.drop_duplicates('player_x')
          .loc[:, ['player_x','career_pts_per_g','career_trb_per_g',
                   'career_ast_per_g','career_tov_per_g','career_orb','career_drb']]
          .rename(columns={
              'career_pts_per_g':'PTS/G',
              'career_trb_per_g':'TRB/G',
              'career_ast_per_g':'AST/G',
              'career_tov_per_g':'TOV/G',
              'career_orb':'ORB',
              'career_drb':'DRB'
          })
    )

    career_df = fg_df.merge(pct_df, on='player_x').merge(pg_df, on='player_x')
    career_df = career_df.merge(games_df, on='player_x')
    career_df['ORB/G'] = career_df['ORB'] / career_df['TotalGames']
    career_df['DRB/G'] = career_df['DRB'] / career_df['TotalGames']

    career_df = career_df.rename(columns={'player_x':'player'})
    career_df = career_df.drop(columns=['FGSum','Games','TotalGames','ORB','DRB'])

    return career_df

career_df = load_data('Player Final.csv')

# ----------------------
# Title and Selector
# ----------------------
st.markdown("""
    <div style='font-family: Orbitron, sans-serif; font-size: 2.5rem; font-weight: 700; color: #f45208; text-align: center; margin-bottom: 0.5rem;'>
        PLAYER CAREER
    </div>
""", unsafe_allow_html=True)
# ----------------------
# Subtitle
# ----------------------
st.markdown("""
    <div style='font-family: Orbitron, sans-serif; font-size: 1.1rem; color: #333; text-align: center; margin-bottom: 2rem;'>
        Analyze each player’s career performance compared to NBA league averages across multiple metrics
    </div>
""", unsafe_allow_html=True)

# Player selector
st.markdown("<label style='color: black; font-weight: bold;'>Select a player:</label>", unsafe_allow_html=True)
players = sorted(career_df['player'].unique())
selected_player = st.selectbox("", options=players, index=players.index("LeBron James") if "LeBron James" in players else 0)

# ----------------------
# Player Image
# ----------------------
# ----------------------
# Player Image (Centered)
# ----------------------
img_file = None
for ext in ['png', 'jpg', 'jpeg']:
    candidate = f"{selected_player}.{ext}"
    if os.path.isfile(candidate):
        img_file = candidate
        break

if not img_file:
    try:
        last, first = selected_player.split(", ")
        base_name = f"{first}_{last}".replace(" ", "_")
    except:
        base_name = selected_player.replace(" ", "_")

    for ext in ['png', 'jpg', 'jpeg']:
        candidate = f"images/{base_name}.{ext}"
        if os.path.isfile(candidate):
            img_file = candidate
            break

# Mostra immagine centrata o testo centrato
# ----------------------
# Player Image (Perfectly Centered)
# ----------------------
center_container = st.container()

with center_container:
    if img_file:
        st.markdown(f"""
            <div style='text-align: center;'>
                <img src='data:image/png;base64,{base64.b64encode(open(img_file, "rb").read()).decode()}' 
                     width='250' style='margin-bottom: 8px;'/>
                <div style='font-size: 18px; color: black; font-weight: bold;'>{selected_player}</div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style='text-align: center; color: black; font-size: 16px; margin-top: 10px;'>
                Photo not available for the selected player.
            </div>
        """, unsafe_allow_html=True)

# ----------------------
# Radar Charts
# ----------------------
# ----------------------
# Radar Charts with Orbitron Font in Titles

# ----------------------
st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    perc_metrics = ['FG%','2P%','3P%','FT%','eFG%']
    player_perc = career_df.loc[career_df['player']==selected_player, perc_metrics].iloc[0]
    league_avg_perc = career_df[perc_metrics].mean()
    radar_perc = pd.DataFrame({
        'Metric': perc_metrics*2,
        'Value': list(player_perc) + list(league_avg_perc),
        'Group': [selected_player]*len(perc_metrics) + ['NBA Avg']*len(perc_metrics)
    })
    fig_perc = px.line_polar(
        radar_perc,
        r='Value',
        theta='Metric',
        color='Group',
        line_close=True,
        labels={'Group': 'Legend'}
    )
    fig_perc.update_layout(
        title=dict(
            text="Shooting % vs NBA Avg",
            x=0,
            xanchor="left",
            font=dict(family="Orbitron, sans-serif", size=22, color="black")
        ),
        plot_bgcolor="#f7f7f7",
        paper_bgcolor="#f7f7f7",
        font=dict(family="Orbitron, sans-serif", size=16, color='black'),
        polar=dict(
            radialaxis=dict(tickfont=dict(size=14, color='black')),
            angularaxis=dict(tickfont=dict(size=14, color='black'))
        ),
        legend=dict(font=dict(size=14, color='black'), title_font=dict(size=14, color='black'))
    )
    st.plotly_chart(fig_perc, use_container_width=True)

with col2:
    pg_metrics = ['PTS/G','TRB/G','AST/G','TOV/G','ORB/G','DRB/G']
    player_pg = career_df.loc[career_df['player']==selected_player, pg_metrics].iloc[0]
    league_avg_pg = career_df[pg_metrics].mean()
    radar_pg = pd.DataFrame({
        'Metric': pg_metrics*2,
        'Value': list(player_pg) + list(league_avg_pg),
        'Group': [selected_player]*len(pg_metrics) + ['NBA Avg']*len(pg_metrics)
    })
    fig_pg = px.line_polar(
        radar_pg,
        r='Value',
        theta='Metric',
        color='Group',
        line_close=True,
        labels={'Group': 'Legend'}
    )
    fig_pg.update_layout(
        title=dict(
            text="Per Game Stats vs NBA Avg",
            x=0,
            xanchor="left",
            font=dict(family="Orbitron, sans-serif", size=22, color="black")
        ),
        plot_bgcolor="#f7f7f7",
        paper_bgcolor="#f7f7f7",
        font=dict(family="Orbitron, sans-serif", size=16, color='black'),
        polar=dict(
            radialaxis=dict(tickfont=dict(size=14, color='black')),
            angularaxis=dict(tickfont=dict(size=14, color='black'))
        ),
        legend=dict(font=dict(size=14, color='black'), title_font=dict(size=14, color='black'))
    )
    st.plotly_chart(fig_pg, use_container_width=True)


# … codice precedente ai radar …
from pathlib import Path

current_dir = Path(__file__).parent
logo_dir = current_dir.parent / "logos"

# Carico di nuovo il raw dataframe (non solo career_df), per poter pescare le stagioni
@st.cache_data
def load_raw(path: str):
    return pd.read_csv(path)

raw_df = load_raw('Player Final.csv')

# Dropdown per la stagione, filtrata in base al giocatore selezionato
available_seasons = (
    raw_df[raw_df['player_x'] == selected_player]['season']
    .dropna()
    .astype(int)
    .sort_values(ascending=False)
    .unique()
)

st.markdown("---")
st.markdown("""
    <h3 style="color: black; font-family: 'Orbitron', sans-serif; margin-top: 2rem;">
        Season Stats
    </h3>
""", unsafe_allow_html=True)

selected_season = st.selectbox("Pick a season:", available_seasons)

# Recupero i dati di quella stagione
season_row = raw_df[
    (raw_df['player_x'] == selected_player) &
    (raw_df['season'] == selected_season)
].iloc[0]

# Preparo le metriche
season_stats = {
    "Team": season_row["tm"],
    "G (Games)": int(season_row["g"]),
    "MPG": round(season_row["mp"] / season_row["g"], 1),
    "PPG": round(season_row["pts"] / season_row["g"], 1),
    "RPG": round(season_row["trb"] / season_row["g"], 1),
    "APG": round(season_row["ast"] / season_row["g"], 1),
    "SPG": round(season_row["stl"] / season_row["g"], 1),
    "BPG": round(season_row["blk"] / season_row["g"], 1),
    "TO/G": round(season_row["tov"] / season_row["g"], 1),
    "FG%": round(season_row["fg_percent"] * 100, 1),
    "3P%": round(season_row["x3p_percent"] * 100, 1),
    "FT%": round(season_row["ft_percent"] * 100, 1),
}

# CSS custom
st.markdown("""
    <style>
    .stat-card {
        background: #f7f9fc;
        border-left: 4px solid #ff4500;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 12px;
        text-align: center;
    }
    .stat-label { color: #555; font-size: 0.9rem; }
    .stat-value { color: #1f2c56; font-size: 1.8rem; font-weight: bold; }
    .team-logo { margin-bottom: 8px; height: 50px; }
    </style>
""", unsafe_allow_html=True)
# CSS per grid e card armoniche
st.markdown("""
    <style>
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 16px;
        margin-top: 16px;
    }
    .stat-card {
        background: #f7f9fc;
        border-left: 4px solid #ff4500;
        border-radius: 8px;
        padding: 16px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 160px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .stat-label {
        color: #555;
        font-size: 0.9rem;
        margin-top: 8px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .stat-value {
        color: #1f2c56;
        font-size: 1.8rem;
        font-weight: bold;
        margin-top: 4px;
    }
    .team-logo {
        height: 50px;
        margin-bottom: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# Genera l’HTML della grid con data-URI per i loghi
cards_html = '<div class="stats-grid">'
for label, value in season_stats.items():
    cards_html += '<div class="stat-card">'
    if label == "Team":
        # cerco il file logo
        logo_path, logo_ext = None, None
        for ext in ("png", "jpg", "jpeg"):
            candidate = logo_dir / f"{value}.{ext}"
            if candidate.is_file():
                logo_path, logo_ext = candidate, ext
                break

        if logo_path:
            # leggo e converto in base64
            with open(logo_path, "rb") as f:
                data = f.read()
            b64 = base64.b64encode(data).decode()
            mime = "jpeg" if logo_ext in ("jpg","jpeg") else "png"
            cards_html += f'<img src="data:image/{mime};base64,{b64}" class="team-logo" alt="{value} logo">'
        cards_html += f'<div class="stat-value">{value}</div>'
        cards_html += '<div class="stat-label">Team</div>'

    else:
        cards_html += f'<div class="stat-value">{value}</div>'
        cards_html += f'<div class="stat-label">{label}</div>'

    cards_html += '</div>'
cards_html += '</div>'

st.markdown(cards_html, unsafe_allow_html=True)