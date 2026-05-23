"""
Market Researcher — Weekly Macro Bias
Triggered every Sunday. Analyses USD trend, risk-on/off, key levels.
Result → Telegram
"""
import os, anthropic
from telegram_sender import send

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

PROMPT = """You are a professional FX and index trader analyst.
Analyse the current macro environment for prop trading this week.

Instruments: EURUSD, GBPUSD, XAUUSD (Gold), NAS100, USDJPY, AUDUSD, NZDUSD

Provide:
1. USD Bias (Bullish/Bearish/Neutral) with key reason
2. Risk Sentiment (Risk-On / Risk-Off / Mixed)
3. Per-instrument weekly bias (BUY / SELL / AVOID) with 1-line reason
4. Top 3 setups to watch this week with entry zone
5. Key events/data releases to avoid trading around

Format as a clean Telegram message with emojis. Keep it concise — traders need fast actionable info.
Start with: 📊 *WEEKLY MACRO BIAS — [current week dates]*"""

msg  = client.messages.create(model="claude-sonnet-4-5", max_tokens=1024, messages=[{"role":"user","content":PROMPT}])
text = msg.content[0].text
send(text)
print(text)
