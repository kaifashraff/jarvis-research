#!/usr/bin/env python3
"""🛡️ GUARDIAN AGENT — System health, error alerting, quality control for other agents"""
import json, time, urllib.request, os, signal, sys, subprocess
from datetime import datetime, timezone, timedelta
from pathlib import Path

MISTRAL_API_KEY = "R2pBYB7SkpaTgXCERyIoaSWFVrWYMzZa"
MISTRAL_URL = "https://api.mistral.ai/v1/chat/completions"
TELEGRAM_BOT_TOKEN = "8319377738:AAFBsPbuzhAdgCcokRl0tZFwwSErRSgiZMg"
TELEGRAM_CHAT_ID = "5998285479"
STATE_FILE = Path("/home/ubuntu/.openclaw/workspace/memory/guardian-state.json")
MEMORY_DIR = Path("/home/ubuntu/.openclaw/workspace/memory")
AGENTS_DIR = Path("/home/ubuntu/.openclaw/workspace/agents")
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
        urllib.request.urlopen(urllib.request.Request(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage", data=payload, headers={"Content-Type": "application/json"}), timeout=10)
    except Exception as e:
        print(f"  ❌ Telegram send failed: {e}", flush=True)

def mistral(prompt, max_tokens=500):
    time.sleep(1.2)
    data = json.dumps({"model":"mistral-small-latest","messages":[{"role":"user","content":prompt}],"max_tokens":max_tokens,"temperature":0.3}).encode()
    try:
        r = urllib.request.urlopen(urllib.request.Request(MISTRAL_URL, data=data, headers={"Content-Type":"application/json","Authorization":f"Bearer {MISTRAL_API_KEY}"}), timeout=30)
        return json.loads(r.read())["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"  ❌ Mistral error: {e}", flush=True)
        return None

def check_agent_health():
    """Check if all agent processes are running"""
    agent_processes = {"observer":"", "researcher":"", "strategist":"", "content-creator":"", "guardian":""}
    try:
        result = subprocess.run(["ps", "aux"], capture_output=True, text=True)
        for agent_name in agent_processes:
            if agent_name in result.stdout and "grep" not in result.stdout:
                agent_processes[agent_name] = "✅ Running"
            else:
                agent_processes[agent_name] = "❌ Not detected"
    except Exception as e:
        return f"Health check error: {e}"
    
    return "\n".join([f"{agent}: {status}" for agent, status in agent_processes.items()])

def check_system_resources():
    """Check disk space, memory, etc."""
    health_report = []
    try:
        # Disk space
        result = subprocess.run(["df", "-h", "/"], capture_output=True, text=True)
        disk_info = result.stdout.strip().split("\n")[-1]
        health_report.append(f"📀 Disk: {disk_info}")
        
        # Memory usage
        result_free = subprocess.run(["free", "-m"], capture_output=True, text=True)
        mem_info = result_free.stdout.strip().split("\n")[1]
        health_report.append(f"🧠 Memory: {mem_info}")
        
        # Load average
        result = subprocess.run(["uptime"], capture_output=True, text=True)
        health_report.append(f"⏱️ Uptime: {result.stdout.strip()}")
    except Exception as e:
        health_report.append(f"System check error: {e}")
    
    return "\n".join(health_report)

def generate_daily_report():
    """Generate comprehensive daily summary of all agent activities"""
    agent_summaries = []
    for agent_file in ["observer-state.json", "researcher-state.json", "strategist-state.json", "content-creator-state.json"]:
        state_file = MEMORY_DIR / agent_file
        if state_file.exists():
            try:
                state = json.loads(state_file.read_text())
                agent_name = agent_file.replace("-state.json", "")
                cycles = state.get("cycle", "N/A")
                agent_summaries.append(f"• {agent_name}: {cycles} cycles completed")
            except:
                pass
    
    return "\n".join(agent_summaries) if agent_summaries else "No agent states found"

def validate_content_quality():
    """Review recent agent outputs for quality"""
    recent_logs = []
    for log_file in sorted(MEMORY_DIR.glob("watcher-*.log"), reverse=True)[:1]:
        try:
            lines = log_file.read_text().split("\n")[-20:]
            recent_logs.extend(lines)
        except:
            pass
    
    if recent_logs:
        log_text = "\n".join(recent_logs[-10:])
        quality_review = mistral(
            f"You are a quality control analyst for an AI agent system managing a zari embroidery business. "
            f"Review these recent agent outputs and identify: 1) Any incorrect information 2) Poor quality alerts 3) Suggested improvements "
            f"Logs:\n{log_text}",
            400
        )
        return quality_review
    return "No recent logs to review"

def main():
    global running
    state = json.loads(STATE_FILE.read_text()) if STATE_FILE.exists() else {"cycle":0,"last_report":""}
    print(f"\n[{now_ist()}] 🛡️ Guardian Agent STARTED — System health & quality control", flush=True)
    send_alert(f"🛡️ *Guardian Agent ONLINE*\n_Time: {now_ist()}_\nMonitoring: Agent health, System resources, Quality control, Security\n— Jarvis Agent Factory 🦞")
    
    while running:
        state["cycle"] += 1
        t = datetime.now(timezone(timedelta(hours=5, minutes=30)))
        hour = t.hour
        minute = t.minute
        date_str = t.strftime("%Y-%m-%d")
        
        # System health check every 1 hour
        if minute == 0 and state.get("last_health_check_hour") != hour:
            print(f"  🛡️ Running system health check...", flush=True)
            health = check_agent_health()
            system = check_system_resources()
            
            health_report = f"🛡️ *System Health Check*\n_Time: {now_ist()}_\n\n{health}\n\n{system}\n\n— Guardian Agent 🦞"
            print(f"  📤 Sending health report...", flush=True)
            send_alert(health_report)
            state["last_health_check_hour"] = hour
        
        # Daily report at 9 AM IST
        if hour == 9 and minute < 5 and state.get("last_daily_report_date") != date_str:
            print(f"  📊 Generating daily report...", flush=True)
            agent_summary = generate_daily_report()
            quality = validate_content_quality()
            
            daily_report = f"📊 *Jarvis Daily Summary — {date_str}*\n\n🔄 *Agent Activity:*\n{agent_summary}\n\n📋 *Quality Assessment:*\n{quality}\n\n— Guardian Agent 🦞"
            print(f"  📤 Sending daily report...", flush=True)
            send_alert(daily_report)
            state["last_daily_report_date"] = date_str
        
        # Security check every 4 hours
        if hour % 4 == 0 and minute < 5:
            print(f"  🔒 Running security scan...", flush=True)
            # Check for sensitive files, API key exposure, etc.
            security_issues = []
            
            # Check if any sensitive files are exposed
            sensitive_paths = [".env", "secrets", "password", "key", "token"]
            for agent_file in AGENTS_DIR.glob("*.py"):
                content = agent_file.read_text()
                if any(secret in content for secret in sensitive_paths):
                    security_issues.append(f"⚠️ Sensitive data in {agent_file.name}")
            
            if security_issues:
                alert = f"🚨 *Security Alert*\n_Time: {now_ist()}_\n\n" + "\n".join(security_issues)
                send_alert(alert)
            
            security_check = f"✅ Security scan completed. Issues: {len(security_issues)}"
            print(f"  {security_check}", flush=True)
        
        STATE_FILE.write_text(json.dumps(state, indent=2))
        for _ in range(300):  # Check every 5 minutes
            if not running: break
            time.sleep(1)

if __name__ == "__main__":
    main()
