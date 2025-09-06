import email
from imapclient import IMAPClient
import pyzmail
from datetime import datetime, timedelta
import re
from database import Email, get_db
from sqlalchemy.orm import Session

class EmailFetcher:
    def __init__(self, server, username, password):
        self.server = server
        self.username = username
        self.password = password
        self.client = None
        
    def connect(self):
        self.client = IMAPClient(self.server, ssl=True)
        self.client.login(self.username, self.password)
        self.client.select_folder('INBOX')
        
    def disconnect(self):
        if self.client:
            self.client.logout()
            
    def fetch_emails(self, since_days=1):
        if not self.client:
            self.connect()
            
        since_date = datetime.now() - timedelta(days=since_days)
        messages = self.client.search(['SINCE', since_date])
        
        email_data = []
        for uid, message_data in self.client.fetch(messages, ['RFC822']).items():
            raw_email = message_data[b'RFC822']
            msg = pyzmail.PyzMessage.factory(raw_email)
            
            subject = msg.get_subject()
            sender = msg.get_addresses('from')[0] if msg.get_addresses('from') else ('', '')
            body = self._get_email_body(msg)
            date = msg.get_decoded_header('date', '')
            
            # Check if email matches our filter criteria
            if self._is_support_email(subject):
                email_data.append({
                    'message_id': f"{uid}",
                    'sender': sender[1],
                    'subject': subject,
                    'body': body,
                    'received_at': date
                })
                
        return email_data
    
    def _get_email_body(self, msg):
        if msg.text_part:
            return msg.text_part.get_payload().decode(msg.text_part.charset)
        elif msg.html_part:
            return msg.html_part.get_payload().decode(msg.html_part.charset)
        return ""
    
    def _is_support_email(self, subject):
        support_keywords = ['support', 'query', 'request', 'help', 'issue', 'problem']
        subject_lower = subject.lower()
        return any(keyword in subject_lower for keyword in support_keywords)
    
    def save_emails_to_db(self, db: Session, emails):
        for email_data in emails:
            # Check if email already exists
            existing_email = db.query(Email).filter(Email.message_id == email_data['message_id']).first()
            if not existing_email:
                email_record = Email(
                    message_id=email_data['message_id'],
                    sender=email_data['sender'],
                    subject=email_data['subject'],
                    body=email_data['body'],
                    received_at=email_data['received_at']
                )
                db.add(email_record)
        db.commit()