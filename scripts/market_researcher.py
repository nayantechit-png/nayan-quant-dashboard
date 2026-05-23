"""
Market Researcher — Weekly Macro Bias
Fetches LIVE prices first, then sends to Claude for analysis.
Result → Telegram
"""
import os, sys, anthropic
sys.path.insert(0, os.path.dirname(__file__))
from telegram_sender import send
from price_fetcher import get_live_prices, format_prices

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

# ── Fetch live prices ──────────────────────────────────
prices = get_live_prices()
live   = format_prices(prices)

PROMPT = f"""You are a macro research analyst specialising in FX and commodities for prop trading.

{live}

Using the EXACT current prices above, provide a weekly macro bias report for:
EURUSD, GBPUSD, XAUUSD, NAS100, USDJPY, AUDUSD, NZDUSD

For each instrument provide:
- Current price (use the live price given above — do not invent levels)
- Weekly bias: BULLISH / BEARISH / NEUTRAL
- Key level to watch (support/resistance near the current price)
- 1 key macro driver this week

Then provide:
TOP 3 SETUPS — best risk/reward opportunities this week with:
- Entry zone (near current price ± realistic range)
- Target
- Stop loss
- Rationale

Format as clean Telegram message with emojis.
Start with: 🔍 *WEEKLY MACRO BIAS — [today's date]*"""

msg  = client.messages.create(model="claude-sonnet-4-5", max_tokens=1024, messages=[{"role":"user","content":PROMPT}])
text = msg.content[0].text
send(text)
print(text)
