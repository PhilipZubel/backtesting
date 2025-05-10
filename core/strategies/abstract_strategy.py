from datetime import date
import pandas as pd
from abc import ABC, abstractmethod

class Strategy(ABC):
    """
    Abstract base class for a trading strategy.
    All strategies should inherit from this class and implement the three abstract methods.
    """
    
    @abstractmethod
    def calculate(self, df: pd.DataFrame, start_date: date) -> tuple[pd.DataFrame, dict[str, str]]:
        """
        Perform the strategy calculation on the given data.

        :return: DataFrame with strategy indicators.
        """
        pass
    
    @abstractmethod
    def get_required_data_range(self, start_date: date, end_date: date) -> tuple:
        """
        Calculate and return the necessary start and end date range for the strategy.

        :param start_date: The start date of the requested data.
        :param end_date: The end date of the requested data.
        :return: Tuple with (required_start_date, end_date).
        """
        pass
    
    def set_params(self, **params) -> None:
        """
        Set the strategy parameters (self attributes).

        :param params: Dictionary of parameters to set as attributes.
        :return: None
        """
        for key, value in params.items():
            setattr(self, key, value)
