import pandas as pd

from .utils import load_ticker_options
from .strategies import STRATEGIES, get_strategy, get_strategy_params, Strategy
from .data import DataLoader
from .metrics import METRICS

class BacktestingEngine:
    def __init__(self):
        self.start_date = None
        self.end_date = None
        self.ticker = None
        self.strategy_name = None
        self.strategy_params = None
        self._strategy = None
        self._data_loader = DataLoader()
    
    def get_tickets(self):
        return load_ticker_options()
    
    def get_strategies(self):
        return sorted(list(STRATEGIES.keys()))
    
    def get_strategy_params(self):
        self._strategy: Strategy = get_strategy(self.strategy_name)()
        return get_strategy_params(self._strategy)
        
    def run_backtest(self):
        self._strategy.set_params(**self.strategy_params)
        start_date, end_date = self._strategy.get_required_data_range(self.start_date, self.end_date)
        data = self._data_loader.load(self.ticker, start_date, end_date)
        results = self._strategy.calculate(data, self.start_date)
        return results
    
    def get_metrics(self, results: pd.DataFrame) -> dict:
        return {metric: METRICS[metric](results) for metric in METRICS}
        

    
        
        