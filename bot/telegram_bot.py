"""
Nayan Quant — Telegram Bot
Each command is a single clickable hyperlink in Telegram.

Commands:
  /start    — Welcome message + command menu
  /market   — Weekly Macro Bias
  /earnings — NAS100 Earnings Filter
  /fx       — FX Carry + Vol Analysis
  /model    — Performance Model
  /calendar — Earnings Calendar
  /risk     — Daily Risk Report
  /runall   — Run all 6
  /status   — Current bot status
  /help     — Full command list
"""

import os, sys, time, json, threading, subprocess
import urllib.request, urllib.parse, ssl

# ── Config ────────────────────────────────────
TOKEN   = os.environ.get("TELEGRAM_BOT_TOKEN", "")
ADMIN   = os.environ.get("TELEGRAM_ADMIN_ID", "")
API     = f"https://api.telegram.org/bot{TOKEN}"
CTX     = ssl.create_default_context()
CTX.check_hostname = False
CTX.verify_mode    = ssl.CERT_NONE

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
/market   — 🔍 Weekly Macro Bias
/earnings — 📊 NAS100 Earnings Filter
/fx       — 📈 FX Carry + Vol Analysis
/model    — 💹 Performance Model
/calendar — 📅 Earnings Calendar
/risk     — 🛡️ Daily Risk Report
/runall   — ⚡ Run All 6

*Info Commands:*
/status   — Current bot status
/help     — This menu
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
        send(chat_id, f"❌ Unknown command: `{key}`")
        return

    send(chat_id, f"⟳ Running *{key}* analysis — result coming shortly...")

    script_path = os.path.join(SCRIPTS, script)
    env = {**os.environ}

    def _run():
        try:
            result = subprocess.run(
                [sys.executable, script_path],
                capture_output=True, text=True, timeout=180, env=env
            )
            if result.returncode != 0:
                send(chat_id, f"❌ *{key}* error:\n```{result.stderr[-500:]}```")
        except subprocess.TimeoutExpired:
            send(chat_id, f"⏱ *{key}* timed out after 180s")
        except Exception as e:
            send(chat_id, f"❌ *{key}* failed: {e}")

    threading.Thread(target=_run, daemon=True).start()

# ── Handle incoming message ───────────────────
def handle(msg):
    chat_id = msg["chat"]["id"]
    text    = msg.get("text", "").strip().lower()

    # Strip bot username suffix (e.g. /market@nayanfinancialbot)
    text = text.split("@")[0]

    if text in ("/start", "/help"):
        send(chat_id, MENU)

    elif text == "/runall":
        send(chat_id, "⚡ Running all 6 analyses — results incoming...")
        for key in COMMAND_MAP:
            run_script(chat_id, key)
            time.sleep(2)

    elif text == "/status":
        send(chat_id,
            "🟢 *Bot Status*\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "Bot: ✅ Online\n"
            "Scripts: ✅ Ready\n"
            "API: ✅ Connected\n"
            f"Commands: {len(COMMAND_MAP)} available"
        )

    elif text in ("/market", "/earnings", "/fx", "/model", "/calendar", "/risk"):
        key = text[1:]  # strip leading /
        run_script(chat_id, key)

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
