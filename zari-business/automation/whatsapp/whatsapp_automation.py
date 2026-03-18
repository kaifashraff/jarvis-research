#!/usr/bin/env python3
"""
WhatsApp Business Automation System
JARVIS v2.0 - Zari Business
"""

import json
import time
import random
from datetime import datetime, timedelta

class WhatsAppAutomation:
    def __init__(self):
        self.templates = self.load_templates()
        self.sent_messages = []
        self.responses = []
        
    def load_templates(self):
        """Load message templates"""
        return {
            'initial_contact': {
                'template': """🌟 Namaste {name} ji!

Main {sender_name} se {business_name}. Hum premium zari embroidery ka kaam karte hain - bridal wear, designer outfits, aur ethnic garments ke liye.

✨ Hamari specialties:
• Hand zari & zardozi work
• Custom designs
• Premium quality guarantee
• Timely delivery

Kya hum aapke liye ek sample piece bana sakte hain? Free consultation ke liye reply karein!

📞 {contact_number}""",
                'variables': ['name', 'sender_name', 'business_name', 'contact_number']
            },
            'follow_up': {
                'template': """🙏 {name} ji, namaste!

Kya aapne hamara previous message dekha? Hum {business_name} se hain - premium zari embroidery specialists.

🎯 Aapke business ke liye special offer:
• 20% discount on first order
• Free sample piece
• Flexible payment terms

Kya hum aapse 5 minute baat kar sakte hain?

📞 {contact_number}
🌐 {website}""",
                'variables': ['name', 'business_name', 'contact_number', 'website']
            },
            'quotation': {
                'template': """📋 {name} ji,

Aapke requirements ke liye quotation:

🎯 Order Details:
• Design: {design_type}
• Quantity: {quantity} pieces
• Timeline: {timeline} days
• Price: ₹{price} per piece

💎 Total: ₹{total_price}

✅ Includes:
• Premium zari thread
• Hand embroidery
• Quality guarantee
• Free delivery

Order confirm karne ke liye 'YES' reply karein!

📞 {contact_number}""",
                'variables': ['name', 'design_type', 'quantity', 'timeline', 'price', 'total_price', 'contact_number']
            }
        }
    
    def personalize_message(self, template_name, lead_data):
        """Personalize message with lead data"""
        template = self.templates[template_name]['template']
        variables = self.templates[template_name]['variables']
        
        # Replace variables
        message = template
        for var in variables:
            if var in lead_data:
                message = message.replace('{' + var + '}', str(lead_data[var]))
        
        return message
    
    def send_message(self, phone, message, lead_id):
        """Simulate sending WhatsApp message"""
        # In real implementation, this would use WhatsApp Business API
        print(f"📱 Sending to {phone}...")
        print(f"📝 Message preview: {message[:100]}...")
        
        # Simulate sending delay
        time.sleep(1)
        
        # Log sent message
        self.sent_messages.append({
            'lead_id': lead_id,
            'phone': phone,
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'status': 'sent'
        })
        
        print(f"✅ Message sent to {phone}")
        return True
    
    def schedule_follow_up(self, lead_id, days_delay=3):
        """Schedule follow-up message"""
        follow_up_date = datetime.now() + timedelta(days=days_delay)
        
        print(f"📅 Follow-up scheduled for {follow_up_date.strftime('%Y-%m-%d')}")
        return {
            'lead_id': lead_id,
            'scheduled_date': follow_up_date.isoformat(),
            'status': 'scheduled'
        }
    
    def generate_campaign(self, leads_data, campaign_type='initial'):
        """Generate complete outreach campaign"""
        print(f"🎯 Generating {campaign_type} campaign...")
        
        campaign_results = []
        
        for lead in leads_data:
            # Personalize message
            if campaign_type == 'initial':
                message = self.personalize_message('initial_contact', lead)
            elif campaign_type == 'follow_up':
                message = self.personalize_message('follow_up', lead)
            
            # Send message
            success = self.send_message(lead['phone'], message, lead['id'])
            
            if success:
                # Schedule follow-up
                follow_up = self.schedule_follow_up(lead['id'])
                
                campaign_results.append({
                    'lead_id': lead['id'],
                    'name': lead['name'],
                    'phone': lead['phone'],
                    'message_sent': True,
                    'follow_up_scheduled': follow_up,
                    'campaign_type': campaign_type
                })
        
        return campaign_results
    
    def get_analytics(self):
        """Get campaign analytics"""
        total_sent = len(self.sent_messages)
        
        return {
            'total_messages_sent': total_sent,
            'campaigns_run': 1,
            'last_updated': datetime.now().isoformat()
        }

# Test the system
if __name__ == "__main__":
    print("🤖 WhatsApp Automation System - JARVIS v2.0")
    print("=" * 50)
    
    # Initialize
    wa_bot = WhatsAppAutomation()
    
    # Sample leads
    sample_leads = [
        {
            'id': 'IND001',
            'name': 'Sabyasachi',
            'business': 'Sabyasachi Couture',
            'phone': '+91-9876543210',
            'sender_name': 'JARVIS Team',
            'business_name': 'Premium Zari Works',
            'contact_number': '+91-9876543211',
            'website': 'https://premiumzari.com'
        }
    ]
    
    # Generate campaign
    results = wa_bot.generate_campaign(sample_leads, 'initial')
    
    print("\n📊 Campaign Results:")
    print(json.dumps(results, indent=2))
    
    # Analytics
    analytics = wa_bot.get_analytics()
    print("\n📈 Analytics:")
    print(json.dumps(analytics, indent=2))
