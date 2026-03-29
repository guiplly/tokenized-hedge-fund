import streamlit as st
import pandas as pd

# Page config
st.set_page_config(page_title="Tokenized Hedge Fund", layout="wide")

# --------------------------
# Simulated database
# --------------------------
if "tokens" not in st.session_state:
    st.session_state.tokens = 0
if "nav" not in st.session_state:
    st.session_state.nav = 100  # price per token
if "cash" not in st.session_state:
    st.session_state.cash = 10000  # starting cash

# Fees
MANAGEMENT_FEE = 0.005  # 0.5%
TRANSACTION_FEE = 0.01  # 1%

# --------------------------
# Sidebar Menu
# --------------------------
menu = st.sidebar.selectbox("Menu", ["Home", "Invest", "Sell", "Dashboard", "Admin"])

# --------------------------
# HOME PAGE
# --------------------------
if menu == "Home":
    st.title("Welcome to TokenFund")
    st.write("Invest in a hedge fund via blockchain tokens. Minimum investment: €100 instead of €100,000.")
    
    st.subheader("How It Works")
    st.markdown("""
    1. **Tokenization**: Each hedge fund is split into tokens. Each token represents a share of the fund.  
    2. **Invest**: Buy tokens with any amount above the minimum investment.  
    3. **Portfolio Tracking**: Dashboard shows tokens owned and current value.  
    4. **Sell Tokens**: Sell tokens anytime at the current NAV (fees apply).  
    5. **Fund Performance**: Monitor NAV and portfolio growth over time.  
    6. **Admin (Simulation)**: Update NAV to simulate market changes.  
    """)
    
    st.info("This is a prototype using Streamlit. In a real system, tokens would be ERC-20 on a blockchain, and transactions would use smart contracts.")

# --------------------------
# INVEST PAGE
# --------------------------
elif menu == "Invest":
    st.header("Buy Tokens")
    st.write(f"Current Token Price (NAV): €{st.session_state.nav:.2f}")
    amount = st.number_input("How much would you like to invest?", min_value=0.0, step=100.0)
    
    if st.button("Buy"):
        total_fee = amount * (MANAGEMENT_FEE + TRANSACTION_FEE)
        net_invest = amount - total_fee
        
        if amount > st.session_state.cash:
            st.error("Insufficient cash to invest this amount.")
        elif amount < 100:
            st.error("Minimum investment is €100.")
        else:
            tokens_bought = net_invest / st.session_state.nav
            st.session_state.tokens += tokens_bought
            st.session_state.cash -= amount
            st.success(
                f"You invested €{amount:.2f} (Fees: €{total_fee:.2f} → Management: {MANAGEMENT_FEE*100:.1f}%, Transaction: {TRANSACTION_FEE*100:.1f}%)\n"
                f"Tokens received: {tokens_bought:.2f}"
            )

# --------------------------
# SELL PAGE
# --------------------------
elif menu == "Sell":
    st.header("Sell Tokens")
    st.write(f"Current Token Price (NAV): €{st.session_state.nav:.2f}")
    tokens_to_sell = st.number_input("How many tokens would you like to sell?", min_value=0.0, step=1.0)
    
    if st.button("Sell"):
        if tokens_to_sell > st.session_state.tokens:
            st.error("You do not own enough tokens.")
        else:
            gross_amount = tokens_to_sell * st.session_state.nav
            fees = gross_amount * (MANAGEMENT_FEE + TRANSACTION_FEE)
            net_amount = gross_amount - fees
            st.session_state.tokens -= tokens_to_sell
            st.session_state.cash += net_amount
            st.success(
                f"You sold {tokens_to_sell:.2f} tokens for €{net_amount:.2f} " +
                f"(Fees: €{fees:.2f} → Management: {MANAGEMENT_FEE*100:.1f}%, Transaction: {TRANSACTION_FEE*100:.1f}%)"
            )

# --------------------------
# DASHBOARD PAGE
# --------------------------
elif menu == "Dashboard":
    st.header("Portfolio Dashboard")
    
    portfolio_value = st.session_state.tokens * st.session_state.nav
    st.metric("Tokens Owned", f"{st.session_state.tokens:.2f}")
    st.metric("Token Price (NAV)", f"€{st.session_state.nav:.2f}")
    st.metric("Portfolio Value", f"€{portfolio_value:.2f}")
    st.metric("Cash Available", f"€{st.session_state.cash:.2f}")
    
    st.subheader("Fund Performance")
    # Example NAV trend
    data = pd.DataFrame({
        'Day': range(1, 11),
        'NAV': [100, 102, 101, 105, 110, 108, 112, 115, 118, st.session_state.nav]
    })
    st.line_chart(data.set_index('Day'))

# --------------------------
# ADMIN PAGE
# --------------------------
# --------------------------
# ADMIN PAGE
# --------------------------
elif menu == "Admin":
    st.header("Admin - Update NAV")
    # Force value to float
    new_nav = st.number_input("Set New NAV", min_value=1.0, value=float(st.session_state.nav), step=0.1)
    
    if st.button("Update NAV"):
        st.session_state.nav = new_nav
        st.success(f"NAV updated to €{new_nav:.2f}")