import inspect

from .abstract_strategy import Strategy
from .sma_crossover import SMACrossover
from .buy_and_hold import BuyAndHold
from .rsi import RSIStrategy
from .macd import MACDStrategy
from .boillinger import BollingerBandsStrategy

STRATEGIES: dict[str, Strategy] = {
    "SMA Crossover": SMACrossover,
    "Buy and Hold": BuyAndHold,
    "RSI Strategy": RSIStrategy,
    "MACD Strategy": MACDStrategy,
    "Bollinger Bands": BollingerBandsStrategy,
}

def get_strategy(name: str) -> Strategy:
    try:
        return STRATEGIES[name]
    except KeyError:
        raise ValueError(f"Unknown strategy: {name}")

def get_strategy_params(strategy_class):
    init_signature = inspect.signature(strategy_class.__init__)
    params = {}
    
    for name, param in init_signature.parameters.items():
        if name == "self":
            continue  # Skip the 'self' parameter
        if name == "args" or name == "kwargs":
            continue
        
        annotation = param.annotation
        default = param.default

        param_type = annotation if annotation != inspect._empty else str  # Default to 'str' if annotation is not provided
        default_val = default if default != inspect._empty else None  # Default value is None if not provided

        params[name] = {
            "type": param_type,
            "default": default_val,
        }

    return params
