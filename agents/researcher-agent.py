#!/usr/bin/env python3
"""🔍 RESEARCHER AGENT — Trend research, competitor intel, seasonal opportunities"""
import json, time, urllib.request, urllib.parse, os, signal, re
from datetime import datetime, timezone, timedelta
from pathlib import Path

MISTRAL_API_KEY = "R2pBYB7SkpaTgXCERyIoaSWFVrWYMzZa"
MISTRAL_URL = "https://api.mistral.ai/v1/chat/completions"
TELEGRAM_BOT_TOKEN = "8319377738:AAFBsPbuzhAdgCcokRl0tZFwwSErRSgiZMg"
TELEGRAM_CHAT_ID = "5998285479"
STATE_FILE = Path("/home/ubuntu/.openclaw/workspace/memory/researcher-state.json")
running = True

def shutdown(s, f):
    global running; running = False; sys.exit(0)
signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)

def now_ist():
    return datetime.now(timezone(timedelta(hours=5.5))).strftime("%Y-%m-%d %I:%M %p IST")

def send_alert(text):
    payload = json.dumps({"chat_id": TELEGRAM_CHAT_ID, "text": text[:4000], "parse_mode": "Markdown"}).encode()
    try:
        urllib.request.urlopen(urllib.request.Request(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage", data=payload, headers={"Content-Type": "application/json"}), timeout=10)
    except: pass

def mistral(prompt, max_tokens=600):
    time.sleep(1.2)
    data = json.dumps({"model":"mistral-small-latest","messages":[{"role":"user","content":prompt}],"max_tokens":max_tokens,"temperature":0.4}).encode()
    try:
        r = urllib.request.urlopen(urllib.request.Request(MISTRAL_URL, data=data, headers={"Content-Type":"application/json","Authorization":f"Bearer {MISTRAL_API_KEY}"}), timeout=30)
        return json.loads(r.read())["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"  ❌ Mistral error: {e}", flush=True)
        return None

def research_competitors():
    return mistral(
        "You are researching competitors for R Company (Ahmedabad zari/handwork embroidery studio). "
        "Research and report: 1) 2-3 Ahmedabad-based zari competitors and their current activities "
        "2) Any new pricing strategies in the zari market 3) What are other zari businesses doing on Instagram/WhatsApp? "
        "4) Any new technology or process being adopted? 5 bullet points, specific and actionable.",
        "500"
    )

def research_seasonal_demand():
    today = datetime.now(timezone.utc)
    months_ahead = (today.month + 2) % 12
    month_names = {1:"January",2:"February",3:"March",4:"April",5:"May",6:"June",7:"July",8:"August",9:"September",10:"October",11:"November",12:"December"}
    return mistral(
        f"You are analyzing seasonal demand for zari/handwork embroidery in India. "
        f"What are the biggest opportunities in the next 2-3 months? "
        f"Include: weddings, festivals, seasonal changes in demand in Gujarat/Ahmedabad. "
        f"Give 3 specific opportunities with approximate revenue potential.",
        "400"
    )

def main():
    global running
    state = json.loads(STATE_FILE.read_text()) if STATE_FILE.exists() else {"cycle":0,"last_report":""}
    print(f"\n[{now_ist()}] 🔍 Researcher Agent STARTED — Competitor & trend intelligence", flush=True)
    send_alert(f"🔍 *Researcher Agent ONLINE*\n_Time: {now_ist()}_\nResearching: Competitor moves, Seasonal demand, Industry trends\n— Jarvis Agent Factory 🦞")
    
    while running:
        state["cycle"] += 1
        hour = datetime.now(timezone(timedelta(hours=5.5))).hour
        
        if hour % 4 == 0:  # Every 4 hours
            print(f"  🔍 Running competitor research...", flush=True)
            intel = research_competitors()
            if intel:
                state["last_report"] = "comp"
                msg = f"🔍 *Jarvis Researcher — Competitor Intel*\n_Time: {now_ist()}_\n\n{intel}\n\n— Researcher Agent 🦞"
                print(f"  📤 Sending intelligence report to Telegram...", flush=True)
                send_alert(msg)
        
        if hour % 5 == 0:  # Every 5 hours
            print(f"  🔍 Running seasonal demand analysis...", flush=True)
            seasonal = research_seasonal_demand()
            if seasonal:
                state["last_report"] = "seasonal"
                msg = f"📈 *Jarvis Researcher — Seasonal Demand*\n_Time: {now_ist()}_\n\n{seasonal}\n\n— Researcher Agent 🦞"
                print(f"  📤 Sending seasonal analysis to Telegram...", flush=True)
                send_alert(msg)
        
        STATE_FILE.write_text(json.dumps(state, indent=2))
        wait_time = 600
        print(f"  ⏳ Next research cycle in {wait_time//60} min... (cycle {state['cycle']})\n", flush=True)
        for _ in range(wait_time):
            if not running: break
            time.sleep(1)

if __name__ == "__main__":
    main()
