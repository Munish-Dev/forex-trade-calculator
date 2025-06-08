import streamlit as st

# Define pip size for common forex pairs like EUR/USD or USD/EUR
PIP_SIZE = 0.0001

st.title("💹 Forex Trade Calculator with Auto 1:2 Risk-Reward")

st.sidebar.header("Trade Parameters")

account_balance = st.sidebar.number_input("Account Balance ($)", value=1000.0, step=10.0)
risk_percent = st.sidebar.slider("Risk % per Trade", min_value=0.1, max_value=10.0, value=1.0)
entry_price = st.sidebar.number_input("Entry Price", value=1.1000, format="%.5f")
trade_direction = st.sidebar.selectbox("Trade Direction", ["Buy", "Sell"])
stop_loss_pips = st.sidebar.number_input("Stop Loss Distance (pips)", min_value=1, max_value=1000, value=50)

# Auto-calculate Stop Loss and Take Profit prices for 1:2 RR ratio
if trade_direction == "Buy":
    stop_loss_price = entry_price - (stop_loss_pips * PIP_SIZE)
    take_profit_price = entry_price + (2 * stop_loss_pips * PIP_SIZE)
else:
    stop_loss_price = entry_price + (stop_loss_pips * PIP_SIZE)
    take_profit_price = entry_price - (2 * stop_loss_pips * PIP_SIZE)

st.sidebar.markdown(f"**Calculated Stop Loss Price:** {stop_loss_price:.5f}")
st.sidebar.markdown(f"**Calculated Take Profit Price:** {take_profit_price:.5f}")

def forex_trade_calculator(account_balance, risk_percent, entry_price,
                           stop_loss_price, take_profit_price,
                           trade_direction, pip_value_per_lot=10):

    risk_dollars = (risk_percent / 100) * account_balance

    if trade_direction.lower() == "buy":
        stop_loss_pips_calc = (entry_price - stop_loss_price) * 10000
        take_profit_pips_calc = (take_profit_price - entry_price) * 10000
    else:
        stop_loss_pips_calc = (stop_loss_price - entry_price) * 10000
        take_profit_pips_calc = (entry_price - take_profit_price) * 10000

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
