MEMORY_AGI.md v2.1 — Jarvis Persistent Intelligence
THREE MEMORY TYPES
Episodic — what happened (daily logs)
Semantic — what is true (facts + knowledge graph)
Procedural — how to do things (skills + scripts)
EPISODIC MEMORY (77KB raw)
Every session logged: timestamp, input, action, output, files, decisions, lessons, confidence.
Key files:
zari-b2b-research-report.md (5.8KB)
zari-buyer-database.md (6.6KB)
zari-offer-catalog.md (9.5KB)
pricing-strategy-kaif.md (4.6KB)
6-hour-challenge-plan.md (5.5KB)
SEMANTIC MEMORY — KNOWLEDGE GRAPH
Kaif: Owner R Company | Ahmedabad | Hinglish | Truth > comfort | Friend mode
R Company: Zari/handwork/dyework/silai | Ahmedabad | Target ₹500+/day profit | B2B boutiques/bridal
Jarvis: OpenClaw on EC2 | qwen/qwen3-plus:free | 82 skills | 286KB research | Friend > Servant
Providers: OpenRouter (primary), Mistral, Groq, Cerebras, SiliconFlow, SambaNova
VERIFIED FACTS
Fact
Confidence
"Al-Quran" count = 57
95%
"Allah" count = 2,828
95%
Code 19 claims 80% invalid
90%
Alibaba zari ₹1,100-1,700/piece
80%
Etsy zari ₹2,500-17,000/piece
80%
Volza 533+ zari importers
85%
KNOWLEDGE DECAY
Knowledge
Risk
Action
Market prices
HIGH
Auto-refresh every 2 hours
Festival calendar
LOW
Weekly check
Business context
MEDIUM
Kaif to update
Agent identities
NONE
Monthly review
PROCEDURAL MEMORY
Top skills: instagram-agent, pricing-calc, clawflow, skill-creator, mcporter, healthcheck
Cron scripts:
autonomous-thinking-engine.sh → every 10 min
gateway-watchdog.sh → every 1 min
self-improvement.sh → every 6 hours
memory-distillation.sh → daily
DISTILLATION PIPELINE
Raw session log
→ Pattern extraction
→ Noise filtering (greetings, duplicates)
→ Knowledge extraction (facts/decisions/lessons)
→ MEMORY.md update
→ Archive raw (delete after 30 days)
→ Knowledge graph update
CURRENT MEMORY STATE
Category
Size
Daily logs
14.5KB
MEMORY.md
4.8KB
Research archives
~90KB
Agent research
286KB
Total
~395KB
KEY LESSONS
About Kaif: Direct action > discussion | Friend mode | No summary-only | Proactive | Hinglish | ₹500/day target
About system: Free models work | Telegram = inbox | GitHub = archive | Cron + systemd = stable
EVOLUTION PHASES
Phase 1 → File-based memory ✅ (now, 400KB)
Phase 2 → LanceDB + Knowledge Graph 🟡 (week 1-2)
Phase 3 → Auto-distillation + decay detection 🟠 (month 2-3)
Phase 4 → Predictive memory 🔴 (month 4-6)
STATUS
🟡 Phase 1 complete | 395KB / 26 files | 85% accuracy | Phase 2 ready
