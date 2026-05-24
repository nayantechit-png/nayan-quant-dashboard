// ═══════════════════════════════════════════════
//  NAYAN QUANT — Dashboard App Logic
//  Buttons open Telegram with the command pre-filled.
//  The bot running on your Mac handles all AI calls.
//  No API keys stored here — everything stays local.
// ═══════════════════════════════════════════════

const COMMANDS = {
  market:   { label: "Market Researcher",  cmd: "/market"   },
  earnings: { label: "Earnings Reviewer",  cmd: "/earnings" },
  fx:       { label: "FX Analysis",        cmd: "/fx"       },
  model:    { label: "Performance Model",  cmd: "/model"    },
  calendar: { label: "Earnings Calendar",  cmd: "/calendar" },
  risk:     { label: "Risk Report",        cmd: "/risk"     },
};

// Bot username — set in config.js (no secrets needed)
const BOT = (typeof CONFIG !== "undefined" && CONFIG.TELEGRAM_BOT_USERNAME)
  ? CONFIG.TELEGRAM_BOT_USERNAME.replace("@", "")
  : "nayanfinancialbot";

// ── Clock ─────────────────────────────────────
function updateClock() {
  const now = new Date();
  document.getElementById("clock").textContent =
    now.toUTCString().slice(17, 25) + " UTC";
}
setInterval(updateClock, 1000);
updateClock();

// ── Log ───────────────────────────────────────
function log(msg, type = "info") {
  const body  = document.getElementById("logBody");
  const now   = new Date().toUTCString().slice(17, 25);
  const entry = document.createElement("div");
  entry.className = `log-entry log-${type}`;
  entry.innerHTML = `<span class="log-time">${now}</span>${msg}`;
  body.prepend(entry);
}

function clearLog() {
  document.getElementById("logBody").innerHTML =
    '<div class="log-entry log-info">Log cleared.</div>';
}

// ── Last run times ────────────────────────────
function loadRunTimes() {
  Object.keys(COMMANDS).forEach(key => {
    const saved = localStorage.getItem(`lastRun_${key}`);
    const el = document.getElementById(`last-${key}`);
    if (saved && el) el.textContent = `Last: ${saved}`;
  });
}

function saveRunTime(key) {
  const t = new Date().toLocaleString("en-GB", { timeZone: "UTC", hour12: false })
              .replace(",", "") + " UTC";
  localStorage.setItem(`lastRun_${key}`, t);
  const el = document.getElementById(`last-${key}`);
  if (el) el.textContent = `Last: ${t}`;
}

// ── Open Telegram with command pre-filled ─────
function openTelegram(telegramCmd) {
  const encoded = encodeURIComponent(telegramCmd);
  const url = `https://t.me/${BOT}?text=${encoded}`;
  window.open(url, "_blank");
}

// ── Run Single Command ────────────────────────
function runCommand(key) {
  const cmd  = COMMANDS[key];
  const btn  = document.getElementById(`btn-${key}`);
  const card = document.getElementById(`card-${key}`);
  const prog = document.getElementById(`prog-${key}`);

  // UI: flash running state
  if (btn)  btn.disabled = true;
  if (card) card.classList.add("running");
  if (prog) prog.style.width = "60%";
  log(`Opening Telegram → ${cmd.label} ...`, "running");

  // Open Telegram with the command pre-filled
  openTelegram(cmd.cmd);

  // After short delay, mark as "sent"
  setTimeout(() => {
    if (card) {
      card.classList.remove("running");
      card.classList.add("success");
    }
    if (prog) prog.classList.add("full");
    saveRunTime(key);
    log(`📲 ${cmd.label} sent to Telegram — tap Send in the app`, "success");

    setTimeout(() => {
      if (card) card.classList.remove("success");
      if (prog) { prog.style.width = "0%"; prog.classList.remove("full"); }
    }, 4000);

    if (btn) {
      btn.disabled = false;
    }
  }, 800);
}

// ── Run All ───────────────────────────────────
function runAll() {
  log("⚡ Opening Telegram for /runall ...", "running");
  openTelegram("/runall");
  log("📲 /runall sent — tap Send in Telegram. All 6 results incoming.", "success");
}

// ── Init ──────────────────────────────────────
loadRunTimes();
log(`Dashboard ready — @${BOT} connected. Click any button to trigger via Telegram.`, "info");
