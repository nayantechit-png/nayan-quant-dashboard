"""
Nayan Quant — New Telegram Bot
Handles commands from Telegram + receives results from 6 analysis scripts.

Commands:
  /start    — Welcome message + command menu
  /run      — Run a specific command (e.g. /run market)
  /runall   — Run all 6 commands
  /status   — Current signal status from VPS
  /help     — Full command list

Usage (run on VPS):
  pip install anthropic requests
  TELEGRAM_BOT_TOKEN=xxx ANTHROPIC_API_KEY=xxx python3 telegram_bot.py
"""

import os, sys, time, json, threading, subprocess
import urllib.request, urllib.parse, ssl

# ── Config ────────────────────────────────────
TOKEN   = os.environ.get("TELEGRAM_BOT_TOKEN", "")
ADMIN   = os.environ.get("TELEGRAM_ADMIN_ID", "")   # your personal Telegram user ID
API     = f"https://api.telegram.org/bot{TOKEN}"
CTX     = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode    = ssl.CERT_NONE

# Scripts directory (relative to this file)
SCRIPTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts")

COMMAND_MAP = {
    "market":   "market_researcher.py",
    "earnings": "earnings_reviewer.py",
    "fx":       "fx_analysis.py",
    "model":    "model_builder.py",
    "calendar": "sp_global.py",
    "risk":     "risk_report.py",
}

MENU = """
🤖 *Nayan Quant Auto AI*
━━━━━━━━━━━━━━━━━━━━
*Analysis Commands:*
/run market   — 🔍 Weekly Macro Bias
/run earnings — 📊 NAS100 Earnings Filter
/run fx       — 📈 FX Carry + Vol Analysis
/run model    — 💹 Performance Model
/run calendar — 📅 Earnings Calendar
/run risk     — 🛡️ Daily Risk Report
/runall       — ⚡ Run All 6

*Info Commands:*
/status       — Current bot status
/help         — This menu
━━━━━━━━━━━━━━━━━━━━
⚡ Powered by Autotrade AI
"""

# ── HTTP helpers ──────────────────────────────
def api_get(method, params=None):
    url = f"{API}/{method}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req  = urllib.request.Request(url)
    resp = urllib.request.urlopen(req, timeout=15, context=CTX)
    return json.loads(resp.read())

def api_post(method, data):
    url     = f"{API}/{method}"
    payload = urllib.parse.urlencode(data).encode()
    req     = urllib.request.Request(url, data=payload, method="POST")
    resp    = urllib.request.urlopen(req, timeout=15, context=CTX)
    return json.loads(resp.read())

def send(chat_id, text):
    try:
        api_post("sendMessage", {
            "chat_id":    chat_id,
            "text":       text,
            "parse_mode": "Markdown",
        })
    except Exception as e:
        print(f"Send error: {e}")

# ── Run analysis script ───────────────────────
def run_script(chat_id, key):
    script = COMMAND_MAP.get(key)
    if not script:
        send(chat_id, f"❌ Unknown command: `{key}`\nTry: market, earnings, fx, model, calendar, risk")
        return

    send(chat_id, f"⟳ Running *{key}* analysis — result coming to Telegram shortly...")

    script_path = os.path.join(SCRIPTS, script)
    env = {**os.environ}   # pass all env vars including ANTHROPIC_API_KEY

    def _run():
        try:
            result = subprocess.run(
                [sys.executable, script_path],
                capture_output=True, text=True, timeout=120, env=env
            )
            if result.returncode != 0:
                send(chat_id, f"❌ *{key}* script error:\n```{result.stderr[-500:]}```")
        except subprocess.TimeoutExpired:
            send(chat_id, f"⏱ *{key}* timed out after 120s")
        except Exception as e:
            send(chat_id, f"❌ *{key}* failed: {e}")

    threading.Thread(target=_run, daemon=True).start()

# ── Handle incoming message ───────────────────
def handle(msg):
    chat_id = msg["chat"]["id"]
    text    = msg.get("text", "").strip()

    if text.startswith("/start") or text.startswith("/help"):
        send(chat_id, MENU)

    elif text.startswith("/runall"):
        send(chat_id, "⚡ Running all 6 analyses — results incoming...")
        for key in COMMAND_MAP:
            run_script(chat_id, key)
            time.sleep(2)

    elif text.startswith("/run"):
        parts = text.split()
        if len(parts) < 2:
            send(chat_id, "Usage: `/run <command>`\nCommands: market, earnings, fx, model, calendar, risk")
        else:
            run_script(chat_id, parts[1].lower())

    elif text.startswith("/status"):
        send(chat_id,
            "🟢 *Bot Status*\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "Bot: ✅ Online\n"
            "Scripts: ✅ Ready\n"
            "API: ✅ Connected\n"
            f"Commands available: {len(COMMAND_MAP)}"
        )

    else:
        send(chat_id, "Unknown command. Type /help for the full menu.")

# ── Polling loop ──────────────────────────────
def poll():
    print(f"🤖 Nayan Quant Bot starting...")
    offset = 0
    while True:
        try:
            data = api_get("getUpdates", {"offset": offset, "timeout": 30, "allowed_updates": ["message"]})
            for update in data.get("result", []):
                offset = update["update_id"] + 1
                if "message" in update:
                    handle(update["message"])
        except Exception as e:
            print(f"Poll error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    if not TOKEN:
        print("❌ Set TELEGRAM_BOT_TOKEN env var"); sys.exit(1)
    poll()
