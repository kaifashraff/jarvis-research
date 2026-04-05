#!/bin/bash
cd /home/ubuntu/.openclaw/workspace/agents
python3 observer-agent.py > ../memory/agent-observer.log 2>&1 &
python3 researcher-agent.py > ../memory/agent-researcher.log 2>&1 &
python3 strategist-agent.py > ../memory/agent-strategist.log 2>&1 &
python3 content-creator-agent.py > ../memory/agent-content-creator.log 2>&1 &
python3 guardian-agent.py > ../memory/agent-guardian.log 2>&1 &
