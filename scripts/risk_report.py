"""
Risk Report — Daily Prop Account Health Check
Checks GoatFunded + FTMO rule compliance and SafeGuard status.
Result → Telegram
"""
import os, anthropic
from telegram_sender import send

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

PROMPT = """You are a prop trading risk manager specialising in FTMO and GoatFunded funded challenges.

Perform a daily risk health check for the following prop accounts:

GOATFUNDED $100K (1-Step 2026):
- Profit Target: 10% ($10,000)
- Daily DD Limit: 4% ($4,000) from high watermark
- Max Overall DD: 6% ($6,000) — equity never below $94,000
- Float Loss Cap: 2% ($2,000) per trade idea
- Valid Trading Days: 3 minimum (each ≥ +0.5%)
- SafeGuard EA: monitoring with $2,000 halt trigger, 4h cooldown

FTMO $100K (Instant Funding):
- Profit Target: 10%
- Daily Loss Limit: 5% ($5,000)
- Max Overall Loss: 10% ($10,000)

KNOWN ISSUES:
- Recent -1001 pip day (20 losses in one day)
- BTCUSD single SL = -297 pips (too large)
- Win rate 25.9%, profit factor 0.23
- 22 open trades untracked

RISK CHECK — provide:
1. ACCOUNT STATUS: Green / Yellow / Red for each firm
2. DAILY DD USAGE estimate (% used today)
3. SAFEGUARD STATUS: Active / Standby
4. CRITICAL WARNINGS (anything near breach)
5. TODAY'S ACTION PLAN: what to do / avoid today
6. RECOMMENDED CHANGES to prevent another -1001 pip day

Format as clean Telegram message with emojis. Use 🟢 🟡 🔴 for status.
Start with: 🛡️ *DAILY RISK REPORT — [today's date]*"""

msg  = client.messages.create(model="claude-sonnet-4-5", max_tokens=1200, messages=[{"role":"user","content":PROMPT}])
text = msg.content[0].text
send(text)
print(text)
