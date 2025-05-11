from datetime import date, datetime, timedelta
import pandas as pd
from .abstract_strategy import Strategy


class BollingerBandsStrategy(Strategy):
    def __init__(self, period: int = 20, stddev: float = 2.0):
        self.period = period
        self.stddev = stddev

    def calculate(
        self, df: pd.DataFrame, start_date: date
    ) -> tuple[pd.DataFrame, dict[str, str]]:
        if self.period <= 0:
            raise ValueError("Period must be a positive integer.")
        if self.stddev <= 0:
            raise ValueError("Standard deviation multiplier must be a positive number.")
        df = df.copy()
        df["MA"] = df["Close"].rolling(window=self.period).mean()
        df["STD"] = df["Close"].rolling(window=self.period).std()
        df["Upper"] = df["MA"] + self.stddev * df["STD"]
        df["Lower"] = df["MA"] - self.stddev * df["STD"]

        df["Signal"] = 0
        df.loc[df["Close"] < df["Lower"], "Signal"] = 1  # Buy
        df.loc[df["Close"] > df["Upper"], "Signal"] = -1  # Sell
        df["Position"] = df["Signal"].diff().fillna(0)
        df["Signal"] = df["Signal"].map({1: "Buy", -1: "Sell", 0: "Hold"})

        start_date = datetime.combine(start_date, datetime.min.time())
        df = df[df["Date"] >= start_date].reset_index(drop=True)

        return (
            df,
            {
                f"BB MA {self.period}": "MA",
                "Upper Band": "Upper",
                "Lower Band": "Lower",
            },
            {},
        )

    def get_required_data_range(self, start_date: date, end_date: date) -> tuple:
        required_start = start_date - timedelta(days=self.period * 2)
        return required_start, end_date
