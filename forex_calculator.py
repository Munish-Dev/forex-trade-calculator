import streamlit as st

# Predefined pip sizes for common pairs
pip_sizes = {
    "EUR/USD": 0.0001,
    "GBP/USD": 0.0001,
    "USD/JPY": 0.01,
    "EUR/JPY": 0.01,
    "GBP/JPY": 0.01,
    "AUD/USD": 0.0001,
    "USD/CAD": 0.0001
}

st.title("💹 Forex Trade Calculator with 1:2 RR + Pip Size Per Pair")

st.sidebar.header("Trade Setup")

# Input: currency pair
currency_pair = st.sidebar.selectbox("Currency Pair", list(pip_sizes.keys()))
PIP_SIZE = pip_sizes[currency_pair]

# Optional manual override
if st.sidebar.checkbox("Override Pip Size"):
    PIP_SIZE = st.sidebar.number_input("Custom Pip Size", value=PIP_SIZE, step=0.00001, format="%.5f")

# Inputs
account_balance = st.sidebar.number_input("Account Balance ($)", value=1000.0, step=10.0)
risk_percent = st.sidebar.slider("Risk % per Trade", min_value=0.1, max_value=10.0, value=1.0)
entry_price = st.sidebar.number_input("Entry Price", value=1.1000, format="%.5f")
trade_direction = st.sidebar.selectbox("Trade Direction", ["Buy", "Sell"])
stop_loss_pips = st.sidebar.number_input("Stop Loss Distance (pips)", min_value=1, max_value=1000, value=50)

# Auto-calculate SL and TP prices based on pip size
if trade_direction == "Buy":
    stop_loss_price = entry_price - (stop_loss_pips * PIP_SIZE)
    take_profit_price = entry_price + (2 * stop_loss_pips * PIP_SIZE)
else:
    stop_loss_price = entry_price + (stop_loss_pips * PIP_SIZE)
    take_profit_price = entry_price - (2 * stop_loss_pips * PIP_SIZE)

st.sidebar.markdown(f"**Pip Size:** {PIP_SIZE}")
st.sidebar.markdown(f"**Stop Loss Price:** `{stop_loss_price:.5f}`")
st.sidebar.markdown(f"**Take Profit Price:** `{take_profit_price:.5f}`")

# Calculation function
def forex_trade_calculator(account_balance, risk_percent, entry_price,
                           stop_loss_price, take_profit_price,
                           trade_direction, pip_value_per_lot=10):

    risk_dollars = (risk_percent / 100) * account_balance

    if trade_direction.lower() == "buy":
        stop_loss_pips_calc = (entry_price - stop_loss_price) / PIP_SIZE
        take_profit_pips_calc = (take_profit_price - entry_price) / PIP_SIZE
    else:
        stop_loss_pips_calc = (stop_loss_price - entry_price) / PIP_SIZE
        take_profit_pips_calc = (entry_price - take_profit_price) / PIP_SIZE

    stop_loss_pips_calc = abs(stop_loss_pips_calc)
    take_profit_pips_calc = abs(take_profit_pips_calc)

    lot_size = risk_dollars / (stop_loss_pips_calc * pip_value_per_lot)
    reward_dollars = take_profit_pips_calc * pip_value_per_lot * lot_size
    rr_ratio = reward_dollars / risk_dollars if risk_dollars else 0
    pip_value = pip_value_per_lot * lot_size

    return {
        "Lot Size": round(lot_size, 3),
        "Risk Amount ($)": round(risk_dollars, 2),
        "Reward Amount ($)": round(reward_dollars, 2),
        "Stop Loss (pips)": round(stop_loss_pips_calc, 1),
        "Take Profit (pips)": round(take_profit_pips_calc, 1),
        "Pip Value ($)": round(pip_value, 2),
        "Risk-to-Reward Ratio": round(rr_ratio, 2)
    }

# Show results
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
