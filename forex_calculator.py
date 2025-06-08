import streamlit as st

def forex_trade_calculator(account_balance, risk_percent, entry_price,
                           stop_loss_price, take_profit_price,
                           trade_direction, pip_value_per_lot=10):

    risk_dollars = (risk_percent / 100) * account_balance

    if trade_direction.lower() == "buy":
        stop_loss_pips = (entry_price - stop_loss_price) * 10000
        take_profit_pips = (take_profit_price - entry_price) * 10000
    else:
        stop_loss_pips = (stop_loss_price - entry_price) * 10000
        take_profit_pips = (entry_price - take_profit_price) * 10000

    stop_loss_pips = abs(stop_loss_pips)
    take_profit_pips = abs(take_profit_pips)

    lot_size = risk_dollars / (stop_loss_pips * pip_value_per_lot)
    reward_dollars = take_profit_pips * pip_value_per_lot * lot_size
    rr_ratio = reward_dollars / risk_dollars if risk_dollars else 0
    pip_value = pip_value_per_lot * lot_size

    return {
        "Lot Size": round(lot_size, 3),
        "Risk Amount ($)": round(risk_dollars, 2),
        "Reward Amount ($)": round(reward_dollars, 2),
        "Stop Loss (pips)": round(stop_loss_pips, 1),
        "Take Profit (pips)": round(take_profit_pips, 1),
        "Pip Value ($)": round(pip_value, 2),
        "Risk-to-Reward Ratio": round(rr_ratio, 2)
    }

# ------------------- Streamlit App -------------------

st.title("💹 Forex Trade Calculator")

st.sidebar.header("Trade Parameters")

account_balance = st.sidebar.number_input("Account Balance ($)", value=1000.0, step=10.0)
risk_percent = st.sidebar.slider("Risk % per Trade", min_value=0.1, max_value=10.0, value=1.0)
entry_price = st.sidebar.number_input("Entry Price", value=1.1000, format="%.5f")
stop_loss_price = st.sidebar.number_input("Stop Loss Price", value=1.0950, format="%.5f")
take_profit_price = st.sidebar.number_input("Take Profit Price", value=1.1100, format="%.5f")
trade_direction = st.sidebar.selectbox("Trade Direction", ["Buy", "Sell"])
currency_pair = st.sidebar.text_input("Currency Pair (info only)", value="EUR/USD")

if st.button("Calculate Trade"):
    result = forex_trade_calculator(
        account_balance,
        risk_percent,
        entry_price,
        stop_loss_price,
        take_profit_price,
        trade_direction
    )

    st.subheader("📈 Trade Summary")
    for key, value in result.items():
        st.write(f"**{key}**: {value}")
