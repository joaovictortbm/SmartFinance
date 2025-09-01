import os
import finnhub
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv("FINNHUB_API_KEY")
os.environ["FINNHUB_API_KEY"] = api_key
finnhub_client = finnhub.Client(api_key=api_key)


TICKERS = [
    "AAPL", "MSFT", "TSLA", "GOOGL", "AMZN", "FB", "NFLX", "NVDA",
    "BABA", "INTC", "AMD", "PYPL", "DIS", "ORCL", "IBM", "ADBE",
    "CRM", "V", "MA", "BINANCE:BTCUSDT", "BINANCE:ETHUSDT",
    "BINANCE:SOLUSDT", "BINANCE:ADAUSDT", "BINANCE:XRPUSDT", "BINANCE:DOGEUSDT"
]


def generate_asset_summary():
    summary = ""

    for ticker in TICKERS:
        try:
            q = finnhub_client.quote(ticker)
            price = q['c']
            change = q['dp']
            high = q['h']
            low = q['l']
            open_ = q['o']
            prev_close = q['pc']

            line = f"{ticker}: Current ${price} ({change:.2f}%), High ${high}, Low ${low}, Open ${open_}, Prev Close ${prev_close}"

            if not ticker.startswith("BINANCE:"):
                recs = finnhub_client.recommendation_trends(ticker)
                if recs:
                    latest = recs[0]
                    line += f", Analysts: Buy {latest['buy']}, Hold {latest['hold']}, Sell {latest['sell']}, Strong Buy {latest['strongBuy']}, Strong Sell {latest['strongSell']}"

            summary += line + "\n"

        except Exception as e:
            summary += f"{ticker}: Error fetching data ({e})\n"

    return summary
