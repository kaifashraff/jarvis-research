RECURSIVE_LEARNING.md — Daily Self-Learning Skill
For: Jarvis | OpenClaw | R Company
WHAT THIS DOES
Every day, Jarvis:
Reads what happened today
Extracts what actually matters
Compresses into permanent memory
Deletes noise
Gets smarter — without growing token load
This is recursive learning. Every cycle builds on the last.
SKILL PROMPT (Paste into OpenClaw skill or cron task)
You are Jarvis's daily learning engine.

Your job: Read today's raw logs, extract intelligence, update permanent memory.

## STEP 1: READ TODAY
Read file: memory/{{TODAY}}.md
If file missing → log "No activity today" and stop.

## STEP 2: EXTRACT ONLY WHAT MATTERS
From today's log, extract:

DECISIONS: What was decided? Why?
MISTAKES: What went wrong? Root cause?
WINS: What worked? Why?
LESSONS: What would I do differently?
KAIF_PATTERNS: New behavior, preference, or feedback from Kaif?
BUSINESS_INTEL: Any R Company data — prices, buyers, orders?
OPEN_TASKS: What is unfinished?

Ignore: greetings, confirmations, repeated info, small talk.

## STEP 3: SCORE EVERYTHING
Every extracted fact gets:
- Confidence: 0-100%
- Decay risk: HIGH (prices) / MEDIUM (strategies) / LOW (identity)
- Category: DECISION / MISTAKE / WIN / LESSON / INTEL / TASK

## STEP 4: UPDATE PERMANENT MEMORY
Read current: memory/MEMORY.md
For each extracted item:
- If new → append under correct category
- If updates existing fact → replace old entry
- If contradicts existing fact → flag with ⚠️ CONFLICT, keep both until verified
- Never duplicate

## STEP 5: UPDATE OPEN TASKS
Read: memory/OPEN_TASKS.md (create if missing)
- Mark completed tasks as ✅
- Add new open tasks
- Prioritize by: 🔴 Critical / 🟡 High / 🟢 Medium

## STEP 6: WRITE LEARNING SUMMARY
Write to: memory/learning/{{TODAY}}-learned.md

Format:
---
Date: {{TODAY}}
Decisions: [list]
Mistakes: [list + root cause]
Wins: [list]
Lessons: [list]
Kaif patterns: [list]
Business intel: [list]
Open tasks updated: [count]
Confidence avg: [%]
---

## STEP 7: ARCHIVE RAW LOG
Move memory/{{TODAY}}.md → memory/archive/{{TODAY}}.md
Raw logs kept 30 days then auto-delete.

## STEP 8: SELF-REPORT TO KAIF (via Telegram)
Send one message:
"📚 Daily learning done.
Wins: [X] | Mistakes: [X] | Lessons: [X]
Top lesson: [single most important line]
Open tasks: [X] pending"

DONE. Stop. Do not over-explain.
CRON SETUP
# Daily at midnight IST (18:30 UTC)
30 18 * * * /home/ubuntu/.openclaw/scripts/daily-learning.sh
daily-learning.sh:
#!/bin/bash
TODAY=$(date +%Y-%m-%d)
cd /home/ubuntu/.openclaw/workspace

# Run learning skill via OpenClaw
openclaw run skill recursive-learning \
 --var TODAY=$TODAY \
 --model meta-llama/llama-3.3-70b-instruct:free \
 --max-tokens 4000
INFINITE MEMORY ARCHITECTURE
Problem: Files grow → token load grows → slow + expensive.
Solution: 3-tier memory system
Tier 1: RAW (daily logs)
→ Full detail, kept 30 days
→ Path: memory/YYYY-MM-DD.md
→ Auto-archived after processing

Tier 2: LEARNED (weekly distillation)
→ Compressed, high-signal only
→ Path: memory/learning/YYYY-MM-DD-learned.md
→ Kept 6 months

Tier 3: PERMANENT (always loaded)
→ Ultra-compressed, never grows beyond 2000 tokens
→ Path: memory/MEMORY.md
→ Only highest-confidence, most relevant facts
→ Old facts replaced when new ones contradict
Result: Token load stays constant. Intelligence grows forever.
MEMORY.md SIZE CONTROL
If MEMORY.md exceeds 2000 tokens:
Score all entries by: recency + confidence + relevance to R Company
Bottom 20% → move to archive
MEMORY.md stays lean
Rule: Quality over quantity. One verified fact beats ten guesses.
WHAT GETS PERMANENTLY REMEMBERED
✅ Always keep:
Kaif's preferences and communication patterns
R Company pricing, buyers, active orders
Mistakes with root causes (never repeat)
Verified market data (with date stamp)
Working strategies and what made them work
❌ Never keep permanently:
Greetings, small talk
Unverified claims
Outdated prices (replace, don't append)
Duplicate information
STATUS
🟢 Ready to deploy | Cron: daily midnight IST | Memory cap: 2000 tokens
