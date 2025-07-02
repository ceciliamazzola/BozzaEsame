import streamlit as st

# CONFIGURAZIONE DELLA PAGINA
st.set_page_config(page_title="Premium Access", page_icon="💳")

# CSS: Font Orbitron + sfondo petrolio
st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&display=swap" rel="stylesheet">
    <style>
        body {
            background-color: #2c6a6d;
            color: white;
        }
        .reportview-container, .main, .block-container {
            background-color: #2c6a6d !important;
            color: white !important;
        }
        h1, h2, h3, h4, h5, h6, p, li {
            color: white !important;
        }
        .plan-card {
            border: 2px solid #f45208;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            background-color: white;
            color: #333;
            margin: 10px;
        }
        .highlight {
            border: 4px solid #f45208;
        }
        .plan-title {
            font-size: 24px;
            font-weight: bold;
        }
        .price {
            font-size: 32px;
            color: #f45208;
            margin: 10px 0;
        }
        .features {
            font-size: 16px;
            margin-top: 10px;
        }
        .select-btn {
            background-color: #f45208;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            margin-top: 15px;
            cursor: pointer;
        }
        .select-btn:hover {
            background-color: #d44107;
        }
        .title-font {
            font-family: 'Orbitron', sans-serif;
            font-size: 42px;
            color: #f45208;
            font-weight: 700;
            text-align: center;
            margin-bottom: 30px;
        }
    </style>
""", unsafe_allow_html=True)

# TITOLO PERSONALIZZATO
st.markdown("<div class='title-font'>Unlock Premium Basketball Analytics</div>", unsafe_allow_html=True)

# SOTTOTITOLO
st.write("Get exclusive access to advanced player metrics, draft insights, and real-time analytics that give you the competitive edge.")

# PIANI DI ABBONAMENTO
plans = [
    {
        "name": "Starter",
        "price": "$19/month",
        "desc": "Perfect for individual enthusiasts",
        "features": ["Basic player statistics", "Weekly reports", "Email support", "Limited data exports"]
    },
    {
        "name": "Pro",
        "price": "$49/month",
        "desc": "Best for professional scouts and analysts",
        "features": ["Advanced analytics", "Player comparisons", "Real-time updates", "Priority support", "Unlimited exports", "Custom reports"],
        "popular": True
    },
    {
        "name": "Enterprise",
        "price": "$79/month",
        "desc": "Complete solution for organizations",
        "features": ["Full analytics suite", "Custom reports", "API access", "Dedicated support", "Team collaboration", "White-label options"]
    }
]

# RENDERING DEI PIANI
cols = st.columns(3)
for idx, plan in enumerate(plans):
    with cols[idx]:
        extra_class = " highlight" if plan.get("popular") else ""
        st.markdown(f"""
            <div class='plan-card{extra_class}'>
                <div class='plan-title'>{plan['name']}</div>
                <div class='price'>{plan['price']}</div>
                <div>{plan['desc']}</div>
                <ul class='features'>
                    {''.join([f"<li>{f}</li>" for f in plan['features']])}
                </ul>
                <form action="#" method="post">
                    <button class='select-btn' name='selected_plan' type='submit'>{'Choose ' + plan['name']}</button>
                </form>
            </div>
        """, unsafe_allow_html=True)

# SEZIONE FINALE
st.markdown("---")
st.subheader("Start Your Trial")

with st.form("payment_form"):
    email = st.text_input("Email Address")
    payment_method = st.radio("Payment Method", ["Credit Card", "PayPal"])
    if payment_method == "Credit Card":
        cc_number = st.text_input("Card Number")
        cc_expiry = st.text_input("MM/YY")
        cc_cvc = st.text_input("CVC")
    st.markdown("**Starter Plan (Monthly)**\n\n7-day free trial\n\nThen $19/month")
    submitted = st.form_submit_button("Start Free Trial")
    if submitted:
        st.success(f"Subscription started for {email}!")

