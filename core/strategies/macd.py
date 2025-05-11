from datetime import date, datetime, timedelta
import pandas as pd
from .abstract_strategy import Strategy

class MACDStrategy(Strategy):
    def __init__(self, fast: int = 12, slow: int = 26, signal: int = 9):
        self.fast = fast
        self.slow = slow
        self.signal = signal

    def calculate(self, df: pd.DataFrame, start_date: date) -> tuple[pd.DataFrame, dict[str, str], dict]:
        
        if self.fast >= self.slow:
            raise ValueError("Fast period must be less than slow period.")
        
        df = df.copy()
        # Calculate MACD line and signal line
        df["EMA_fast"] = df["Close"].ewm(span=self.fast, adjust=False).mean()
        df["EMA_slow"] = df["Close"].ewm(span=self.slow, adjust=False).mean()
        df["MACD"] = df["EMA_fast"] - df["EMA_slow"]
        df["MACD_Signal"] = df["MACD"].ewm(span=self.signal, adjust=False).mean()

        # Trading signal: Buy when MACD crosses above signal line, sell when it crosses below
        df["Signal"] = 0
        df.loc[(df["MACD"] > df["MACD_Signal"]) & (df["MACD"].shift(1) <= df["MACD_Signal"].shift(1)), "Signal"] = 1
        df.loc[(df["MACD"] < df["MACD_Signal"]) & (df["MACD"].shift(1) >= df["MACD_Signal"].shift(1)), "Signal"] = -1

        df["Position"] = df["Signal"].diff().fillna(0)

        df["Signal"] = df["Signal"].map({1: "Buy", -1: "Sell", 0: "Hold"})

        # Filter by start_date and reset index
        start_date = datetime.combine(start_date, datetime.min.time())
        df = df[df['Date'] >= start_date].reset_index(drop=True)

        return df, {}, {
            f"MACD Line ({self.fast}, {self.slow})": "MACD",
            f"Signal Line ({self.signal})": "MACD_Signal"
        }

    def get_required_data_range(self, start_date: date, end_date: date) -> tuple:
        required_start_date = start_date - timedelta(days=self.slow * 2)
        return required_start_date, end_date
