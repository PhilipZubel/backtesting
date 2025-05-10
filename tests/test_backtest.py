# import pytest
# import pandas as pd
# from strategies.sma_crossover import sma_crossover
# from core.backtest_engine import backtest_strategy

# def test_sma_crossover():
#     data = pd.DataFrame({
#         "Close": [100, 102, 104, 106, 108, 110, 112, 114, 116, 118]
#     })
#     df = sma_crossover(data)
#     assert "Signal" in df.columns
#     assert df["Signal"].iloc[0] == 0  # No signal on first day

# def test_backtest_strategy():
#     data = pd.DataFrame({
#         "Close": [100, 102, 104, 106, 108],
#         "Signal": [0, 1, 1, 0, 1]
#     })
#     df, total_return, sharpe = backtest_strategy(data)
#     assert isinstance(total_return, float)
#     assert isinstance(sharpe, float)
#     assert total_return >= -1  # Total return should not be less than -100%
#     assert sharpe >= -1  # Sharpe ratio should not be less than -1
#     assert df["Returns"].iloc[0] == 0  # No returns on first day
#     assert df["Strategy_Returns"].iloc[0] == 0  # No strategy returns on first day