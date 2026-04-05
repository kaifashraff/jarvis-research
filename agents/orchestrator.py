#!/usr/bin/env python3
"""
JARVIS ORCHESTRATOR — 5 Sub-Agents, 24/7 Autonomous Operation
Powered by Mistral Free API (1 req/s, 1B tokens/month)
Launches: Observer, Researcher, Strategist, ContentCreator, Guardian
"""

import subprocess
import time
import signal
import sys
import os
from pathlib import Path

AGENTS = [
    {"name": "observer",        "role": "👁️ Observer",       "file": "observer-agent.py"},
    {"name": "researcher",      "role": "🔍 Researcher",      "file": "researcher-agent.py"},
    {"name": "strategist",      "role": "🧠 Strategist",      "file": "strategist-agent.py"},
    {"name": "content-creator", "role": "🎬 Content Creator", "file": "content-creator-agent.py"},
    {"name": "guardian",        "role": "🛡️ Guardian",        "file": "guardian-agent.py"},
]

BASE = Path("/home/ubuntu/.openclaw/workspace/agents")
LOG_DIR = Path("/home/ubuntu/.openclaw/workspace/memory")
LOG_DIR.mkdir(parents=True, exist_ok=True)

processes = {}
running = True

def shutdown(signum, frame):
    global running
    running = False
    for name, p in processes.items():
        if p and p.poll() is None:
            p.terminate()
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)

def launch_agent(agent):
    log_file = LOG_DIR / f"{agent['name']}-{time.strftime('%Y-%m-%d')}.log"
    cmd = [sys.executable, str(BASE / agent["file"])]
    with open(log_file, "a") as f:
        p = subprocess.Popen(cmd, stdout=f, stderr=subprocess.STDOUT)
    processes[agent["name"]] = p
    return p

def main():
    global running
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 🦞 Jarvis Orchestrator — Launching {len(AGENTS)} agents...", flush=True)
    
    for agent in AGENTS:
        p = launch_agent(agent)
        print(f"  ✅ {agent['role']} ({agent['name']}) — PID {p.pid}", flush=True)
    
    print(f"\n  All agents live. 24/7 autonomous operation initiated.\n", flush=True)
    
    while running:
        time.sleep(30)
        for name, p in list(processes.items()):
            if p.poll() is not None:
                print(f"[{time.strftime('%H:%M:%S')}] ⚠️ {name} exited (code {p.returncode}). Restarting...", flush=True)
                agent = next(a for a in AGENTS if a["name"] == name)
                p = launch_agent(agent)
                processes[name] = p
                print(f"  ✅ {agent['role']} restarted — PID {p.pid}", flush=True)

if __name__ == "__main__":
    main()
