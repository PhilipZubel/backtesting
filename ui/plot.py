import plotly.graph_objects as go
import streamlit as st
import pandas as pd

def plot_candlestick_with_indicators(df: pd.DataFrame, line_names: dict[str, str]) -> go.Figure:
    required_columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Position']
    if not all(col in df.columns for col in required_columns):
        st.error("DataFrame is missing one or more required columns.")
        return
    
    fig = go.Figure(data=[go.Candlestick(
        x=df['Date'],
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        name='Candlesticks'
    )])

    
    colors = ['orange', 'blue', 'yellow', 'purple', 'brown']
    for label, column_name in line_names.items():
        fig.add_trace(go.Scatter(
            x=df['Date'], y=df[column_name],
            mode='lines', name=label, line=dict(color=colors.pop(0))
        ))

    buy_signals = df[df['Position'] == 1]
    sell_signals = df[df['Position'] == -1]

    fig.add_trace(go.Scatter(
        x=buy_signals['Date'], y=buy_signals['Close'],
        mode='markers', name='Buy Signal', marker=dict(symbol='triangle-up', color='green', size=10)
    ))

    fig.add_trace(go.Scatter(
        x=sell_signals['Date'], y=sell_signals['Close'],
        mode='markers', name='Sell Signal', marker=dict(symbol='triangle-down', color='red', size=10)
    ))

    position_change_indices = df[df['Position'].diff() != 0].index
    for idx in position_change_indices:
        fig.add_vline(x=df['Date'].iloc[idx], line=dict(color='gray', dash='dash'))

    fig.update_layout(
        title='Stock Price with Indicators',
        xaxis_title='Date',
        yaxis_title='Price',
        xaxis_rangeslider_visible=False,
    )

    return fig