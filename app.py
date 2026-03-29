import streamlit as st
import pandas as pd

st.set_page_config(page_title="Tokenized Hedge Fund", layout="wide")

# Base de données simulée
if "tokens" not in st.session_state:
    st.session_state.tokens = 0
if "nav" not in st.session_state:
    st.session_state.nav = 100  # prix du token
if "cash" not in st.session_state:
    st.session_state.cash = 10000  # argent initial

st.title("Tokenised Hedge Fund Platform")

menu = st.sidebar.selectbox("Menu", ["Home", "Invest", "Sell", "Dashboard", "Admin"])

# Home
if menu == "Home":
    st.header("Welcome on TokenFund")
    st.write("Invest in a hedge fund via tokens.")
    st.write("Minimum investment: €100 instead of €100,000.")
    st.subheader("How It Works ?")
    st.write("""
    1. **Tokenization:** Each hedge fund is split into tokens. Each token represents a share of the fund.
    2. **Invest:** You can buy tokens with any amount above the minimum investment.
    3. **Portfolio Tracking:** Your dashboard shows how many tokens you own and the current value of your investment.
    4. **Selling Tokens:** You can sell tokens anytime at the current NAV price.
    5. **Fund Performance:** You can monitor the fund’s NAV and see how the investment grows over time.
    6. **Admin (Simulation):** The NAV can be updated to simulate market changes.
    """)

# Invest
elif menu == "Invest":
    st.header("Buy tokens")
    st.write("Price of token (NAV): €", st.session_state.nav)
    amount = st.number_input("how much would you like to invest ?", min_value=0)
    
    if st.button("Buy"):
        tokens_bought = amount / st.session_state.nav
        st.session_state.tokens += tokens_bought
        st.session_state.cash -= amount
        st.success(f"You bought {tokens_bought:.2f} tokens")

# Sell
elif menu == "Sell":
    st.header("Sells tokens")
    tokens_to_sell = st.number_input("How much token would you like to sells ?", min_value=0.0)
    
    if st.button("Sell"):
        if tokens_to_sell <= st.session_state.tokens:
            money = tokens_to_sell * st.session_state.nav
            st.session_state.tokens -= tokens_to_sell
            st.session_state.cash += money
            st.success(f"you sold for €{money:.2f}")
        else:
            st.error("not enought tokens")

# Dashboard
elif menu == "Dashboard":
    st.header("Your portfoolio")
    portfolio_value = st.session_state.tokens * st.session_state.nav
    
    st.metric("Tokens possessed", f"{st.session_state.tokens:.2f}")
    st.metric("Price of token", f"€{st.session_state.nav}")
    st.metric("Value of portfolio", f"€{portfolio_value:.2f}")
    st.metric("Cash", f"€{st.session_state.cash:.2f}")

    st.subheader("Fund Performance")
    
    data = pd.DataFrame({
        'Jour': range(1, 11),
        'NAV': [100, 102, 101, 105, 110, 108, 112, 115, 118, st.session_state.nav]
    })
    
    st.line_chart(data.set_index('Jour'))

# Admin
elif menu == "Admin":
    st.header("Admin - Modify the NAV")
    new_nav = st.number_input("New NAV", min_value=1)
    
    if st.button("Update"):
        st.session_state.nav = new_nav
        st.success("NAV update")