from datetime import date, datetime, timedelta
import pandas as pd
from .abstract_strategy import Strategy

class SMACrossover(Strategy):
    def __init__(self, short: int = 10, long: int = 50):
        if short >= long:
            raise ValueError("Short period must be smaller than the long period.")
        self.short = short
        self.long = long

    def calculate(self, df: pd.DataFrame, start_date: date) -> tuple[pd.DataFrame, dict[str, str]]:
        df = df.copy()
        df["SMA_Short"] = df["Close"].rolling(window=self.short).mean()
        df["SMA_Long"] = df["Close"].rolling(window=self.long).mean()
        df["Signal"] = 0
        df.loc[self.short:, "Signal"] = (df.loc[self.short:, "SMA_Short"] > df.loc[self.short:, "SMA_Long"]).astype(int)
        
        df["Position"] = df["Signal"].diff().fillna(0)
        df["Signal"] = df["Signal"].map({0: "Hold", 1: "Buy"})
        
        # Filter by start_date and reset index
        start_date = datetime.combine(start_date, datetime.min.time())
        df = df[df['Date'] >= start_date].reset_index(drop=True)
        
        return df, {
                f"SMA Short {self.short} Days":  "SMA_Short",
                f"SMA Long {self.long} Days":  "SMA_Long",
            }

    def get_required_data_range(self, start_date: date, end_date: date) -> tuple:
        required_start_date = start_date - timedelta(days=self.long)
        return required_start_date, end_date
