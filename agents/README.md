# 🦞 JARVIS AGENT FACTORY — Autonomous 24/7 Sub-Agents

> 5 agents powered by Mistral Free API (1B tokens/month, 1 req/s)
> Each agent runs independently, monitors, analyzes, and alerts Kaif on Telegram

---

## 🧠 Agent Architecture

```
┌─────────────────────────────────────────────────┐
│            JARVIS ORCHESTRATOR                    │
│         (Launches & Monitors)                     │
├────────┬────────┬────────┬───────────┬───────────┤
│  👁️    │  🔍    │  🧠   │  🎬       │  🛡️       │
│Observer│Research│Strategy│Content    │Guardian   │
│        │        │        │           │           │
│Markets │Trends  │Revenue │Content    │Health    │
│Prices  │Comps   │Pricing │Outreach   │Security  │
│Signals │Seasons │Ops     │Broadcasts │Alerts    │
└────────┴────────┴────────┴───────────┴───────────┘
```

---

## 📡 How It Works

### Mistral Free API Usage
- **Rate Limit:** 1 request/second
- **Monthly Tokens:** 1,000,000,000 (1 billion)
- **Daily Capacity:** ~86,400 requests
- **Cost:** ₹0

### Smart Scheduling (No API Waste)
| Agent | Scan Interval | Mistral Calls/Day | Purpose |
|-------|--------------|-------------------|---------|
| Observer | Every 5 min | ~30 | Gold/silver prices, market signals |
| Researcher | Every 10 min | ~6 | Competitor intel, trend research |
| Strategist | Every 15 min | ~4 | Revenue ideas, pricing, alerts |
| ContentCreator | Every 8 min | ~8 | Posts, captions, WhatsApp drafts |
| Guardian | Every 5 min | ~2 | System health, quality control |

**Total:** ~50 Mistral calls/day = ~1500/month = **0.15% of free limit used**

### Telegram Alerting
All agents alert Kaif directly on Telegram when they find something actionable:
- Price changes >5%
- New competitor moves
- Revenue opportunities
- Content ideas
- System issues

---

## 🚀 Setup & Deployment

### 1. Push to GitHub
```bash
cd /home/ubuntu/.openclaw/workspace
git add agents/
git commit -m "Add 5 autonomous sub-agents with Mistral API"
git push origin main
```

### 2. Install Systemd Services
```bash
# Each agent gets its own service for auto-restart
sudo systemctl daemon-reload
sudo systemctl enable jarvis-observer jarvis-researcher jarvis-strategist jarvis-content-creator jarvis-guardian
sudo systemctl start jarvis-observer jarvis-researcher jarvis-strategist jarvis-content-creator jarvis-guardian
```

### 3. Monitor
```bash
# Check all agent status
systemctl status jarvis-*

# View live logs
journalctl -f -u jarvis-observer
```

---

## 📊 Agent Details

### 👁️ Observer Agent
**File:** `observer-agent.py`
**Role:** Market intelligence & price monitoring
**Checks:**
- Gold/silver prices in Ahmedabad (every 5 min)
- Zari market trends
- Textile industry signals
- Festival calendar alerts
**Output:** Telegram alerts when prices move >5% or market shifts detected

### 🔍 Researcher Agent  
**File:** `researcher-agent.py`
**Role:** Deep research & competitor analysis
**Checks:**
- Competitor moves in Ahmedabad zari market
- Seasonal demand patterns
- Industry trend reports
- New opportunities
**Output:** Research summaries + competitive intelligence reports

### 🧠 Strategist Agent
**File:** `strategist-agent.py`  
**Role:** Business strategy & decision support
**Checks:**
- Revenue opportunity identification
- Pricing optimization
- Operational improvements
- Risk alerts
**Output:** Strategic recommendations + priority action items

### 🎬 ContentCreator Agent
**File:** `content-creator-agent.py`
**Role:** Content generation & marketing
**Generates:**
- Instagram post ideas (daily)
- WhatsApp broadcast messages
- Buyer outreach templates
- Trending hook suggestions
**Output:** Ready-to-use content delivered to Telegram

### 🛡️ Guardian Agent
**File:** `guardian-agent.py`
**Role:** System health & quality control
**Monitors:**
- All other agents running status
- API usage & rate limits
- Memory/logs health
- Security scans
**Output:** Daily system reports + emergency alerts

---

## 📁 File Structure

```
agents/
├── orchestrator.py           # Main launcher for all agents
├── observer-agent.py         # Market monitoring
├── researcher-agent.py       # Intel & research
├── strategist-agent.py       # Business strategy
├── content-creator-agent.py  # Content generation
├── guardian-agent.py         # System health
└── README.md                 # This file

memory/
├── observer-state.json       # Agent state persistence
├── researcher-state.json
├── strategist-state.json
├── content-creator-state.json
└── guardian-state.json

memory/
└── watcher-*.log             # Daily agent logs
```

---

## ⚡ Key Features

- **Auto-restart:** If any agent crashes, it restarts automatically
- **State persistence:** Each agent saves its state so it doesn't repeat work
- **Rate limit handling:** Respects 1 req/s Mistral API limit
- **Smart scheduling:** Different intervals per agent to spread API load
- **Quality control:** Guardian agent monitors output quality of others
- **Cost optimization:** Uses <1% of daily free token limit
- **Telegram integration:** All alerts go directly to Kaif's phone

---

## 🎯 Next Steps

1. ✅ All agents coded and ready
2. 🚀 Deploy as systemd services for 24/7 operation
3. 📊 Add dashboard for real-time monitoring
4. 🤝 Add inter-agent communication (agents can trigger each other)
5. 📈 Add performance metrics & usage tracking

---

*Built by Kaif Ashraf · Jarvis Autonomous Intelligence System · April 2026*