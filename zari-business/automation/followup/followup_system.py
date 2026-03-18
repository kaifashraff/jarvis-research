#!/usr/bin/env python3
"""
Intelligent Follow-up System
JARVIS v2.0 - Zari Business
"""

import json
from datetime import datetime, timedelta

class FollowUpSystem:
    def __init__(self):
        self.follow_up_rules = self.load_rules()
        self.scheduled_followups = []
        
    def load_rules(self):
        """Load follow-up rules"""
        return {
            'no_response': {
                'delay_days': 3,
                'max_attempts': 3,
                'channels': ['whatsapp', 'email']
            },
            'interested': {
                'delay_days': 1,
                'max_attempts': 5,
                'channels': ['whatsapp', 'call']
            },
            'quotation_sent': {
                'delay_days': 2,
                'max_attempts': 2,
                'channels': ['whatsapp', 'email']
            },
            'negotiation': {
                'delay_days': 1,
                'max_attempts': 3,
                'channels': ['call', 'whatsapp']
            }
        }
    
    def analyze_response(self, message):
        """Analyze customer response sentiment"""
        positive_keywords = ['interested', 'yes', 'ok', 'good', 'great', 'perfect', 'proceed']
        negative_keywords = ['no', 'not interested', 'busy', 'later', 'expensive']
        quotation_keywords = ['price', 'cost', 'quote', 'quotation', 'how much']
        
        message_lower = message.lower()
        
        if any(word in message_lower for word in positive_keywords):
            return 'interested'
        elif any(word in message_lower for word in negative_keywords):
            return 'not_interested'
        elif any(word in message_lower for word in quotation_keywords):
            return 'quotation_requested'
        else:
            return 'neutral'
    
    def schedule_followup(self, lead_id, lead_status, last_contact):
        """Schedule follow-up based on lead status"""
        rules = self.follow_up_rules.get(lead_status, self.follow_up_rules['no_response'])
        
        next_followup = {
            'lead_id': lead_id,
            'status': lead_status,
            'scheduled_date': (datetime.now() + timedelta(days=rules['delay_days'])).isoformat(),
            'channels': rules['channels'],
            'max_attempts': rules['max_attempts'],
            'current_attempt': 1
        }
        
        self.scheduled_followups.append(next_followup)
        return next_followup
    
    def generate_followup_message(self, lead_data, attempt_number):
        """Generate personalized follow-up message"""
        if attempt_number == 1:
            return f"🙏 {lead_data['name']} ji, namaste! Kya aapne hamara previous message dekha?"
        elif attempt_number == 2:
            return f"🎯 {lead_data['name']} ji, special offer - 20% discount on first order!"
        else:
            return f"📞 {lead_data['name']} ji, kya hum aapse 5 minute baat kar sakte hain?"
    
    def get_analytics(self):
        """Get follow-up analytics"""
        return {
            'total_scheduled': len(self.scheduled_followups),
            'pending_followups': len([f for f in self.scheduled_followups if f['current_attempt'] < f['max_attempts']]),
            'last_updated': datetime.now().isoformat()
        }

# Test the system
if __name__ == "__main__":
    print("🔄 Follow-up System - JARVIS v2.0")
    print("=" * 50)
    
    # Initialize
    followup_bot = FollowUpSystem()
    
    # Test response analysis
    test_responses = [
        "Haan, I'm interested in your zari work",
        "What's the price for 100 pieces?",
        "Not interested right now",
        "Can you send me more details?"
    ]
    
    print("\n🔍 Response Analysis:")
    for response in test_responses:
        analysis = followup_bot.analyze_response(response)
        print(f"Response: '{response}' → {analysis}")
    
    # Schedule follow-ups
    sample_lead = {
        'id': 'IND001',
        'name': 'Sabyasachi',
        'business': 'Sabyasachi Couture'
    }
    
    followup = followup_bot.schedule_followup('IND001', 'no_response', datetime.now())
    
    print("\n📅 Scheduled Follow-up:")
    print(json.dumps(followup, indent=2))
    
    # Analytics
    analytics = followup_bot.get_analytics()
    print("\n📈 Analytics:")
    print(json.dumps(analytics, indent=2))
