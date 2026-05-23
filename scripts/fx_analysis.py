"""
FX Analysis — Carry Trade + Vol Surface Check
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

PROMPT = f"""You are an FX carry trade and volatility specialist for prop trading.

{live}

Using the EXACT prices above (do not use any other price levels), analyse these pairs for today's trading session:
EURUSD, GBPUSD, NZDUSD, AUDUSD, USDJPY, XAUUSD

Provide:
1. CARRY TRADE RANKING — rank pairs by carry-to-vol attractiveness
2. VOL WARNING — flag any pair with elevated implied vol (avoid trading these)
3. SESSION BIAS per pair (BUY / SELL / AVOID) for today with entry zones based on current price
4. CORRELATION WARNINGS — any pairs moving in dangerous correlation today
5. SPREAD ALERT — any pairs with typically wide spreads at current session

Risk context: GoatFunded prop account — 4% daily DD limit, 2% float loss cap per trade.
Must avoid any pairs where a single 15-pip spike could trigger the 2% float cap.

Format as clean Telegram message with emojis.
Start with: 📈 *FX SESSION ANALYSIS — [today's date]*
Include current price for each pair in your analysis."""

msg  = client.messages.create(model="claude-sonnet-4-5", max_tokens=1024, messages=[{"role":"user","content":PROMPT}])
text = msg.content[0].text
send(text)
print(text)
