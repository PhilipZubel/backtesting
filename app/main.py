import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from datetime import datetime, timedelta

from core import BacktestingEngine
from ui import validate_dates
from ui.plot import plot_candlestick_with_indicators
from core.metrics import track_positions

be = BacktestingEngine()

st.title("Backtester Tool 🔙📈🛠️")

today = datetime.today().date()

ticker_options = be.get_tickets()
selected_label = st.selectbox("Search by Ticker or Company Name", list(ticker_options.keys()))
be.ticker = ticker_options[selected_label]

col1, col2 = st.columns([1, 1])
col1, col2 = st.columns([1, 1])
with col1:
    be.start_date = st.date_input(
        "Select Start Date",
        value=today - timedelta(days=365),
        min_value=datetime(2000, 1, 1).date(),
        max_value=today
    )
with col2:
    be.end_date = st.date_input(
        "Select End Date",
        value=today,
        min_value=datetime(2000, 1, 1).date(),
        max_value=today
    )
    
be.strategy_name = st.selectbox("Select a Strategy", be.get_strategies())
strategy_params = be.get_strategy_params()

input_functions = {
    int: st.number_input,
    float: st.number_input,
    bool: st.checkbox,
    str: st.text_input,
}

# Dynamically create input fields for strategy parameters
be.strategy_params = {}
for param_name, param_info in strategy_params.items():
    param_type = param_info["type"]
    default_value = param_info["default"]
    input_function = input_functions.get(param_type)
    
    if input_function:
        if param_type in [int, float]:
            value = default_value or (10 if param_type == int else 1.0)
            be.strategy_params[param_name] = input_function(f"Enter {param_name}", value=value, format="%.2f" if param_type == float else None)
        elif param_type == bool:
            be.strategy_params[param_name] = input_function(f"Enable {param_name}", value=default_value or False)
        elif param_type == str:
            be.strategy_params[param_name] = input_function(f"Enter {param_name}", value=default_value or "")
    else:
        st.warning(f"Unsupported parameter type: {param_type} for {param_name}")
        
st.write(f"Running '{be.strategy_name}' strategy with the following parameters:")
st.write(be.strategy_params)

if st.button("Backtest"):
    df, plot_lines = be.run_backtest()
    st.success("Backtest completed successfully!")
    st.write("Results:", df)
    metrics = be.get_metrics(df)
    risk_free_rate = st.number_input("Risk-Free Rate (annual)", min_value=0.0, max_value=0.2, value=0.0433, step=0.001)
    st.write(f"Sharpe Ratio: {metrics['sharpe_ratio']:.2f}")
    st.write(f"Max Drawdown: {metrics['max_drawdown']:.2%}")
    st.write(f"Calmar Ratio: {metrics['calmar_ratio']:.2f}")
    st.write(f"Total Return: {metrics['total_return']:.2%}")
    st.write(f"Total Return (Annualized): {metrics['yearly_return']:.2%}")
    
    fig = plot_candlestick_with_indicators(df, plot_lines)
    st.plotly_chart(fig)
    
    tracked_positions = track_positions(df)
    st.write("Tracked Positions:", tracked_positions)

try:
    start_str = be.start_date.strftime("%Y-%m-%d")
    end_str = be.end_date.strftime("%Y-%m-%d")
    start, end = validate_dates(start_str, end_str)
except ValueError as e:
    st.error(f"Error: {e}")

