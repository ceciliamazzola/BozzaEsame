import streamlit as st

st.set_page_config(
    page_title="Home - Next Gen Draft",
    page_icon="",
)


st.markdown("""
        <div style='display: flex; flex-direction: column; justify-content: center; align-items: center; height: 80vh; padding: 2rem;'>
            <div class="title-custom">NEXT GEN<br>DRAFT</div>
            <div class="subtitle-effect">
                Where talent meets destiny and every pick could shape the future of the game
            </div>
        </div>
    """, unsafe_allow_html=True)


# Global style for custom look and feel
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
            font-size: 5rem;
            color: var(--primary-color);
            -webkit-text-stroke: 3px var(--text-color);
            text-shadow: 5px 5px 10px rgba(0,0,0,0.3);
            text-align: center;
            margin-bottom: 2rem;
        }
        .subtitle-effect {
            font-family: 'Orbitron', sans-serif;
            font-size: 1.8rem;
            color: white;
            text-align: center;
            animation: fadeIn 2s ease-in-out;
            transition: transform 0.3s ease;
            margin-bottom: 3rem;
        }
        .subtitle-effect:hover {
            transform: scale(1.08);
            color: #f45208;
            text-shadow: 0 0 10px rgba(244,82,8,0.7);
        }
        .back-arrow {
            position: absolute;
            top: 20px;
            right: 30px;
            font-size: 18px;
            color: white;
            font-weight: bold;
            text-decoration: none;
            background-color: transparent;
            border: 2px solid white;
            padding: 6px 12px;
            border-radius: 8px;
            transition: all 0.3s ease;
        }
        .back-arrow:hover {
            background-color: white;
            color: #2f6974;
            text-decoration: none;
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

