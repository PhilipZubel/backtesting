def run_backtest_with_inputs(engine, strategy_name, params):
    engine.strategy_name = strategy_name
    engine.strategy_params = params
    return engine.run_backtest()