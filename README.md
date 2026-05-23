# 🤖 Nayan Quant — AI Trading Dashboard

A GitHub Pages dashboard that sends commands to your local Telegram bot.  
All AI analysis runs **on your Mac** — no API keys ever leave your machine.

---

## How It Works

```
[Dashboard Button] → opens Telegram with command pre-filled
       ↓
[You press Send in Telegram]
       ↓
[Bot on your Mac] → calls Claude AI → sends result back to Telegram
```

No GitHub secrets. No API keys online. Everything local.

---

## Setup — 3 Steps

### Step 1 — Push site to GitHub Pages

```bash
cd /Users/haevaymay/Desktop/CLAUDE/NayanQuant-Site

git init
git add .
git commit -m "Nayan Quant Dashboard"
git remote add origin https://github.com/YOUR_USERNAME/nayan-quant-dashboard.git
git branch -M main
git push -u origin main
```

Then: repo → **Settings → Pages → Source: main / root → Save**

Your site: `https://YOUR_USERNAME.github.io/nayan-quant-dashboard/`

### Step 2 — Start the bot on your Mac

```bash
export TELEGRAM_BOT_TOKEN="your_bot_token"
export TELEGRAM_CHAT_ID="your_chat_id"
export ANTHROPIC_API_KEY="your_anthropic_key"   # stays on your Mac only

nohup python3 /Users/haevaymay/Desktop/CLAUDE/NayanQuant-Site/bot/telegram_bot.py \
  > /tmp/nayanbot.log 2>&1 &
```

### Step 3 — Use the dashboard

1. Open your GitHub Pages URL
2. Click any button → Telegram opens with the command pre-filled
3. Press **Send** in Telegram
4. Result arrives in Telegram from the bot within ~30 seconds

---

## Bot Commands (direct in Telegram)

| Command | What it does |
|---------|-------------|
| `/help` | Show full menu |
| `/run market` | Weekly macro bias |
| `/run earnings` | NAS100 earnings filter |
| `/run fx` | FX carry + vol session bias |
| `/run model` | Performance diagnosis |
| `/run calendar` | 2-week earnings calendar |
| `/run risk` | GoatFunded + FTMO health check |
| `/runall` | Run all 6 |
| `/status` | Bot online status |

---

## Project Structure

```
NayanQuant-Site/
├── index.html              ← Dashboard UI
├── css/style.css           ← Dark trading theme
├── js/
│   ├── config.js           ← Bot username only (safe to commit)
│   └── app.js              ← Button → Telegram link logic
├── scripts/
│   ├── telegram_sender.py  ← Shared send utility
│   ├── market_researcher.py
│   ├── earnings_reviewer.py
│   ├── fx_analysis.py
│   ├── model_builder.py
│   ├── sp_global.py
│   └── risk_report.py
├── bot/
│   └── telegram_bot.py     ← Run this on your Mac
└── requirements.txt
```

---

*⚡ Powered by Claude AI — runs locally, zero cloud exposure*
