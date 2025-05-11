# Lightweight Backtesting Tool

[Lightweight Backtester](https://lightweightbacktester.streamlit.app/) is a web-based application designed for evaluating trading strategies using historical close prices. It allows you to test and analyze your strategies with various technical indicators and performance metrics, providing insights based on the backtest results.

## Features

- **Simple Interface**: A user-friendly Streamlit interface for selecting tickers, date ranges, and strategies.
- **Custom Strategy Parameters**: Configure and test trading strategies with customizable parameters.
- **Technical Indicators**: Use common indicators like Moving Averages, RSI, MACD, and more.
- **Performance Metrics**: View key metrics like Sharpe Ratio, Max Drawdown, Total Return, Calmar Ratio, and Yearly Return.
- **Interactive Visualizations**: Analyze results with candlestick charts and overlaid indicators.
  
## How to Use

1. **Visit the App**: Go to the [Lightweight Backtester](https://lightweightbacktester.streamlit.app/) website.
2. **Select a Ticker**: Choose a ticker or company name from the dropdown list to load the historical data.
3. **Set Date Range**: Select the start and end dates for your backtest. You can choose any custom time period for testing.
4. **Choose a Strategy**: Pick a strategy from the list of available strategies.
5. **Configure Parameters**: Set the parameters for your selected strategy based on your preferences.
6. **Run the Backtest**: Click the "Backtest" button to simulate buy and sell signals based on the strategy.
7. **View Results**: After the backtest is complete, view detailed performance metrics and strategy visualizations.

## Key Metrics

- **Sharpe Ratio**: Measures the risk-adjusted return of your strategy.
- **Max Drawdown**: Indicates the maximum loss from the highest peak to the lowest trough.
- **Calmar Ratio**: The ratio of average annual return to maximum drawdown.
- **Total Return**: The overall return during the backtest period.
- **Yearly Return**: The average annual return based on the backtest results.

## Available Strategies

- **Simple Moving Average (SMA) Crossover**: A strategy based on the crossover of short-term and long-term moving averages.
- **RSI (Relative Strength Index)**: A momentum oscillator that buys when RSI is below a threshold and sells when above.
- **MACD (Moving Average Convergence Divergence)**: A strategy using the difference between two moving averages to identify trends.

## Installation (For Local Use)

If you want to run the app locally, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repo/lightweight-backtester.git
   ```
2. Install Python 3.12
3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
4. **Run the Streamlit App**
    ```bash
    streamlit run app.py
    ```

## Contributing
Contributions are welcome! If you have ideas for improvements or fixes, feel free to submit issues or pull requests.
