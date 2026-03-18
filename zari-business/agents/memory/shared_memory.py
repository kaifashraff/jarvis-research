#!/usr/bin/env python3
"""
Shared Memory System for 19-Agent Architecture
JARVIS v2.0 - Zari Business
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Any

class SharedMemory:
    def __init__(self):
        self.memory_store = {
            'global': {},
            'agent_specific': {},
            'project': {},
            'temporary': {}
        }
        self.access_log = []
        
    def store(self, key: str, value: Any, category: str = 'global', agent_id: str = None):
        """Store data in shared memory"""
        timestamp = datetime.now().isoformat()
        
        if category not in self.memory_store:
            self.memory_store[category] = {}
        
        self.memory_store[category][key] = {
            'value': value,
            'stored_by': agent_id,
            'stored_at': timestamp,
            'last_accessed': None,
            'access_count': 0
        }
        
        # Log access
        self.access_log.append({
            'operation': 'store',
            'key': key,
            'category': category,
            'agent_id': agent_id,
            'timestamp': timestamp
        })
        
        return True
    
    def retrieve(self, key: str, category: str = 'global', agent_id: str = None):
        """Retrieve data from shared memory"""
        if category not in self.memory_store:
            return None
        
        if key not in self.memory_store[category]:
            return None
        
        data = self.memory_store[category][key]
        
        # Update access stats
        data['last_accessed'] = datetime.now().isoformat()
        data['access_count'] += 1
        
        # Log access
        self.access_log.append({
            'operation': 'retrieve',
            'key': key,
            'category': category,
            'agent_id': agent_id,
            'timestamp': datetime.now().isoformat()
        })
        
        return data['value']
    
    def search(self, query: str, category: str = None):
        """Search memory for relevant data"""
        results = []
        
        search_categories = [category] if category else self.memory_store.keys()
        
        for cat in search_categories:
            if cat in self.memory_store:
                for key, data in self.memory_store[cat].items():
                    if query.lower() in key.lower() or query.lower() in str(data['value']).lower():
                        results.append({
                            'category': cat,
                            'key': key,
                            'value': data['value'],
                            'stored_by': data['stored_by'],
                            'stored_at': data['stored_at']
                        })
        
        return results
    
    def delete(self, key: str, category: str = 'global', agent_id: str = None):
        """Delete data from shared memory"""
        if category in self.memory_store and key in self.memory_store[category]:
            del self.memory_store[category][key]
            
            self.access_log.append({
                'operation': 'delete',
                'key': key,
                'category': category,
                'agent_id': agent_id,
                'timestamp': datetime.now().isoformat()
            })
            
            return True
        
        return False
    
    def get_memory_stats(self):
        """Get memory usage statistics"""
        stats = {
            'categories': {},
            'total_keys': 0,
            'total_accesses': len(self.access_log),
            'last_updated': datetime.now().isoformat()
        }
        
        for category, data in self.memory_store.items():
            stats['categories'][category] = {
                'keys': len(data),
                'total_accesses': sum(item['access_count'] for item in data.values())
            }
            stats['total_keys'] += len(data)
        
        return stats
    
    def export_memory(self, filepath: str):
        """Export memory to JSON file"""
        with open(filepath, 'w') as f:
            json.dump(self.memory_store, f, indent=2, default=str)
        
        return True
    
    def import_memory(self, filepath: str):
        """Import memory from JSON file"""
        try:
            with open(filepath, 'r') as f:
                imported = json.load(f)
            
            # Merge with existing memory
            for category, data in imported.items():
                if category not in self.memory_store:
                    self.memory_store[category] = {}
                
                self.memory_store[category].update(data)
            
            return True
        except Exception as e:
            print(f"Import error: {e}")
            return False

# Test the system
if __name__ == "__main__":
    print("🧠 Shared Memory System - JARVIS v2.0")
    print("=" * 50)
    
    # Initialize
    memory = SharedMemory()
    
    # Store some data
    memory.store('market_research', {
        'uae_demand': 'high',
        'india_competition': 'medium',
        'uk_potential': 'growing'
    }, 'global', 'research_agent_01')
    
    memory.store('lead_scores', {
        'IND001': 300,
        'IND002': 290,
        'UAE001': 285
    }, 'project', 'strategy_agent_01')
    
    # Retrieve data
    market_data = memory.retrieve('market_research', 'global', 'strategy_agent_01')
    print(f"📊 Retrieved market data: {market_data is not None}")
    
    # Search
    results = memory.search('uae')
    print(f"🔍 Search results: {len(results)}")
    
    # Stats
    stats = memory.get_memory_stats()
    print(f"\n📈 Memory Stats:")
    print(f"Total keys: {stats['total_keys']}")
    print(f"Total accesses: {stats['total_accesses']}")
    
    # Export
    memory.export_memory('shared_memory_export.json')
    print("✅ Memory exported")
