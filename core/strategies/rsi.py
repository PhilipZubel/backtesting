from datetime import date, datetime, timedelta
import pandas as pd
from .abstract_strategy import Strategy

class RSIStrategy(Strategy):
    def __init__(self, period: int = 14, lower: float = 30.0, upper: float = 70.0):
        self.period = period
        self.lower = lower
        self.upper = upper

    def calculate(self, df: pd.DataFrame, start_date: date) -> tuple[pd.DataFrame, dict[str, str], dict]:
        if not (0 < self.lower < self.upper < 100):
            raise ValueError("Lower and upper bounds must be between 0 and 100, with lower < upper.")
        
        df = df.copy()
        delta = df["Close"].diff()

        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)

        avg_gain = gain.rolling(window=self.period).mean()
        avg_loss = loss.rolling(window=self.period).mean()

        rs = avg_gain / avg_loss
        df["RSI"] = 100 - (100 / (1 + rs))

        # Generate signals: Buy when RSI < lower, sell when RSI > upper
        df["Signal"] = 0
        df.loc[df["RSI"] < self.lower, "Signal"] = 1   # Buy
        df.loc[df["RSI"] > self.upper, "Signal"] = -1  # Sell

        df["Position"] = df["Signal"].diff().fillna(0)

        # Convert signal to human-readable labels
        df["Signal"] = df["Signal"].map({1: "Buy", -1: "Sell", 0: "Hold"})

        # Filter by start_date and reset index
        start_date = datetime.combine(start_date, datetime.min.time())
        df = df[df['Date'] >= start_date].reset_index(drop=True)

        return df, {}, {f"RSI {self.period} Days": "RSI", 'red': self.lower, 'green': self.upper}

    def get_required_data_range(self, start_date: date, end_date: date) -> tuple:
        # We need at least `period` days of data before start
        required_start_date = start_date - timedelta(days=self.period * 2)
        return required_start_date, end_date
