import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from datetime import datetime, timedelta
from core.backtesting_engine import BacktestingEngine
from ui.forms import render_strategy_params
from ui.display import show_plot, show_metrics
from ui.engine_interface import run_backtest_with_inputs

st.title("Backtester Tool 🔙📈🛠️")
st.text(
    "A lightweight backtesting tool that evaluates your trading strategies using historical close prices."
)

be = BacktestingEngine()
today = datetime.today().date()

selected_label = st.selectbox(
    "Search by Ticker or Company Name", list(be.get_tickets().keys())
)
be.ticker = be.get_tickets()[selected_label]

col1, col2 = st.columns([1, 1])
be.start_date = col1.date_input("Select Start Date", value=today - timedelta(days=365))
be.end_date = col2.date_input("Select End Date", value=today)

be.strategy_name = st.selectbox("Select a Strategy", be.get_strategies())
strategy_params = render_strategy_params(be.get_strategy_params())

try:
    if st.button("Backtest"):
        df, plot_lines, subplot_lines = run_backtest_with_inputs(
            be, be.strategy_name, strategy_params
        )
        st.success("Backtest completed successfully!")
        st.write("Results:", df)
        st.session_state.update(
            {
                "backtest_df": df,
                "plot_lines": plot_lines,
                "subplot_lines": subplot_lines,
                "backtest_run": True,
            }
        )
except ValueError as e:
    st.error(f"Error: {e}")

if st.session_state.get("backtest_run"):
    df = st.session_state["backtest_df"]
    plot_lines = st.session_state["plot_lines"]
    subplot_lines = st.session_state["subplot_lines"]
    show_plot(df, plot_lines, subplot_lines)
    show_metrics(df, be)
