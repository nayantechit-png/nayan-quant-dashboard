"""
Performance Model Builder — Weekly P&L Analysis
Analyses trade stats and recommends system adjustments.
Result → Telegram
"""
import os, anthropic
from telegram_sender import send

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

# ── Load live stats from DB if available, else use last known ──
STATS = {
    "total_trades": 49,
    "wins": 7,
    "losses": 20,
    "open": 22,
    "net_pips": -924,
    "profit_factor": 0.23,
    "best_pair": "XAUUSD +149p (5W/3L)",
    "worst_day": "2026-05-21 -1001p (5W/20L)",
    "avg_tp_pips": 124.6,
    "avg_sl_pips": 51.3,
    "rr_ratio": 2.43,
    "account_size": 100000,
    "daily_dd_limit_pct": 4.0,
    "max_dd_pct": 6.0,
}

PROMPT = f"""You are a quantitative trading system analyst.

Analyse this prop trading system performance and recommend improvements:

CURRENT STATS (Last 30 days):
- Total trades: {STATS['total_trades']} ({STATS['wins']} wins / {STATS['losses']} losses / {STATS['open']} open)
- Win rate: {STATS['wins']/(STATS['wins']+STATS['losses'])*100:.1f}%
- Net pips: {STATS['net_pips']}
- Profit factor: {STATS['profit_factor']}
- Avg TP: {STATS['avg_tp_pips']} pips | Avg SL: {STATS['avg_sl_pips']} pips | R:R = 1:{STATS['rr_ratio']}
- Best: {STATS['best_pair']}
- Worst day: {STATS['worst_day']}
- Account: ${STATS['account_size']:,} | Daily DD: {STATS['daily_dd_limit_pct']}% | Max DD: {STATS['max_dd_pct']}%

Provide:
1. DIAGNOSIS — what's causing the poor performance
2. BREAKEVEN WIN RATE needed for this R:R
3. CONFIDENCE THRESHOLD recommendation (currently fires at 7/10)
4. MAX DAILY TRADES recommendation (currently unlimited)
5. PAIRS TO DISABLE (losing pairs)
6. POSITION SIZING adjustment
7. EXPECTED improvement if recommendations followed

Format as clean Telegram message with emojis.
Start with: 💹 *PERFORMANCE MODEL — WEEKLY REVIEW*"""

msg  = client.messages.create(model="claude-sonnet-4-5", max_tokens=1200, messages=[{"role":"user","content":PROMPT}])
text = msg.content[0].text
send(text)
print(text)
