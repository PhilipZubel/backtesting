import ta
from datetime import date, datetime, timedelta
import pandas as pd
from .abstract_strategy import Strategy


class ParabolicSARStrategy(Strategy):
    def calculate(
        self, df: pd.DataFrame, start_date: date
    ) -> tuple[pd.DataFrame, dict[str, str]]:
        df = df.copy()
        df["SAR"] = ta.trend.psar(
            df["High"], df["Low"], df["Close"], step=0.02, max_step=0.2
        )

        df["Signal"] = 0
        df.loc[df["Close"] > df["SAR"], "Signal"] = 1
        df.loc[df["Close"] < df["SAR"], "Signal"] = -1
        df["Position"] = df["Signal"].diff().fillna(0)
        df["Signal"] = df["Signal"].map({1: "Buy", -1: "Sell", 0: "Hold"})

        start_date = datetime.combine(start_date, datetime.min.time())
        df = df[df["Date"] >= start_date].reset_index(drop=True)

        return df, {"Parabolic SAR": "SAR"}, {}

    def get_required_data_range(self, start_date: date, end_date: date) -> tuple:
        return start_date - timedelta(days=40), end_date
