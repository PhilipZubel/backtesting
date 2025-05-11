import pandas as pd


def load_ticker_options(path: str = "core/utils/tickers.csv") -> dict:
    df = pd.read_csv(path)

    if "Symbol" not in df.columns or "Security" not in df.columns:
        raise ValueError(
            f"CSV must contain 'Symbol' and 'Security' columns. Found: {df.columns.tolist()}"
        )
    df["Label"] = df["Symbol"] + " – " + df["Security"]
    df = df.sort_values("Label")

    return dict(zip(df["Label"], df["Symbol"]))
