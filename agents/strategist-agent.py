#!/usr/bin/env python3
"""🧠 STRATEGIST AGENT — Business strategy, pricing decisions, opportunity alerts"""
import json, time, urllib.request, urllib.parse, os, signal, re
from datetime import datetime, timezone, timedelta
from pathlib import Path

MISTRAL_API_KEY = "R2pBYB7SkpaTgXCERyIoaSWFVrWYMzZa"
MISTRAL_URL = "https://api.mistral.ai/v1/chat/completions"
TELEGRAM_BOT_TOKEN = "8319377738:AAFBsPbuzhAdgCcokRl0tZFwwSErRSgiZMg"
TELEGRAM_CHAT_ID = "5998285479"
STATE_FILE = Path("/home/ubuntu/.openclaw/workspace/memory/strategist-state.json")
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
    data = json.dumps({"model":"mistral-small-latest","messages":[{"role":"user","content":prompt}],"max_tokens":max_tokens,"temperature":0.3}).encode()
    try:
        r = urllib.request.urlopen(urllib.request.Request(MISTRAL_URL, data=data, headers={"Content-Type":"application/json","Authorization":f"Bearer {MISTRAL_API_KEY}"}), timeout=30)
        return json.loads(r.read())["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"  ❌ Mistral error: {e}", flush=True)
        return None

def business_strategy():
    return mistral(
        "Kaif runs R Company — a zari handwork embroidery studio in Ahmedabad. "
        "Be brutally honest, specific, and actionable. No fluff. "
        f"Current date is {datetime.now(timezone.utc).strftime('%B %d, %Y')}. "
        "What should Kaif focus on: 1) Revenue opportunity this week 2) Cost reduction idea 3) Buyer outreach strategy 4) Pricing adjustment recommendation. "
        "Include specific numbers where possible. 6-8 bullet points max.",
        "600"
    )

def pricing_analysis():
    return mistral(
        """You are a pricing strategist for a zari/handwork embroidery business. 
        R Company (Ahmedabad) does zari, handwork, dyework, silai. 
        What competitive pricing strategies should Kaif implement right now?
        Consider: B2B vs B2C pricing, bulk discounts, seasonal adjustments, premium tier options. 
        Give 4 actionable pricing recommendations with specific numbers.""",
        "500"
    )

def main():
    global running
    state = json.loads(STATE_FILE.read_text()) if STATE_FILE.exists() else {"cycle":0,"last_alert":""}
    print(f"\n[{now_ist()}] 🧠 Strategist Agent STARTED — Business strategy engine", flush=True)
    send_alert(f"🧠 *Strategist Agent ONLINE*\n_Time: {now_ist()}_\nOptimizing: Revenue, Pricing, Cost reduction, Buyer strategy\n— Jarvis Agent Factory 🦞")
    
    while running:
        state["cycle"] += 1
        hour = datetime.now(timezone(timedelta(hours=5.5))).hour
        
        # Run strategy analysis every 3 hours
        if hour % 3 == 0 and datetime.now(timezone(timedelta(hours=5.5))).minute < 15:
            print(f"  🧠 Running business strategy analysis...", flush=True)
            strategy = business_strategy()
            if strategy:
                state["last_strategy"] = datetime.now(timezone.utc).isoformat()
                msg = f"🧠 *Jarvis Strategist — Business Intelligence*\n_Time: {now_ist()}_\n\n{strategy}\n\n— Strategist Agent 🦞"
                print(f"  📤 Sending strategy to Telegram...", flush=True)
                send_alert(msg)
        
        # Run pricing analysis every 6 hours
        if hour % 6 == 3 and datetime.now(timezone(timedelta(hours=5.5))).minute < 15:
            print(f"  📊 Running pricing analysis...", flush=True)
            pricing = pricing_analysis()
            if pricing:
                state["last_pricing"] = datetime.now(timezone.utc).isoformat()
                msg = f"💰 *Jarvis Strategist — Pricing Strategy*\n_Time: {now_ist()}_\n\n{pricing}\n\n— Strategist Agent 🦞"
                print(f"  📤 Sending pricing analysis to Telegram...", flush=True)
                send_alert(msg)
        
        STATE_FILE.write_text(json.dumps(state, indent=2))
        wait_time = 900
        print(f"  ⏳ Next strategy cycle in {wait_time//60} min... (cycle {state['cycle']})\n", flush=True)
        for _ in range(wait_time):
            if not running: break
            time.sleep(1)

if __name__ == "__main__":
    main()
