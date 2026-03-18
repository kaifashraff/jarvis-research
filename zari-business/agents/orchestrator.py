#!/usr/bin/env python3
"""
Agent Orchestrator - 19-Agent System Coordinator
JARVIS v2.0 - Zari Business
"""

import json
import time
from datetime import datetime

class AgentOrchestrator:
    def __init__(self):
        self.agents = self.load_agents()
        self.task_queue = []
        self.completed_tasks = []
        self.system_status = 'operational'
        
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
                    'current_task': None,
                    'task_history': [],
                    'performance_score': 100
                }
        return agents
    
    def assign_task(self, agent_id: str, task: Dict):
        """Assign task to specific agent"""
        if agent_id not in self.agents:
            return False
        
        agent = self.agents[agent_id]
        
        if agent['status'] != 'active':
            return False
        
        task_assignment = {
            'task_id': f"task_{len(self.task_queue) + 1:04d}",
            'agent_id': agent_id,
            'task': task,
            'assigned_at': datetime.now().isoformat(),
            'status': 'assigned',
            'priority': task.get('priority', 'medium')
        }
        
        self.task_queue.append(task_assignment)
        agent['current_task'] = task_assignment['task_id']
        
        return task_assignment
    
    def delegate_by_capability(self, task: Dict, required_capabilities: List):
        """Delegate task to agent with required capabilities"""
        suitable_agents = []
        
        for agent_id, agent in self.agents.items():
            if agent['status'] == 'active':
                agent_capabilities = set(agent['capabilities'])
                required = set(required_capabilities)
                
                if required.issubset(agent_capabilities):
                    suitable_agents.append((agent_id, agent['performance_score']))
        
        if not suitable_agents:
            return None
        
        # Sort by performance score
        suitable_agents.sort(key=lambda x: x[1], reverse=True)
        best_agent_id = suitable_agents[0][0]
        
        return self.assign_task(best_agent_id, task)
    
    def complete_task(self, task_id: str, result: Dict):
        """Mark task as completed"""
        for task in self.task_queue:
            if task['task_id'] == task_id:
                task['status'] = 'completed'
                task['completed_at'] = datetime.now().isoformat()
                task['result'] = result
                
                # Update agent
                agent_id = task['agent_id']
                if agent_id in self.agents:
                    self.agents[agent_id]['current_task'] = None
                    self.agents[agent_id]['task_history'].append(task_id)
                
                self.completed_tasks.append(task)
                self.task_queue.remove(task)
                
                return True
        
        return False
    
    def get_system_status(self):
        """Get overall system status"""
        active_agents = len([a for a in self.agents.values() if a['status'] == 'active'])
        pending_tasks = len([t for t in self.task_queue if t['status'] == 'assigned'])
        completed_tasks = len(self.completed_tasks)
        
        return {
            'system_status': self.system_status,
            'active_agents': active_agents,
            'total_agents': len(self.agents),
            'pending_tasks': pending_tasks,
            'completed_tasks': completed_tasks,
            'timestamp': datetime.now().isoformat()
        }
    
    def optimize_workload(self):
        """Optimize workload distribution"""
        # Find overloaded agents
        overloaded = []
        underloaded = []
        
        for agent_id, agent in self.agents.items():
            if agent['status'] == 'active':
                if agent['current_task'] and agent['performance_score'] < 70:
                    overloaded.append(agent_id)
                elif not agent['current_task'] and agent['performance_score'] > 80:
                    underloaded.append(agent_id)
        
        # Redistribute tasks if needed
        redistribution_count = 0
        for overloaded_agent in overloaded[:3]:  # Limit to 3 redistributions
            if underloaded:
                target_agent = underloaded.pop(0)
                # Task redistribution logic would go here
                redistribution_count += 1
        
        return {
            'redistributed_tasks': redistribution_count,
            'overloaded_agents': len(overloaded),
            'underloaded_agents': len(underloaded)
        }

# Test the orchestrator
if __name__ == "__main__":
    print("🎯 Agent Orchestrator - JARVIS v2.0")
    print("=" * 50)
    
    # Initialize
    orchestrator = AgentOrchestrator()
    
    print(f"✅ Loaded {len(orchestrator.agents)} agents")
    
    # Assign task
    task = {
        'type': 'market_research',
        'description': 'Research UAE embroidery market',
        'priority': 'high',
        'requirements': ['web_search', 'data_extraction']
    }
    
    assignment = orchestrator.delegate_by_capability(task, ['web_search', 'data_extraction'])
    
    if assignment:
        print(f"📋 Task assigned: {assignment['task_id']} to {assignment['agent_id']}")
    
    # Complete task
    result = {
        'findings': 'High demand for premium zari work in UAE',
        'confidence': 0.85,
        'sources': 5
    }
    
    if assignment:
        orchestrator.complete_task(assignment['task_id'], result)
        print(f"✅ Task completed: {assignment['task_id']}")
    
    # System status
    status = orchestrator.get_system_status()
    print(f"\n📈 System Status:")
    print(f"Active agents: {status['active_agents']}/{status['total_agents']}")
    print(f"Completed tasks: {status['completed_tasks']}")
    
    # Optimize
    optimization = orchestrator.optimize_workload()
    print(f"\n🔧 Workload optimization: {optimization['redistributed_tasks']} tasks redistributed")
