from datetime import date, datetime
import pandas as pd
from .abstract_strategy import Strategy

class BuyAndHold(Strategy):
    def __init__(self):
        pass

    def calculate(self, df: pd.DataFrame, start_date: date) -> tuple[pd.DataFrame, dict[str, str], dict]:
        df = df.copy()

        # Filter by start_date first
        start_date_dt = datetime.combine(start_date, datetime.min.time())
        df = df[df['Date'] >= start_date_dt].reset_index(drop=True)

        # Set signals and position
        df["Signal"] = "Hold"
        df["Position"] = 0

        if not df.empty:
            df.loc[0, "Signal"] = "Buy"
            df.loc[0, "Position"] = 1  # Enter position on the first day

        return df, {}, {}


    def get_required_data_range(self, start_date: date, end_date: date) -> tuple:
        # The strategy requires all data from the start date
        return start_date, end_date
