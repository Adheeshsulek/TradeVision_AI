import yfinance as yf

def get_data(symbol):

    df = yf.download(
        symbol,
        period="6mo",
        interval="1d",
        auto_adjust=True,
        group_by="column"
    )

    if hasattr(df.columns, "levels"):
        df.columns = df.columns.get_level_values(0)

    df.columns = [
        str(col).capitalize()
        for col in df.columns
    ]

    return df