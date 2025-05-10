import numpy as np
import pandas as pd

def sharpe_ratio(df, risk_free_rate=0.0433):
    # Initialize variable to track the cumulative return
    total_return = 1.0
    excess_returns = []
    
    # Track the entry price (buy price)
    entry_price = None
    
    for i in range(1, len(df)):
        if df['Position'].iloc[i] == 1:  # Buy signal
            entry_price = df['Close'].iloc[i]
        elif df['Position'].iloc[i] == -1 and entry_price is not None:  # Sell signal
            exit_price = df['Close'].iloc[i]
            # Calculate the return for this trade
            trade_return = (exit_price - entry_price) / entry_price
            excess_return = trade_return - risk_free_rate
            excess_returns.append(excess_return)
            total_return *= (1 + trade_return)
            entry_price = None  # Reset entry price after a trade
    
    # Ensure we close any open position on the last day
    if entry_price is not None:
        exit_price = df['Close'].iloc[-1]  # Sell at the last available price
        trade_return = (exit_price - entry_price) / entry_price
        excess_return = trade_return - risk_free_rate
        excess_returns.append(excess_return)
        total_return *= (1 + trade_return)

    # Calculate the Sharpe ratio: mean of excess returns / std of excess returns
    if len(excess_returns) > 0:
        return np.mean(excess_returns) / np.std(excess_returns) * np.sqrt(252)
    else:
        return np.nan

def max_drawdown(df):
    total_return = 1.0
    cumulative_returns = [1.0]
    
    # Track the entry price (buy price)
    entry_price = None
    
    for i in range(1, len(df)):
        if df['Position'].iloc[i] == 1:  # Buy signal
            entry_price = df['Close'].iloc[i]
        elif df['Position'].iloc[i] == -1 and entry_price is not None:  # Sell signal
            exit_price = df['Close'].iloc[i]
            # Calculate the return for this trade
            trade_return = (exit_price - entry_price) / entry_price
            total_return *= (1 + trade_return)
            cumulative_returns.append(total_return)
            entry_price = None  # Reset entry price after a trade
    
    # Ensure we close any open position on the last day
    if entry_price is not None:
        exit_price = df['Close'].iloc[-1]  # Sell at the last available price
        trade_return = (exit_price - entry_price) / entry_price
        total_return *= (1 + trade_return)
        cumulative_returns.append(total_return)
    
    # Convert cumulative_returns to a pandas Series for cummax() and other methods
    cumulative_returns = pd.Series(cumulative_returns)
    
    # Calculate the drawdown
    drawdown = (cumulative_returns / cumulative_returns.cummax()) - 1
    return drawdown.min()

def calmar_ratio(df, risk_free_rate=0.0433):
    annualized_return = yearly_return(df) * 100
    max_dd = max_drawdown(df) * 100
    if max_dd == 0:
        return np.nan  # Avoid division by zero
    print(annualized_return, risk_free_rate, max_dd)
    return (annualized_return - risk_free_rate * 100) / abs(max_dd)

def total_return(df):
    
    # Track the entry price (buy price)
    total_return = 1.0
    entry_price = None
    
    for i in range(1, len(df)):
        # When the position is 1 (buy), store the entry price
        if df['Position'].iloc[i] == 1:  # Buy signal
            entry_price = df['Close'].iloc[i]
        
        # When the position is -1 (sell), calculate return from the entry price
        elif df['Position'].iloc[i] == -1 and entry_price is not None:  # Sell signal
            exit_price = df['Close'].iloc[i]
            # Calculate return from buy to sell
            trade_return = (exit_price - entry_price) / entry_price
            total_return *= (1 + trade_return)
            entry_price = None  # Reset entry price after a trade
    
    # Ensure we close any open position on the last day
    if entry_price is not None:
        exit_price = df['Close'].iloc[-1]  # Sell at the last available price
        trade_return = (exit_price - entry_price) / entry_price
        total_return *= (1 + trade_return)
    
    # Subtract 1 to get total return (since we used cumulative product)
    return total_return - 1

def yearly_return(df):
    # Compute total return using your function
    total_ret = total_return(df)

    # Parse dates if not already datetime
    if not pd.api.types.is_datetime64_any_dtype(df['Date']):
        df['Date'] = pd.to_datetime(df['Date'])

    # Compute number of years in the data
    days = (df['Date'].iloc[-1] - df['Date'].iloc[0]).days + 1
    years = days / 365

    if years == 0:
        return np.nan  # Avoid division by zero

    # Annualize the return
    annualized_return = (1 + total_ret) ** (1 / years) - 1
    return annualized_return

def track_positions(df):
    position_changes = df[df['Position'] != 0]  # Filter to include only non-zero positions
    entry_exit_prices = []  # List to store the trade data
    
    entry_row = None  # To track the entry (buy) signal
    
    for i in range(len(position_changes)):
        row = position_changes.iloc[i]
        
        if row['Position'] == 1:  # A buy signal (long position)
            entry_row = row  # Store the entry signal
        elif row['Position'] == -1 and entry_row is not None:  # A sell signal (closing the position)
            exit_row = row
            profit = (exit_row['Close'] - entry_row['Close']) * entry_row['Position']  # Calculate profit
            
            entry_exit_prices.append({
                'Entry Date': entry_row['Date'],
                'Entry Price': entry_row['Close'],
                'Exit Date': exit_row['Date'],
                'Exit Price': exit_row['Close'],
                'Profit': profit
            })
            
            entry_row = None  # Reset entry_row after completing the trade
    
    # Convert the list of trades to a DataFrame
    entry_exit_df = pd.DataFrame(entry_exit_prices)
    
    return entry_exit_df
    
METRICS = {
    'sharpe_ratio': sharpe_ratio,
    'max_drawdown': max_drawdown,
    'calmar_ratio': calmar_ratio,
    'total_return': total_return,
    'yearly_return': yearly_return,
}