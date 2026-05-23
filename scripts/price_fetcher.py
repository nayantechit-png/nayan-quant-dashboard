"""
Live price fetcher — pulls current market prices before Claude analysis.
Uses yfinance (free, no API key needed).
"""
import subprocess, sys

# Auto-install yfinance if missing
try:
    import yfinance as yf
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "yfinance", "-q"])
    import yfinance as yf

def get_live_prices():
    """Returns dict of current prices for all tracked instruments."""
    tickers = {
        "XAUUSD": "GC=F",      # Gold futures
        "EURUSD": "EURUSD=X",
        "GBPUSD": "GBPUSD=X",
        "USDJPY": "USDJPY=X",
        "AUDUSD": "AUDUSD=X",
        "NZDUSD": "NZDUSD=X",
        "NAS100": "NQ=F",       # Nasdaq futures
        "BTCUSD": "BTC-USD",
    }

    prices = {}
    for name, symbol in tickers.items():
        try:
            ticker = yf.Ticker(symbol)
            hist   = ticker.history(period="2d", interval="1h")
            if not hist.empty:
                price = round(hist["Close"].iloc[-1], 4)
                prev  = round(hist["Close"].iloc[0], 4)
                chg   = round(((price - prev) / prev) * 100, 2)
                prices[name] = {"price": price, "change_pct": chg}
            else:
                prices[name] = {"price": "N/A", "change_pct": 0}
        except Exception as e:
            prices[name] = {"price": "N/A", "change_pct": 0}

    return prices

def format_prices(prices: dict) -> str:
    """Formats prices as a clean string to inject into Claude prompts."""
    lines = ["LIVE MARKET PRICES (real-time — use these exact levels):"]
    for name, data in prices.items():
        p = data["price"]
        c = data["change_pct"]
        arrow = "▲" if c > 0 else "▼" if c < 0 else "→"
        lines.append(f"  {name}: {p}  {arrow} {c:+.2f}% today")
    return "\n".join(lines)

if __name__ == "__main__":
    prices = get_live_prices()
    print(format_prices(prices))
