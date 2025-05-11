from plotly.subplots import make_subplots
import plotly.graph_objects as go
import streamlit as st
import pandas as pd


def plot_candlestick_with_indicators(
    df: pd.DataFrame, line_names: dict[str, str], subplot_lines: dict
) -> go.Figure:
    required_columns = ["Date", "Open", "High", "Low", "Close", "Position"]
    if not all(col in df.columns for col in required_columns):
        st.error("DataFrame is missing one or more required columns.")
        return

    fig = make_subplots(
        rows=2 if subplot_lines else 1,
        cols=1,
        shared_xaxes=True,
        row_heights=[0.7, 0.3] if subplot_lines else [1],
        vertical_spacing=0.05,
    )

    # Main candlestick chart
    fig.add_trace(
        go.Candlestick(
            x=df["Date"],
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"],
            name="Candlesticks",
        ),
        row=1,
        col=1,
    )

    # Add indicators like SMA, etc.
    colors = ["orange", "blue", "yellow", "purple", "brown"]
    for label, column_name in line_names.items():
        fig.add_trace(
            go.Scatter(
                x=df["Date"],
                y=df[column_name],
                mode="lines",
                name=label,
                line=dict(color=colors.pop(0)),
            ),
            row=1,
            col=1,
        )

    # Buy/Sell signals
    buy_signals = df[df["Position"] == 1]
    sell_signals = df[df["Position"] == -1]

    fig.add_trace(
        go.Scatter(
            x=buy_signals["Date"],
            y=buy_signals["Close"],
            mode="markers",
            name="Buy Signal",
            marker=dict(symbol="triangle-up", color="green", size=10),
        ),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Scatter(
            x=sell_signals["Date"],
            y=sell_signals["Close"],
            mode="markers",
            name="Sell Signal",
            marker=dict(symbol="triangle-down", color="red", size=10),
        ),
        row=1,
        col=1,
    )

    # Position changes as vertical lines
    position_change_indices = df[df["Position"].diff() != 0].index
    for idx in position_change_indices:
        fig.add_vline(
            x=df["Date"].iloc[idx],
            line=dict(color="gray", dash="dash", width=1),
            row=1,
            col=1,
        )

    colors = ["orange", "blue", "yellow", "purple", "brown"]
    if subplot_lines:
        horizontal_lines = {
            k: v for k, v in subplot_lines.items() if isinstance(v, (int, float))
        }
        normal_lines = {
            k: v for k, v in subplot_lines.items() if not isinstance(v, (int, float))
        }
        for line_name, column_name in normal_lines.items():
            fig.add_trace(
                go.Scatter(
                    x=df["Date"],
                    y=df[column_name],
                    mode="lines",
                    name=line_name,
                    line=dict(color=colors.pop(0)),
                ),
                row=2,
                col=1,
            )

        # Add overbought/oversold zones
        for color, value in horizontal_lines.items():
            fig.add_hline(y=value, line=dict(color=color, dash="dash"), row=2, col=1)

    fig.update_layout(
        title="Stock Price with Indicators",
        xaxis_title="Date",
        yaxis_title="Price",
        xaxis_rangeslider_visible=False,
        height=700 if subplot_lines else 500,
    )

    return fig
