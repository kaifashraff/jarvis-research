#!/usr/bin/env python3
"""
Main Automation Orchestrator
JARVIS v2.0 - Zari Business
"""

import json
import time
from datetime import datetime

# Import automation modules
import sys
sys.path.append('whatsapp')
sys.path.append('email')
sys.path.append('followup')

from whatsapp_automation import WhatsAppAutomation
from email_automation import EmailAutomation
from followup_system import FollowUpSystem

class AutomationOrchestrator:
    def __init__(self):
        self.whatsapp = WhatsAppAutomation()
        self.email = EmailAutomation()
        self.followup = FollowUpSystem()
        self.campaigns = []
        
    def load_leads(self, filepath):
        """Load leads from JSON file"""
        with open(filepath, 'r') as f:
            data = json.load(f)
        return data['leads']
    
    def run_full_campaign(self, leads_data, campaign_name="Zari Business Campaign"):
        """Run complete multi-channel campaign"""
        print(f"🚀 Starting campaign: {campaign_name}")
        print("=" * 50)
        
        campaign_results = {
            'campaign_name': campaign_name,
            'start_time': datetime.now().isoformat(),
            'leads_processed': 0,
            'whatsapp_sent': 0,
            'emails_sent': 0,
            'followups_scheduled': 0,
            'errors': []
        }
        
        for lead in leads_data:
            try:
                print(f"\n📞 Processing: {lead['name']}")
                
                # Step 1: WhatsApp initial contact
                wa_message = self.whatsapp.personalize_message('initial_contact', lead)
                wa_sent = self.whatsapp.send_message(lead['phone'], wa_message, lead['id'])
                if wa_sent:
                    campaign_results['whatsapp_sent'] += 1
                
                # Step 2: Email initial contact (if email available)
                if 'email' in lead:
                    email_content = self.email.personalize_email('cold_outreach', lead)
                    email_sent = self.email.send_email(
                        lead['email'], 
                        email_content['subject'], 
                        email_content['body'], 
                        lead['id']
                    )
                    if email_sent:
                        campaign_results['emails_sent'] += 1
                
                # Step 3: Schedule follow-up
                followup = self.followup.schedule_followup(lead['id'], 'no_response', datetime.now())
                campaign_results['followups_scheduled'] += 1
                
                campaign_results['leads_processed'] += 1
                
                # Small delay between leads
                time.sleep(2)
                
            except Exception as e:
                error_msg = f"Error processing {lead['name']}: {str(e)}"
                print(f"❌ {error_msg}")
                campaign_results['errors'].append(error_msg)
        
        campaign_results['end_time'] = datetime.now().isoformat()
        campaign_results['status'] = 'completed'
        
        # Save results
        with open(f'campaign_results_{campaign_name.replace(" ", "_")}.json', 'w') as f:
            json.dump(campaign_results, f, indent=2)
        
        return campaign_results
    
    def get_dashboard_data(self):
        """Get dashboard analytics"""
        return {
            'whatsapp': self.whatsapp.get_analytics(),
            'email': self.email.get_analytics(),
            'followup': self.followup.get_analytics(),
            'campaigns': len(self.campaigns),
            'last_updated': datetime.now().isoformat()
        }

# Test the orchestrator
if __name__ == "__main__":
    print("🎯 Main Automation Orchestrator - JARVIS v2.0")
    print("=" * 50)
    
    # Initialize
    orchestrator = AutomationOrchestrator()
    
    # Sample leads
    sample_leads = [
        {
            'id': 'IND001',
            'name': 'Sabyasachi',
            'business': 'Sabyasachi Couture',
            'phone': '+91-9876543210',
            'email': 'contact@sabyasachi.com',
            'sender_name': 'JARVIS Team',
            'business_name': 'Premium Zari Works',
            'contact_number': '+91-9876543211',
            'website': 'https://premiumzari.com'
        }
    ]
    
    # Run campaign
    results = orchestrator.run_full_campaign(sample_leads, "Test Campaign")
    
    print("\n📊 Campaign Results:")
    print(json.dumps(results, indent=2))
    
    # Dashboard
    dashboard = orchestrator.get_dashboard_data()
    print("\n📈 Dashboard:")
    print(json.dumps(dashboard, indent=2))
