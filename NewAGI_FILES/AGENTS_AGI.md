AGENTS_AGI.md v1.1 — Jarvis Multi-Agent System
ORCHESTRATOR
Session: agent:main
Model: qwen/qwen3-plus:free (OpenRouter)
Role: Route tasks, manage agents, synthesize output
Memory: MEMORY.md + daily logs
Tools: All OpenClaw tools + 82 skills
SUB-AGENTS (max 5 parallel)
Agent
Model
Purpose
Performance Marketer
Mistral:free
Instagram, Meta Ads
Deep Researcher
Qwen:free
Market intel, competitors
YouTube Strategist
Mistral:free
Scripts, SEO, channel
Business Strategist
Qwen:free
Pricing, revenue
RESEARCH SWARM (7 agents — 286KB done)
#
Topic
File
Size
1
Memory & Continuity
01-memory.md
52K
2
Reasoning & Decisions
02-reasoning.md
49K
3
Self-Improvement
03-self-improve.md
26K
4
Human-AI Symbiosis
04-symbiosis.md
24K
5
Master Synthesis
00-master.md
106K
6
Knowledge
05-epistemology.md
10K
7
Tools & Execution
06-tools.md
19K
82 SKILLS (by category)
Agent Framework: claude-code-skills, codex-cli, copilot-skills, gemini-cli, grok-code, openclaw-agent
Analytics: analytics, dashboard, tracker, data-analysis, metrics, monitoring, performance, telemetry
Social: instagram-agent, post-generator, linkedin, social-media, tiktok, twitter, youtube-agent, youtube-automation, youtube-faceless, content-optimizer, content-strategy
Comms: communication, discord, email-agent, messaging, notification, push, signal, slack, telegram, whatsapp
Strategy: business-strategy, competitive-analysis, market-research, pricing-calc, pricing-strategy, strategy, strategic-planning, swot
Brand: branding, brand-identity, pricing, pricing-engine, quote-generator, value-proposition
Memory: memory, memory-bank, memory-mcp, memory-graph, memory-palace, memory-processor
YouTube: niche-finder, optimizer, research, script
Content: content, content-wizard, copywriting, creative-writing, blog, article, script-writer, seo-content
Automation: automation, clawflow, code-builder, code-generator, python, shell, webhook, workflow
Web: web-research, scraper, seo, keyword-research, domain-checker, link-checker
Data: data-processor, visualizer, csv, json, excel, chart
Marketing: marketing, ad-copy, funnel-builder, landing-page
COMMUNICATION FLOW
Kaif → Orchestrator → Sub-agents → Synthesis → Telegram → Kaif
Research: Agent N → file → GitHub → Agent N+1 reads → builds on it
WHEN TO USE WHAT
Task
Mode
Quick answer
Single prompt
Analysis
Single agent
Research
Multi-agent
Full system build
Swarm
SAFETY RULES
Max 5 parallel agents
Max runtime: 10,800s per agent
No recursive spawning
Agents write own workspace only
No destructive commands
No direct API key access
Output validated before delivery
STATUS
🟢 Active | 19 roles | 4 sub-agents | 82 skills | 7 research done
Next: Phase 2 — Inter-agent communication
