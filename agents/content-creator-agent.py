#!/usr/bin/env python3
"""🎬 CONTENT CREATOR AGENT — Daily content generation, viral hooks, caption writing"""
import json, time, urllib.request, urllib.parse, os, signal, re
from datetime import datetime, timezone, timedelta
from pathlib import Path

MISTRAL_API_KEY = "R2pBYB7SkpaTgXCERyIoaSWFVrWYMzZa"
MISTRAL_URL = "https://api.mistral.ai/v1/chat/completions"
TELEGRAM_BOT_TOKEN = "8319377738:AAFBsPbuzhAdgCcokRl0tZFwwSErRSgiZMg"
TELEGRAM_CHAT_ID = "5998285479"
STATE_FILE = Path("/home/ubuntu/.openclaw/workspace/memory/content-creator-state.json")
running = True

def shutdown(s, f):
    global running; running = False; sys.exit(0)
signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)

def ist_now():
    return datetime.now(timezone(timedelta(hours=5, minutes=30)))

def now_ist():
    return ist_now().strftime("%Y-%m-%d %I:%M %p IST")

def send_alert(text):
    payload = json.dumps({"chat_id": TELEGRAM_CHAT_ID, "text": text[:3500], "parse_mode": "Markdown"}).encode()
    try:
        urllib.request.urlopen(urllib.request.Request(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage", data=payload, headers={"Content-Type": "application/json"}), timeout=10)
    except: pass

def mistral(prompt, max_tokens=600):
    time.sleep(1.2)
    data = json.dumps({"model":"mistral-small-latest","messages":[{"role":"user","content":prompt}],"max_tokens":max_tokens,"temperature":0.5}).encode()
    try:
        r = urllib.request.urlopen(urllib.request.Request(MISTRAL_URL, data=data, headers={"Content-Type":"application/json","Authorization":f"Bearer {MISTRAL_API_KEY}"}), timeout=30)
        return json.loads(r.read())["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"  ❌ Mistral error: {e}", flush=True)
        return None

def generate_content():
    today = ist_now()
    return mistral(
        f"You are a content creator for R Company — zari handwork studio in Ahmedabad. "
        f"Generate 1 ready-to-post Instagram content idea with: "
        f"Hook line (scroll-stopping), Caption (Hinglish, 120 chars no hashtags), "
        f"Visual concept, Audio suggestion, Best post time, 15 hashtags. "
        f"Today: {today.strftime('%A, %B %d, %Y')}.",
        600
    )

def generate_whatsapp_broadcast():
    return mistral(
        "WhatsApp broadcast for R Company zari studio. Hinglish, short, persuasive, under 150 words. "
        "Include urgency, emoji, CTA. Audience: existing customers +boutique owners.",
        400
    )

def generate_buyer_outreach():
    return mistral(
        "Cold outreach message for potential buyers/boutiques in Ahmedabad/Surat/Mumbai. "
        "R Company: zari+handwork embroidery. Hinglish, professional, under 200 words. "
        "Focus: custom work, handcrafted>machine, 7-day turnaround, competitive pricing. Clear CTA.",
        400
    )

def main():
    global running
    state = json.loads(STATE_FILE.read_text()) if STATE_FILE.exists() else {"cycle":0}
    print(f"\n[{now_ist()}] 🎬 Content Creator Agent STARTED — Content generation engine", flush=True)
    send_alert(f"🎬 *Content Creator Agent ONLINE*\n_Time: {now_ist()}_\nGenerating: Instagram posts, WhatsApp broadcasts, Buyer outreach\n— Jarvis Agent Factory 🦞")
    
    while running:
        state["cycle"] += 1
        t = ist_now()
        hour = t.hour
        minute = t.minute
        date_str = t.strftime("%Y-%m-%d")
        
        if 9 <= hour <= 22 and minute < 15 and state.get("last_content_hour") != hour:
            print(f"  🎬 Generating content...", flush=True)
            content = generate_content()
            if content:
                state["last_content_hour"] = hour
                msg = f"🎬 *Jarvis Content Creator — Fresh Content*\n_Time: {now_ist()}_\n\n{content}\n\n— Content Creator Agent 🦞"
                print(f"  📤 Sending to Telegram...", flush=True)
                send_alert(msg)
        
        if hour % 8 == 10 and minute < 15 and state.get("last_broadcast_date") != date_str:
            print(f"  📱 Generating broadcast...", flush=True)
            broadcast = generate_whatsapp_broadcast()
            if broadcast:
                state["last_broadcast_date"] = date_str
                msg = f"📱 *Jarvis Content Creator — WhatsApp Broadcast*\n_Time: {now_ist()}_\n\n{broadcast}\n\n— Content Creator Agent 🦞"
                print(f"  📤 Sending to Telegram...", flush=True)
                send_alert(msg)
        
        if hour == 9 and minute < 15 and state.get("last_outreach_date") != date_str:
            print(f"  📧 Generating buyer outreach...", flush=True)
            outreach = generate_buyer_outreach()
            if outreach:
                state["last_outreach_date"] = date_str
                msg = f"📧 *Jarvis Content Creator — Buyer Outreach*\n_Time: {now_ist()}_\n\n{outreach}\n\n— Content Creator Agent 🦞"
                print(f"  📤 Sending to Telegram...", flush=True)
                send_alert(msg)
        
        STATE_FILE.write_text(json.dumps(state, indent=2))
        for _ in range(600):
            if not running: break
            time.sleep(1)

if __name__ == "__main__":
    main()
