"""
S&P Global Earnings Calendar — NAS100 Block Dates
Fetches LIVE NAS100 price first, then generates 2-week earnings calendar.
Result → Telegram
"""
import os, sys, anthropic
sys.path.insert(0, os.path.dirname(__file__))
from telegram_sender import send
from price_fetcher import get_live_prices, format_prices

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

# ── Live prices ────────────────────────────────
prices = get_live_prices()
live   = format_prices(prices)
nas100 = prices.get("NAS100", {}).get("price", "N/A")
nas_chg = prices.get("NAS100", {}).get("change_pct", 0)

PROMPT = f"""You are an equity research analyst specialising in US tech stocks and NAS100.

{live}

Current NAS100 level: {nas100} ({nas_chg:+.2f}% today)

Generate a complete earnings calendar for NAS100 for the next 2 weeks.
Use today's NAS100 price of {nas100} as the baseline for impact calculations.

Focus on highest-impact components:
Tier 1 (>3% NAS100 move expected): NVDA, AAPL, MSFT, GOOGL, AMZN, META, TSLA
Tier 2 (1-3% move): AVGO, AMD, QCOM, INTC, NFLX, ADBE, CRM, ORCL

For each company reporting:
- Date & time (before/after market)
- Expected EPS vs previous
- Implied move % (options market expectation)
- Impact on NAS100 in points (based on current level {nas100})
- Impact rating: HIGH / MEDIUM / LOW

Then provide:
BLOCK TRADE DATES — specific dates to avoid all NAS100 trading
(day before + day of + day after major Tier 1 earnings)

SAFE DAYS — days with no major tech earnings = green light for NAS100

Format as clean Telegram message with emojis and a clear calendar.
Start with: 📅 *NAS100 EARNINGS CALENDAR — Next 2 Weeks*"""

msg  = client.messages.create(model="claude-sonnet-4-5", max_tokens=1200, messages=[{"role":"user","content":PROMPT}])
text = msg.content[0].text
send(text)
print(text)
