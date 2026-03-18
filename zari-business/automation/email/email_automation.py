#!/usr/bin/env python3
"""
Email Cold Outreach Automation System
JARVIS v2.0 - Zari Business
"""

import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta

class EmailAutomation:
    def __init__(self):
        self.templates = self.load_templates()
        self.sent_emails = []
        
    def load_templates(self):
        """Load email templates"""
        return {
            'cold_outreach': {
                'subject': 'Premium Zari Embroidery Partnership - {business_name}',
                'body': """Dear {name},

I hope this email finds you well.

I am writing to introduce our premium zari embroidery services. We specialize in creating exquisite hand-embroidered pieces for bridal wear, designer collections, and ethnic garments.

Our services include:
• Hand zari and zardozi embroidery
• Custom design development
• Quality assurance guarantee
• Timely delivery
• Competitive pricing

We have worked with leading designers and boutiques across India, UAE, and UK. Our craftsmen have over 20 years of experience in traditional zari work.

I would love to discuss how we can support your upcoming collections. Could we schedule a brief call this week?

Best regards,
{sender_name}
{business_name}
{contact_number}
{website}""",
                'variables': ['name', 'business_name', 'sender_name', 'contact_number', 'website']
            },
            'follow_up': {
                'subject': 'Following Up - Zari Embroidery Partnership',
                'body': """Dear {name},

I wanted to follow up on my previous email regarding our zari embroidery services.

We are currently offering:
• 20% discount on first orders
• Free sample development
• Flexible payment terms

Many designers and boutiques have already benefited from our partnership. I believe we can add significant value to your business as well.

Would you be available for a 10-minute call this week to discuss your requirements?

Best regards,
{sender_name}""",
                'variables': ['name', 'sender_name']
            },
            'quotation': {
                'subject': 'Quotation - Zari Embroidery Services',
                'body': """Dear {name},

Thank you for your interest in our zari embroidery services.

Based on your requirements, here is our quotation:

Design: {design_type}
Quantity: {quantity} pieces
Timeline: {timeline} days
Price per piece: ₹{price}

Total: ₹{total_price}

This includes:
• Premium zari thread
• Hand embroidery
• Quality guarantee
• Free delivery

Please let me know if you would like to proceed or if you have any questions.

Best regards,
{sender_name}""",
                'variables': ['name', 'design_type', 'quantity', 'timeline', 'price', 'total_price', 'sender_name']
            }
        }
    
    def personalize_email(self, template_name, lead_data):
        """Personalize email with lead data"""
        template = self.templates[template_name]
        
        subject = template['subject']
        body = template['body']
        
        # Replace variables
        for var in template['variables']:
            if var in lead_data:
                subject = subject.replace('{' + var + '}', str(lead_data[var]))
                body = body.replace('{' + var + '}', str(lead_data[var]))
        
        return {'subject': subject, 'body': body}
    
    def send_email(self, to_email, subject, body, lead_id):
        """Simulate sending email"""
        print(f"📧 Sending email to {to_email}...")
        print(f"📝 Subject: {subject}")
        
        # Log sent email
        self.sent_emails.append({
            'lead_id': lead_id,
            'to': to_email,
            'subject': subject,
            'body': body,
            'timestamp': datetime.now().isoformat(),
            'status': 'sent'
        })
        
        print(f"✅ Email sent to {to_email}")
        return True
    
    def create_drip_campaign(self, leads_data, campaign_name="Zari Partnership"):
        """Create email drip campaign"""
        print(f"🎯 Creating drip campaign: {campaign_name}")
        
        campaign_schedule = []
        
        for i, lead in enumerate(leads_data):
            # Day 1: Initial outreach
            day1_email = self.personalize_email('cold_outreach', lead)
            campaign_schedule.append({
                'day': 1,
                'lead_id': lead['id'],
                'email': day1_email,
                'type': 'initial'
            })
            
            # Day 4: Follow-up
            campaign_schedule.append({
                'day': 4,
                'lead_id': lead['id'],
                'email': self.personalize_email('follow_up', lead),
                'type': 'follow_up'
            })
            
            # Day 7: Final follow-up
            campaign_schedule.append({
                'day': 7,
                'lead_id': lead['id'],
                'email': self.personalize_email('follow_up', lead),
                'type': 'final_follow_up'
            })
        
        return campaign_schedule
    
    def get_analytics(self):
        """Get email campaign analytics"""
        return {
            'total_emails_sent': len(self.sent_emails),
            'campaigns_active': 1,
            'last_updated': datetime.now().isoformat()
        }

# Test the system
if __name__ == "__main__":
    print("📧 Email Automation System - JARVIS v2.0")
    print("=" * 50)
    
    # Initialize
    email_bot = EmailAutomation()
    
    # Sample leads
    sample_leads = [
        {
            'id': 'IND001',
            'name': 'Sabyasachi Mukherjee',
            'business_name': 'Premium Zari Works',
            'sender_name': 'JARVIS Team',
            'contact_number': '+91-9876543211',
            'website': 'https://premiumzari.com'
        }
    ]
    
    # Create drip campaign
    campaign = email_bot.create_drip_campaign(sample_leads)
    
    print("\n📊 Drip Campaign Schedule:")
    for entry in campaign:
        print(f"Day {entry['day']}: {entry['type']} to {entry['lead_id']}")
    
    # Analytics
    analytics = email_bot.get_analytics()
    print("\n📈 Analytics:")
    print(json.dumps(analytics, indent=2))
