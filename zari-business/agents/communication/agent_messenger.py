#!/usr/bin/env python3
"""
Agent-to-Agent Communication System
JARVIS v2.0 - 19-Agent Architecture
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Any

class AgentMessenger:
    def __init__(self):
        self.agents = self.load_agents()
        self.message_queue = []
        self.shared_memory = {}
        
    def load_agents(self):
        """Load agent definitions"""
        with open('agent_definitions.json', 'r') as f:
            data = json.load(f)
        
        agents = {}
        for category, agent_list in data['agent_architecture']['agent_types'].items():
            for agent in agent_list['agents']:
                agents[agent['id']] = {
                    **agent,
                    'category': category,
                    'message_history': [],
                    'last_active': None
                }
        return agents
    
    def send_message(self, from_agent: str, to_agent: str, message_type: str, content: Dict):
        """Send message between agents"""
        message = {
            'id': f"msg_{len(self.message_queue) + 1:04d}",
            'from': from_agent,
            'to': to_agent,
            'type': message_type,
            'content': content,
            'timestamp': datetime.now().isoformat(),
            'status': 'pending'
        }
        
        self.message_queue.append(message)
        
        # Update agent histories
        if from_agent in self.agents:
            self.agents[from_agent]['message_history'].append({
                'direction': 'sent',
                'message_id': message['id']
            })
            self.agents[from_agent]['last_active'] = datetime.now().isoformat()
        
        if to_agent in self.agents:
            self.agents[to_agent]['message_history'].append({
                'direction': 'received',
                'message_id': message['id']
            })
        
        return message
    
    def broadcast_message(self, from_agent: str, category: str, message_type: str, content: Dict):
        """Broadcast message to all agents in a category"""
        messages = []
        
        for agent_id, agent in self.agents.items():
            if agent['category'] == category and agent_id != from_agent:
                message = self.send_message(from_agent, agent_id, message_type, content)
                messages.append(message)
        
        return messages
    
    def update_shared_memory(self, key: str, value: Any, agent_id: str):
        """Update shared memory accessible by all agents"""
        self.shared_memory[key] = {
            'value': value,
            'updated_by': agent_id,
            'updated_at': datetime.now().isoformat()
        }
    
    def get_shared_memory(self, key: str = None):
        """Get shared memory data"""
        if key:
            return self.shared_memory.get(key)
        return self.shared_memory
    
    def process_message_queue(self):
        """Process pending messages"""
        processed = []
        
        for message in self.message_queue:
            if message['status'] == 'pending':
                # Simulate message processing
                message['status'] = 'delivered'
                message['delivered_at'] = datetime.now().isoformat()
                processed.append(message)
        
        return processed
    
    def get_agent_status(self):
        """Get status of all agents"""
        status = {}
        
        for agent_id, agent in self.agents.items():
            status[agent_id] = {
                'name': agent['name'],
                'status': agent['status'],
                'messages_sent': len([m for m in agent['message_history'] if m['direction'] == 'sent']),
                'messages_received': len([m for m in agent['message_history'] if m['direction'] == 'received']),
                'last_active': agent['last_active']
            }
        
        return status
    
    def get_system_analytics(self):
        """Get system-wide analytics"""
        active_agents = len([a for a in self.agents.values() if a['status'] == 'active'])
        total_messages = len(self.message_queue)
        processed_messages = len([m for m in self.message_queue if m['status'] == 'delivered'])
        
        return {
            'total_agents': len(self.agents),
            'active_agents': active_agents,
            'total_messages': total_messages,
            'processed_messages': processed_messages,
            'shared_memory_keys': len(self.shared_memory),
            'timestamp': datetime.now().isoformat()
        }

# Test the system
if __name__ == "__main__":
    print("🤖 Agent Communication System - JARVIS v2.0")
    print("=" * 50)
    
    # Initialize
    messenger = AgentMessenger()
    
    print(f"✅ Loaded {len(messenger.agents)} agents")
    
    # Test communication
    message = messenger.send_message(
        'research_agent_01',
        'strategy_agent_01',
        'data_insights',
        {'insight': 'High demand for bridal zari in UAE market'}
    )
    
    print(f"\n📨 Message sent: {message['id']}")
    
    # Update shared memory
    messenger.update_shared_memory(
        'market_insights',
        {'uae_demand': 'high', 'price_range': '50k-200k'},
        'research_agent_01'
    )
    
    # Process queue
    processed = messenger.process_message_queue()
    print(f"📬 Processed {len(processed)} messages")
    
    # Analytics
    analytics = messenger.get_system_analytics()
    print("\n📈 System Analytics:")
    print(json.dumps(analytics, indent=2))
    
    # Agent status
    status = messenger.get_agent_status()
    print(f"\n👥 Agent Status: {len(status)} agents tracked")
