import openai
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import re
import json
from datetime import datetime
import config

# Download NLTK data
nltk.download('vader_lexicon')

class AIProcessor:
    def __init__(self):
        openai.api_key = config.Config.OPENAI_API_KEY
        self.sia = SentimentIntensityAnalyzer()
        
    def analyze_sentiment(self, text):
        scores = self.sia.polarity_scores(text)
        if scores['compound'] >= 0.05:
            return "Positive"
        elif scores['compound'] <= -0.05:
            return "Negative"
        else:
            return "Neutral"
    
    def determine_priority(self, text):
        urgent_keywords = ['urgent', 'immediately', 'asap', 'critical', 'emergency', 'cannot access', 'broken', 'not working']
        text_lower = text.lower()
        if any(keyword in text_lower for keyword in urgent_keywords):
            return "Urgent"
        return "Not Urgent"
    
    def extract_information(self, text):
        # Extract phone numbers
        phone_pattern = r'(\+?\d{1,3}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4})'
        phones = re.findall(phone_pattern, text)
        
        # Extract emails
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        emails = re.findall(email_pattern, text)
        
        return {
            'phone_numbers': list(set(phones)),
            'emails': list(set(emails))
        }
    
    def generate_response(self, email_subject, email_body, sender):
        # Load knowledge base
        try:
            with open('../knowledge_base/faq.json', 'r') as f:
                knowledge_base = json.load(f)
        except:
            knowledge_base = {}
        
        # Create context for the AI
        context = f"""
        You are a customer support representative. Respond to the following email.
        
        Sender: {sender}
        Subject: {email_subject}
        Email Content: {email_body}
        
        Knowledge Base:
        {json.dumps(knowledge_base, indent=2)}
        
        Guidelines:
        - Be professional and friendly
        - If the customer seems frustrated, acknowledge their frustration
        - Reference specific products if mentioned
        - Offer helpful solutions
        - Keep the response concise but thorough
        - Sign off with "Best regards, Support Team"
        """
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful customer support assistant."},
                    {"role": "user", "content": context}
                ],
                max_tokens=500,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def process_email(self, email_data):
        # Analyze sentiment
        sentiment = self.analyze_sentiment(email_data['body'])
        
        # Determine priority
        priority = self.determine_priority(email_data['subject'] + " " + email_data['body'])
        
        # Extract information
        extracted_info = self.extract_information(email_data['body'])
        
        # Generate response
        response = self.generate_response(
            email_data['subject'], 
            email_data['body'], 
            email_data['sender']
        )
        
        return {
            'sentiment': sentiment,
            'priority': priority,
            'extracted_info': json.dumps(extracted_info),
            'response': response
        }