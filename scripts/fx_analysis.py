"""
FX Analysis — Carry Trade + Vol Surface Check
Daily pre-session analysis. Identifies best carry pairs,
flags elevated vol, gives session bias. Result → Telegram
"""
import os, anthropic
from telegram_sender import send

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

PROMPT = """You are an FX carry trade and volatility specialist for prop trading.

Analyse these pairs for today's trading session:
EURUSD, GBPUSD, NZDUSD, AUDUSD, USDJPY, XAUUSD

Provide:
1. CARRY TRADE RANKING — rank pairs by carry-to-vol attractiveness
2. VOL WARNING — flag any pair with elevated implied vol (avoid trading these)
3. SESSION BIAS per pair (BUY / SELL / AVOID) for today
4. CORRELATION WARNINGS — any pairs moving in dangerous correlation today
5. SPREAD ALERT — any pairs with typically wide spreads at current session

Risk context: GoatFunded prop account — 4% daily DD limit, 2% float loss cap per trade.
Must avoid any pairs where a single 15-pip spike could trigger the 2% float cap.

Format as clean Telegram message with emojis.
Start with: 📈 *FX SESSION ANALYSIS — [today's date]*"""

msg  = client.messages.create(model="claude-sonnet-4-5", max_tokens=1024, messages=[{"role":"user","content":PROMPT}])
text = msg.content[0].text
send(text)
print(text)
