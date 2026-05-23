"""
Earnings Reviewer — NAS100 Earnings Filter
Checks which major tech earnings are this week/next week.
Flags days to avoid trading NAS100. Result → Telegram
"""
import os, anthropic
from telegram_sender import send

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

PROMPT = """You are a prop trading risk manager specialising in NAS100.

Task: Review upcoming earnings releases that will significantly move NAS100.

Focus on top NAS100 components: Apple (AAPL), Microsoft (MSFT), Nvidia (NVDA),
Amazon (AMZN), Alphabet (GOOGL), Meta (META), Tesla (TSLA), Broadcom (AVGO).

Provide:
1. Earnings dates this week and next 2 weeks
2. Expected % move for each (based on options pricing / historical)
3. NAS100 BLOCK DATES — specific days prop traders should NOT trade NAS100
4. Overall NAS100 risk level this week (LOW / MEDIUM / HIGH)
5. Recommended action: trade NAS100 this week? YES / NO / REDUCED SIZE

Format as clean Telegram message with emojis.
Start with: 📅 *NAS100 EARNINGS FILTER*"""

msg  = client.messages.create(model="claude-sonnet-4-5", max_tokens=1024, messages=[{"role":"user","content":PROMPT}])
text = msg.content[0].text
send(text)
print(text)
