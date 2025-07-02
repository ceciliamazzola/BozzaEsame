import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
from sklearn.preprocessing import MinMaxScaler

st.set_page_config(page_title="Player Profiling - Next Gen Draft")

# Stile coerente con la homepage
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@800&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary-color: #f45208;
            --secondary-color: #2f6974;
            --text-color: white;
        }
        .title-custom {
            font-family: 'Orbitron', sans-serif;
            font-weight: 800;
            font-size: 3.5rem;
            color: var(--primary-color);
            -webkit-text-stroke: 2px var(--text-color);
            text-shadow: 3px 3px 8px rgba(0,0,0,0.3);
            text-align: center;
            margin-bottom: 1rem;
        }
        .subtitle-effect {
            font-family: 'Orbitron', sans-serif;
            font-size: 1.2rem;
            color: white;
            text-align: center;
            animation: fadeIn 2s ease-in-out;
            transition: transform 0.3s ease;
        }
        .subtitle-effect:hover {
            transform: scale(1.05);
            color: #f45208;
        }
        @keyframes fadeIn {
            0% { opacity: 0; transform: translateY(10px); }
            100% { opacity: 1; transform: translateY(0); }
        }
        .stApp {
            background-color: #2f6974;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='title-custom'>PLAYER<br>PROFILING</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle-effect'>Analyze the physical and athletic profiles of draft prospects</div>", unsafe_allow_html=True)

def get_player_image_path(player_name):
    try:
        last, first = player_name.split(", ")
        base_name = f"{first}_{last}".replace(" ", "_")
    except:
        base_name = player_name.replace(" ", "_")
    for ext in ["png", "jpg", "jpeg"]:
        image_path = f"images/{base_name}.{ext}"
        if os.path.exists(image_path):
            return image_path
    return None

df = pd.read_csv("Draft_Combine_00_25.csv")

if df is not None:
    available_years = sorted(df['YEAR'].dropna().unique())
    selected_year = st.selectbox("Select draft year", available_years, index=len(available_years)-1)
    df_year = df[df['YEAR'] == selected_year]
    player_names = sorted(df_year['PLAYER'].dropna().unique())
    selected_player = st.selectbox("View detailed profile for a player", player_names)

    if selected_player:
        player_data = df_year[df_year['PLAYER'] == selected_player].iloc[0]
        col1, col2 = st.columns([1, 2])

        with col1:
            image_path = get_player_image_path(selected_player)
            if image_path:
                st.image(image_path, caption=selected_player, width=200)
            else:
                st.image("https://via.placeholder.com/250x350?text=No+Image", caption=selected_player, width=200)

        with col2:
            st.subheader(f"{selected_player}")
            st.markdown(f"**Position:** {player_data['POS']}")
            st.markdown(f"**Height:** {player_data['HGT']} inches")
            st.markdown(f"**Weight:** {player_data['WGT']} lbs")
            st.markdown(f"**BMI:** {player_data['BMI']:.1f}" if pd.notna(player_data['BMI']) else "**BMI:** N/A")
            st.markdown(f"**Body Fat %:** {player_data['BF']}" if pd.notna(player_data['BF']) else "**Body Fat %:** N/A")
            st.markdown(f"**Wingspan:** {player_data['WNGSPN']} inches")

        st.markdown("---")

    selected_players = st.multiselect("Compare players from the same year", player_names, default=[selected_player])

    if selected_players:
        selected_df = df_year[df_year['PLAYER'].isin(selected_players)]
        st.subheader("\U0001F4AA Physical Attributes")

        phys_metrics = ["HGT", "WGT", "BMI", "BF", "WNGSPN", "STNDRCH"]
        selected_phys = st.multiselect("Select physical metrics to display", phys_metrics, default=["HGT", "WGT", "BMI"])

        if "HGT" in selected_phys and "WGT" in selected_phys:
            col_hgt, col_wgt = st.columns(2)
            with col_hgt:
                fig_hgt = px.bar(selected_df, x="PLAYER", y="HGT", text="HGT")
                fig_hgt.update_traces(textposition='outside', marker=dict(color='lightblue'))
                fig_hgt.update_layout(title="Height Comparison", margin=dict(t=40))
                st.plotly_chart(fig_hgt, use_container_width=True)
            with col_wgt:
                fig_wgt = px.bar(selected_df, x="PLAYER", y="WGT", text="WGT")
                fig_wgt.update_traces(textposition='outside', marker=dict(color='lightblue'))
                fig_wgt.update_layout(title="Weight Comparison", margin=dict(t=40))
                st.plotly_chart(fig_wgt, use_container_width=True)
            selected_phys = [m for m in selected_phys if m not in ["HGT", "WGT"]]

        if "BMI" in selected_phys:
            st.subheader("BMI Overview")
            for _, row in selected_df.iterrows():
                bmi_value = row['BMI'] if pd.notna(row['BMI']) else 0
                bmi_percent = min(max(bmi_value / 35, 0), 1)
                st.markdown(f"""
                    <div style='margin-bottom: 1rem;'>
                        <strong style='color:white;'>{row['PLAYER']}</strong><br>
                        <div style='position: relative; background: #ddd; border-radius: 12px; height: 28px; width: 100%;'>
                            <div style='background: #f48c06; height: 100%; width: {bmi_percent*100:.1f}%; border-radius: 12px;'></div>
                            <div style='position: absolute; top: 0; left: 50%; transform: translateX(-50%); color: white; font-weight: bold; font-size: 15px; line-height: 28px;'>
                                {bmi_value:.1f} BMI
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            selected_phys = [m for m in selected_phys if m != "BMI"]

        if "WNGSPN" in selected_phys:
            st.subheader("Wingspan Overview")
            for _, row in selected_df.iterrows():
                st.markdown(f"**{row['PLAYER']}** — {row['WNGSPN']} inches")
                st.markdown("<div style='height: 2px; background-color: white; margin: 8px 0 20px 0;'></div>", unsafe_allow_html=True)
            selected_phys = [m for m in selected_phys if m != "WNGSPN"]

        if "STNDRCH" in selected_phys:
            st.subheader("Standing Reach Overview")
            for _, row in selected_df.iterrows():
                st.markdown(f"**{row['PLAYER']}** — {row['STNDRCH']} inches")
                st.markdown("<div style='height: 2px; background-color: white; margin: 8px 0 20px 0;'></div>", unsafe_allow_html=True)
            selected_phys = [m for m in selected_phys if m != "STNDRCH"]

        # Combined Physical Score
        st.subheader("\U0001F3C6 Combined Physical Score")
        weights = {"HGT": 0.25, "WGT": 0.20, "BMI": 0.15, "WNGSPN": 0.25, "STNDRCH": 0.15}
        metrics = list(weights.keys())
        score_df = selected_df[['PLAYER'] + metrics].dropna()

        scaler = MinMaxScaler()
        score_df[metrics] = scaler.fit_transform(score_df[metrics])
        score_df['Physical Score'] = score_df[metrics].mul(pd.Series(weights)).sum(axis=1)

        score_fig = px.bar(score_df, x='PLAYER', y='Physical Score', text='Physical Score', color='PLAYER')
        score_fig.update_layout(template="plotly_white", font=dict(size=16), margin=dict(t=50))
        st.plotly_chart(score_fig, use_container_width=True)


# Caricamento dati
# Caricamento dati
import streamlit as st
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

st.title("📈 Athletic Performance Comparison")
df = pd.read_csv("Draft_Combine_00_25.csv")

available_years = sorted(df['YEAR'].dropna().unique())
selected_year = st.selectbox("Select draft year", available_years, index=len(available_years)-1, key="athletic_year")
df_year = df[df['YEAR'] == selected_year]
player_names = sorted(df_year['PLAYER'].dropna().unique())

selected_players = st.multiselect("Select 2 players to compare", player_names, max_selections=2)

metric_labels = {
    "STNDVERT": "Standing Vertical Jump",
    "LPVERT": "Max Vertical Jump",
    "LANE": "Lane Agility Time",
    "SHUTTLE": "Shuttle Run",
    "SPRINT": "Three-Quarter Sprint",
    "BENCH": "Bench Press Reps"
}
colors = ["#f94144", "#f3722c", "#f8961e", "#43aa8b", "#577590", "#277da1"]
athletic_metrics = list(metric_labels.keys())

selected_metrics = st.multiselect("Select athletic metrics to compare", athletic_metrics, default=athletic_metrics)

st.markdown("""
    <style>
        .metric-label {
            font-weight: bold;
            color: #333;
            margin-top: 12px;
            margin-bottom: 4px;
        }
        .bar-wrapper {
            background-color: #ddd;
            height: 28px;
            border-radius: 14px;
            overflow: hidden;
            position: relative;
        }
        .bar {
            height: 100%;
            font-weight: bold;
            text-align: right;
            padding-right: 12px;
            line-height: 28px;
            font-size: 16px;
            color: transparent;
        }
        .bar-value {
            position: absolute;
            right: 10px;
            top: 0;
            height: 28px;
            line-height: 28px;
            font-size: 16px;
            font-weight: bold;
            color: black;
        }
    </style>
""", unsafe_allow_html=True)

if len(selected_players) == 2 and selected_metrics:
    player1_data = df_year[df_year['PLAYER'] == selected_players[0]][selected_metrics]
    player2_data = df_year[df_year['PLAYER'] == selected_players[1]][selected_metrics]

    if not player1_data.empty and not player2_data.empty:
        combined = pd.concat([player1_data, player2_data]).dropna(axis=1)
        used_metrics = combined.columns.tolist()

        col1, col2 = st.columns(2)

        for j, metric in enumerate(used_metrics):
            label = metric_labels.get(metric, metric)
            val1 = player1_data[metric].values[0]
            val2 = player2_data[metric].values[0]

            if metric in ["LANE", "SHUTTLE", "SPRINT"]:
                best_is_lower = True
            else:
                best_is_lower = False

            color = colors[j % len(colors)]

            if (val1 < val2 and best_is_lower) or (val1 > val2 and not best_is_lower):
                percent1, percent2 = 100, 0
            elif (val2 < val1 and best_is_lower) or (val2 > val1 and not best_is_lower):
                percent1, percent2 = 0, 100
            else:
                percent1 = percent2 = 100

            with col1:
                st.markdown(f"<div class='metric-label'>{label}</div>", unsafe_allow_html=True)
                st.markdown(f"""
                    <div class='bar-wrapper'>
                        <div class='bar' style='width:{percent1:.1f}%; background-color:{color if percent1 > 0 else '#ddd'};'></div>
                        <div class='bar-value'>{val1}</div>
                    </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"<div class='metric-label'>&nbsp;</div>", unsafe_allow_html=True)
                st.markdown(f"""
                    <div class='bar-wrapper'>
                        <div class='bar' style='width:{percent2:.1f}%; background-color:{color if percent2 > 0 else '#ddd'};'></div>
                        <div class='bar-value'>{val2}</div>
                    </div>
                """, unsafe_allow_html=True)
else:
    st.info("Please select exactly two players and at least one metric to compare.")
