#!/usr/bin/env python3
"""
JARVIS — Autonomous 24/7 Watcher Engine
Powered by Mistral Free API (1 req/s · 1B tokens/month)
Monitors, Researches, Flags Intelligence → Telegram Alerts
"""

import json
import os
import sys
import time
import signal
import urllib.request as req
import urllib.parse
from datetime import datetime, timezone, timedelta
from pathlib import Path

# ===== CONFIG =====
MISTRAL_API_KEY = os.environ.get("MISTRAL_API_KEY", "R2pBYB7SkpaTgXCERyIoaSWFVrWYMzZa")
TELEGRAM_BOT_TOKEN = "8319377738:AAFBsPbuzhAdgCcokRl0tZFwwSErRSgiZMg"
TELEGRAM_CHAT_ID = "5998285479"
MISTRAL_URL = "https://api.mistral.ai/v1/chat/completions"
MISTRAL_MODEL = "mistral-small-latest"
RATE_LIMIT_SEC = 1.1  # 1 req/s limit buffer
STATE_FILE = Path("/home/ubuntu/.openclaw/workspace/memory/watcher-state.json")
LOG_DIR = Path("/home/ubuntu/.openclaw/workspace/memory")
LOG_DIR.mkdir(parents=True, exist_ok=True)

# ===== GLOBALS =====
running = True
cycle_count = 0
last_alert = ""
alert_cooldown = set()  # Track topics already alerted today

# ===== SIGNAL HANDLERS =====
def shutdown(signum, frame):
    global running
    running = False
    log_event("SYSTEM", "Watcher shutting down gracefully")
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)

# ===== HELPERS =====
def now_ist():
    return datetime.now(timezone(timedelta(hours=5, minutes=30))).strftime("%Y-%m-%d %I:%M %p IST")

def log_event(category, message):
    timestamp = now_ist()
    log_file = LOG_DIR / f"watcher-{datetime.now(timezone.utc).strftime('%Y-%m-%d')}.log"
    entry = f"[{timestamp}] [{category}] {message}"
    with open(log_file, "a") as f:
        f.write(entry + "\n")
    print(entry, flush=True)

def get_state():
    if STATE_FILE.exists():
        with open(STATE_FILE) as f:
            return json.load(f)
    return {
        "last_gold_price": None,
        "last_silver_price": None,
        "last_market_trend": None,
        "last_content_trend": None,
        "alerts_today": 0,
        "cycles": 0,
        "errors": 0,
        "started": None,
    }

def save_state(state):
    state["cycles"] = cycle_count
    state["last_updated"] = now_ist()
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def send_telegram(text):
    """Send alert to Kaif on Telegram"""
    text = text.replace("&", "%26").replace("%", "%25")
    # Only URL-encode the text parameter, not the markdown
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = json.dumps({
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text[:3500],
        "parse_mode": "Markdown"
    }).encode('utf-8')
    try:
        r = req.Request(url, data=payload, headers={"Content-Type": "application/json"})
        resp = req.urlopen(r, timeout=10)
        return resp.status == 200
    except Exception as e:
        log_event("TELEGRAM", f"Failed to send: {e}")
        return False

def web_fetch(url, max_chars=5000):
    """Fetch URL content"""
    try:
        r = req.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        resp = req.urlopen(r, timeout=15)
        html = resp.read().decode("utf-8", errors="ignore")
        # Simple text extraction
        import re
        text = re.sub(r'<[^>]+>', ' ', html)
        text = re.sub(r'\s+', ' ', text).strip()
        return text[:max_chars]
    except Exception as e:
        return None

def mistral_analyze(system_prompt, user_prompt):
    """Call Mistral API with intelligence analysis"""
    global cycle_count
    time.sleep(RATE_LIMIT_SEC)

    payload = json.dumps({
        "model": MISTRAL_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "max_tokens": 800,
        "temperature": 0.3
    }).encode('utf-8')

    try:
        r = req.Request(MISTRAL_URL, data=payload, headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {MISTRAL_API_KEY}"
        })
        resp = req.urlopen(r, timeout=30)
        data = json.loads(resp.read().decode())
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        log_event("MISTRAL", f"API error: {e}")
        return None

def fetch_gold_price():
    """Get today's gold price in Ahmedabad"""
    try:
        text = web_fetch("https://www.goodreturns.in/gold-rates/ahmedabad.html")
        import re
        if text:
            match = re.search(r'₹[\d,]+\s*(?:per|per 1 gram|per 10 gram)', text.replace('\n', ' '))
            return match.group() if match else "Price fetch failed"
    except:
        pass
    return "Not available"

def fetch_trending_reels():
    """Get trending Reels search data"""
    try:
        text = web_fetch("https://www.google.com/trends/hottrends/atom/hourly")
        if text:
            import re
            trends = re.findall(r'<title>(.*?)</title>', text)
            return ", ".join(trends[:5]) if trends else "-"
    except:
        pass
    return "-"

# ===== TASK DEFINITIONS =====

def task_market_intelligence(state):
    """Check zari text market signals"""
    log_event("TASK", "Market Intelligence scan starting...")
    result = mistral_analyze(
        "You are an AI market analyst for a zari/handwork embroidery business in Ahmedabad, India. Be direct, no fluff. Give 3-4 bullet points max.",
        "What major signals are happening RIGHT NOW in: 1) Gold/Silver prices (affects real zari) 2) Indian textile export market 3) Wedding season demand 4) Festivals upcoming in next 2 weeks in India. Use your knowledge."
    )
    if result:
        alert_key = f"market_{datetime.now(timezone.utc).strftime('%Y-%m-%d_%H')}"
        if alert_key not in alert_cooldown:
            alert_cooldown.add(alert_key)
            state["last_market_trend"] = result[:200]
            msg = (
                f"📊 *Jarvis Market Update*\n"
                f"_Time: {now_ist()}_\n\n"
                f"{result}\n\n"
                f"— Jarvis · Autonomous Watcher 🦞"
            )
            send_telegram(msg)
            log_event("ALERT", "Market intelligence alert sent")
        else:
            log_event("TASK", "Market update — cooldown active, skipped alert")

def task_competitor_watch(state):
    """Analyze competitor moves"""
    log_event("TASK", "Competitor watch scan...")
    result = mistral_analyze(
        "You are a competitive intelligence analyst for textile businesses in India. Focus on actionable signals.",
        "List 4 specific competitive moves or pricing strategies from zari/handwork embroidery businesses in Ahmedabad/Surat/Mumbai that are trending online RIGHT NOW. Include any new Instagram trends in this niche."
    )
    if result:
        alert_key = f"comp_{datetime.now(timezone.utc).strftime('%Y-%m-%d_%H')}"
        if alert_key not in alert_cooldown:
            alert_cooldown.add(alert_key)
            msg = (
                f"🔍 *Jarvis Competitor Watch*\n"
                f"_Time: {now_ist()}_\n\n"
                f"{result}\n\n"
                f"— Jarvis · Autonomous Watcher 🦞"
            )
            send_telegram(msg)
            log_event("ALERT", "Competitor alert sent")

def task_content_ideas(state):
    """Generate fresh content ideas"""
    log_event("TASK", "Content ideation scan...")
    result = mistral_analyze(
        "You are a viral content strategist for Instagram Reels. Your client is a zari/handwork embroidery studio in Ahmedabad. Generate ONLY 1 idea — make it extremely actionable and specific.",
        f"Right now is {datetime.now(timezone.utc).strftime('%B %d, %Y')}. Generate 1 viral Instagram Reels idea for a zari embroidery business. Include: [Hook line] [Visual concept] [Audio suggestion] [Posting time]. Make it UNIQUE."
    )
    if result:
        alert_key = f"content_{datetime.now(timezone.utc).strftime('%Y-%m-%d')}"
        if alert_key not in alert_cooldown:
            alert_cooldown.add(alert_key)
            msg = (
                f"💡 *Jarvis Content Idea*\n"
                f"_Time: {now_ist()}_\n\n"
                f"{result}\n\n"
                f"— Jarvis · Autonomous Watcher 🦞"
            )
            send_telegram(msg)
            log_event("ALERT", "Content idea sent")

def task_business_insight(state):
    """Deep strategic insight for R Company"""
    log_event("TASK", "Strategic insight scan...")
    result = mistral_analyze(
        "You are a business strategist for R Company — a zari handwork studio in Ahmedabad. Owner: Kaif. Be brutally honest and specific.",
        "Kaif runs R Company (zari, handwork, dyework, silai, Ahmedabad). Identify 1 specific revenue opportunity or cost-saving strategy that he can implement THIS WEEK. Include exact numbers and steps."
    )
    if result:
        alert_key = f"biz_{datetime.now(timezone.utc).strftime('%Y-%m-%d')}"
        if alert_key not in alert_cooldown:
            alert_cooldown.add(alert_key)
            msg = (
                f"⚡ *Jarvis Business Intel*\n"
                f"_Time: {now_ist()}_\n\n"
                f"{result}\n\n"
                f"— Jarvis · Autonomous Watcher 🦞"
            )
            send_telegram(msg)
            log_event("ALERT", "Business insight sent")

# ===== MAIN LOOP =====

def main():
    global cycle_count, running

    state = get_state()
    if not state.get("started"):
        state["started"] = now_ist()
        save_state(state)

    log_event("SYSTEM", "🚀 Jarvis Autonomous Watcher v1.0 STARTED")
    send_telegram(
        f"🦞 *Jarvis Autonomous Watcher — ACTIVATED*\n\n"
        f"⏰ _Started: {now_ist()}_\n"
        f"🧠 Engine: Mistral Free API\n"
        f"📡 Rate: ~1 scan/minute, 1440/day capacity\n"
        f"🎯 Tasks: Market Intel, Competitor Watch, Content Ideas, Business Strategy\n\n"
        f"Kaif, ab main 24/7 jaag raha hoon. Kuch bhi milega — bhej dunga.\n\n"
        f"— Jarvis · Dabbatulardh ⚙️"
    )

    # Cycle tasks — each type runs at different intervals to be smart
    cycle_tasks = {
        "market": {"interval": 120, "last_run": 0, "fn": task_market_intelligence},
        "content": {"interval": 180, "fn": task_content_ideas, "last_run": 0},
        "competitor": {"interval": 240, "fn": task_competitor_watch, "last_run": 0},
        "strategy": {"interval": 360, "fn": task_business_insight, "last_run": 0},
    }

    cycle_start = time.time()
    while running:
        now = time.time()
        for task_name, task in cycle_tasks.items():
            if now - task["last_run"] >= task["interval"]:
                task["last_run"] = now
                try:
                    task["fn"](state)
                except Exception as e:
                    log_event("ERROR", f"Task {task_name} failed: {e}")
                    state["errors"] += 1

        cycle_count += 1
        save_state(state)

        # Sleep 30s then check again
        for _ in range(30):
            if not running:
                break
            time.sleep(1)

    # Cleanup on shutdown
    save_state(state)
    send_telegram(
        f"⚙️ *Jarvis Watcher — Stopped*\n"
        f"Cycles completed: {cycle_count}\n"
        f"_Restart available anytime_\n"
        f"— Jarvis"
    )

if __name__ == "__main__":
    main()
