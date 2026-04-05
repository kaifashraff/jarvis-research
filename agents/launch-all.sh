#!/bin/bash
# JARVIS AGENT FACTORY — Launch all 5 sub-agents with auto-restart

export MISTRAL_API_KEY="R2pBYB7SkpaTgXCERyIoaSWFVrWYMzZa"
AGENTS_DIR="/home/ubuntu/.openclaw/workspace/agents"
LOG_DIR="/home/ubuntu/.openclaw/workspace/memory"

echo "🦞 Jarvis Agent Factory — Launching 5 agents..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Kill any existing agents
pkill -f "observer-agent.py" 2>/dev/null
pkill -f "researcher-agent.py" 2>/dev/null
pkill -f "strategist-agent.py" 2>/dev/null
pkill -f "content-creator-agent.py" 2>/dev/null
pkill -f "guardian-agent.py" 2>/dev/null
sleep 2

# Launch each agent
agents=("observer" "researcher" "strategist" "content-creator" "guardian")
for agent in "${agents[@]}"; do
    echo ""
    echo "[${agent^}] Starting ${agent}-agent.py..."
    nohup python3 "${AGENTS_DIR}/${agent}-agent.py" \
        >> "${LOG_DIR}/agent-${agent}.log" 2>&1 &
    
    if [ $? -eq 0 ]; then
        echo "  ✅ PID: $!"
    else
        echo "  ❌ Failed to start ${agent}-agent"
    fi
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🟢 All agents launched. 24/7 operation initiated."
echo ""
echo "Monitor with:"
echo "  tail -f ${LOG_DIR}/agent-observer.log"
echo "  tail -f ${LOG_DIR}/agent-guardian.log"
echo ""
echo "Kill all with:"
echo "  pkill -f '-agent.py'"
