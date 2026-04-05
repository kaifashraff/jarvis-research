#!/usr/bin/env python3
"""👁️ OBSERVER AGENT — Market price monitoring, gold/silver/zari tracking"""
import json, time, urllib.request, signal, sys, re
from datetime import datetime, timezone, timedelta
from pathlib import Path

MISTRAL_API_KEY = "R2pBYB7SkpaTgXCERyIoaSWFVrWYMzZa"
MISTRAL_URL = "https://api.mistral.ai/v1/chat/completions"
TELEGRAM_BOT_TOKEN = "8319377738:AAFBsPbuzhAdgCcokRl0tZFwwSErRSgiZMg"
TELEGRAM_CHAT_ID = "5998285479"
STATE_FILE = Path("/home/ubuntu/.openclaw/workspace/memory/observer-state.json")
running = True

def shutdown(s, f):
    global running; running = False; sys.exit(0)
signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)

def now_ist():
    return datetime.now(timezone(timedelta(hours=5, minutes=30))).strftime("%Y-%m-%d %I:%M %p IST")

def send_alert(text):
    payload = json.dumps({"chat_id": TELEGRAM_CHAT_ID, "text": text[:4000], "parse_mode": "Markdown"}).encode()
    try:
        urllib.request.urlopen(urllib.request.Request(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage", data=payload, headers={"Content-Type":"application/json"}), timeout=10)
    except: pass

def mistral(prompt, max_tokens=400):
    time.sleep(1.2)
    data = json.dumps({"model":"mistral-small-latest","messages":[{"role":"user","content":prompt}],"max_tokens":max_tokens,"temperature":0.3}).encode()
    try:
        r = urllib.request.urlopen(urllib.request.Request(MISTRAL_URL, data=data, headers={"Content-Type":"application/json","Authorization":f"Bearer {MISTRAL_API_KEY}"}), timeout=30)
        return json.loads(r.read())["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"[{now_ist()}] ❌ Observer API error: {e}", flush=True)
        return None

def fetch_prices():
    try:
        text = urllib.request.urlopen(urllib.request.Request("https://www.goodreturns.in/gold-rates/ahmedabad.html", headers={"User-Agent":"Mozilla/5.0"}), timeout=15).read().decode('utf-8', errors='ignore')
        clean = re.sub(r'<[^>]+>', ' ', text)
        clean = re.sub(r'\s+', ' ', clean).strip()[:4000]
        prices = re.findall(r'₹[\d,]+', clean)
        return f"Ahmedabad rates: {', '.join(set(prices[:6]))}" if prices else None
    except Exception as e:
        print(f"[{now_ist()}] ❌ Price fetch failed: {e}", flush=True)
        return None

def market_intel():
    return mistral(
        "R Company (Ahmedabad) does zari/handwork embroidery. What are TODAY's signals: "
        "1) Gold price movement (up/down vs yesterday) 2) Textile market activity in Surat/Ahmedabad "
        "3) Wedding season demand trend 4) Any festival in next 2 weeks in India. "
        "4 bullet points. Actionable only. No fluff."
    )

def main():
    global running
    state = json.loads(STATE_FILE.read_text()) if STATE_FILE.exists() else {"cycle":0,"last_report":""}
    print(f"[{now_ist()}] 👁️ Observer Agent ONLINE — Market & price monitoring", flush=True)
    send_alert(f"👁️ *Observer Agent ONLINE*\n_{now_ist()}_\nMonitoring: Gold prices, Silver rates, Zari market signals\n— Jarvis Agent Factory 🦞")
    
    while running:
        state["cycle"] += 1
        
        prices = fetch_prices()
        if prices:
            print(f"  📊 {prices}", flush=True)
        
        intel = market_intel()
        if intel:
            alert_key = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H")
            if state.get("last_report") != alert_key:
                state["last_report"] = alert_key
                price_line = f"💰 {prices}" if prices else "💰 Price data unavailable"
                msg = f"📊 *Jarvis Observer — Market Scan*\n_{now_ist()}_\n\n{price_line}\n\n{intel}\n\n— Observer Agent 🦞"
                print(f"  📤 Alert sent to Telegram", flush=True)
                send_alert(msg)
        
        STATE_FILE.write_text(json.dumps(state, indent=2))
        print(f"  ⏳ Next scan in 5 min (cycle {state['cycle']})", flush=True)
        for _ in range(300):
            if not running: break
            time.sleep(1)

if __name__ == "__main__":
    main()
