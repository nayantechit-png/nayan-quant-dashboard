"""
S&P Global Earnings Calendar — NAS100 Block Dates
Generates NAS100 trading block dates for next 2 weeks.
Result → Telegram
"""
import os, anthropic
from telegram_sender import send

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

PROMPT = """You are an equity research analyst specialising in US tech stocks and NAS100.

Generate a complete earnings calendar for NAS100 for the next 2 weeks.

Focus on highest-impact components:
Tier 1 (>3% NAS100 move expected): NVDA, AAPL, MSFT, GOOGL, AMZN, META, TSLA
Tier 2 (1-3% move): AVGO, AMD, QCOM, INTC, NFLX, ADBE, CRM, ORCL

For each company reporting:
- Date & time (before/after market)
- Expected EPS vs previous
- Implied move % (options market expectation)
- Impact on NAS100 (HIGH / MEDIUM / LOW)

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
