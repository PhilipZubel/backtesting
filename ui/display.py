import streamlit as st
from ui.plot import plot_candlestick_with_indicators
from core.metrics import track_positions
import numpy as np

def show_plot(df, plot_lines, subplot_lines):
    fig = plot_candlestick_with_indicators(df, plot_lines, subplot_lines)
    st.plotly_chart(fig)

def show_metrics(df, be):
    be.risk_free_rate = st.number_input("Risk-Free Rate (annual)", min_value=0.0, max_value=0.2, value=0.043, step=0.001, format="%.4f")
    metrics = be.get_metrics(df)
    st.write(f"Sharpe Ratio: {metrics['sharpe_ratio']:.2f}" if isinstance(metrics['sharpe_ratio'], (float, np.float64)) else metrics['sharpe_ratio'])
    st.write(f"Max Drawdown: {metrics['max_drawdown']:.2%}")
    st.write(f"Calmar Ratio: {metrics['calmar_ratio']:.2f}")
    st.write(f"Total Return: {metrics['total_return']:.2%}")
    st.write(f"Yearly Return: {metrics['yearly_return']:.2%}")
    tracked_positions = track_positions(df)
    st.write("Tracked Positions:", tracked_positions)