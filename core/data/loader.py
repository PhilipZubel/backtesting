import yfinance as yf
import pandas as pd
from datetime import date, timedelta

class DataLoadError(Exception):
    """Raised when stock data cannot be loaded."""
    pass

class DataLoader:
    def __init__(self):
        pass

    def _validate_dates(self, start_date: date, end_date: date) -> None:
        today = date.today()
        
        if start_date >= today:
            raise ValueError("Start date must be before today's date.")
        if end_date > today:
            raise ValueError("End date cannot be after today's date.")
        if start_date >= end_date:
            raise ValueError("Start date must be before end date.")

    def load(self, ticker: str, start_date: date, end_date: date) -> pd.DataFrame:
        ticker = ticker.upper()
        self._validate_dates(start_date, end_date)
        
        total_days = (end_date - start_date).days
        buffer_days = int(total_days * 0.20)
        
        adjusted_start_date = start_date - timedelta(days=buffer_days)
        data = yf.download(ticker, start=adjusted_start_date, end=end_date)

        if data.empty:
            raise DataLoadError(f"No data found for ticker '{ticker}'.")
        
        if isinstance(data.columns, pd.MultiIndex):
            data.columns = [col[0] for col in data.columns]  # Take just 'Close', 'Open', etc.

        data.reset_index(inplace=True)

        return data
