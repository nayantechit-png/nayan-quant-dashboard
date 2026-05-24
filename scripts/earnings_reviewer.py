"""
Earnings Reviewer — NAS100 Earnings Filter
Fetches LIVE NAS100 price first, then reviews upcoming earnings.
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

PROMPT = f"""You are a prop trading risk manager specialising in NAS100.

{live}

Current NAS100: {nas100} — use this as the baseline for all move calculations.

Task: Review upcoming earnings releases that will significantly move NAS100.

Focus on top NAS100 components: Apple (AAPL), Microsoft (MSFT), Nvidia (NVDA),
Amazon (AMZN), Alphabet (GOOGL), Meta (META), Tesla (TSLA), Broadcom (AVGO).

Provide:
1. EARNINGS DATES this week and next 2 weeks
2. EXPECTED % MOVE for each (based on options pricing / historical avg)
3. EXPECTED NAS100 POINT MOVE for each (based on current level {nas100})
4. NAS100 BLOCK DATES — specific days prop traders should NOT trade NAS100
5. Overall NAS100 risk level this week (LOW / MEDIUM / HIGH)
6. Recommended action: trade NAS100 this week? YES / NO / REDUCED SIZE

Format as clean Telegram message with emojis.
Start with: 📊 *NAS100 EARNINGS FILTER — [today's date]*"""

msg  = client.messages.create(model="claude-sonnet-4-5", max_tokens=1024, messages=[{"role":"user","content":PROMPT}])
text = msg.content[0].text
send(text)
print(text)
