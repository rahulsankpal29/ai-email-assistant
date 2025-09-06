from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
from database import get_db, Email
from email_handler import EmailFetcher
from ai_processor import AIProcessor
import config
import threading
import time

app = Flask(__name__)
CORS(app)

# Initialize components
email_fetcher = EmailFetcher(
    config.Config.EMAIL_SERVER,
    config.Config.EMAIL_USERNAME,
    config.Config.EMAIL_PASSWORD
)
ai_processor = AIProcessor()

# Background email processing function
def process_emails_periodically():
    while True:
        try:
            with app.app_context():
                db = next(get_db())
                
                # Fetch new emails
                emails = email_fetcher.fetch_emails(since_days=1)
                email_fetcher.save_emails_to_db(db, emails)
                
                # Process unprocessed emails
                unprocessed_emails = db.query(Email).filter(Email.is_processed == False).all()
                
                for email in unprocessed_emails:
                    email_data = {
                        'sender': email.sender,
                        'subject': email.subject,
                        'body': email.body
                    }
                    
                    # Process with AI
                    result = ai_processor.process_email(email_data)
                    
                    # Update email record
                    email.sentiment = result['sentiment']
                    email.priority = result['priority']
                    email.extracted_info = result['extracted_info']
                    email.response = result['response']
                    email.is_processed = True
                    
                    db.commit()
                
        except Exception as e:
            print(f"Error processing emails: {e}")
        
        # Wait for 5 minutes before checking again
        time.sleep(300)

# Start background thread
processing_thread = threading.Thread(target=process_emails_periodically)
processing_thread.daemon = True
processing_thread.start()

# API Routes
@app.route('/api/emails', methods=['GET'])
def get_emails():
    try:
        db = next(get_db())
        emails = db.query(Email).order_by(Email.received_at.desc()).all()
        
        result = []
        for email in emails:
            result.append({
                'id': email.id,
                'message_id': email.message_id,
                'sender': email.sender,
                'subject': email.subject,
                'body': email.body,
                'received_at': email.received_at.isoformat() if email.received_at else None,
                'sentiment': email.sentiment,
                'priority': email.priority,
                'extracted_info': email.extracted_info,
                'response': email.response,
                'is_processed': email.is_processed,
                'created_at': email.created_at.isoformat() if email.created_at else None
            })
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/emails/stats', methods=['GET'])
def get_stats():
    try:
        db = next(get_db())
        
        # Total emails in last 24 hours
        last_24h = datetime.utcnow() - timedelta(hours=24)
        total_emails = db.query(Email).filter(Email.created_at >= last_24h).count()
        
        # Processed emails
        processed_emails = db.query(Email).filter(Email.is_processed == True, 
                                                Email.created_at >= last_24h).count()
        
        # Pending emails
        pending_emails = total_emails - processed_emails
        
        # Sentiment distribution
        sentiment_counts = {
            'Positive': db.query(Email).filter(Email.sentiment == 'Positive', 
                                             Email.created_at >= last_24h).count(),
            'Negative': db.query(Email).filter(Email.sentiment == 'Negative', 
                                             Email.created_at >= last_24h).count(),
            'Neutral': db.query(Email).filter(Email.sentiment == 'Neutral', 
                                            Email.created_at >= last_24h).count()
        }
        
        # Priority distribution
        priority_counts = {
            'Urgent': db.query(Email).filter(Email.priority == 'Urgent', 
                                           Email.created_at >= last_24h).count(),
            'Not Urgent': db.query(Email).filter(Email.priority == 'Not Urgent', 
                                               Email.created_at >= last_24h).count()
        }
        
        return jsonify({
            'total_emails': total_emails,
            'processed_emails': processed_emails,
            'pending_emails': pending_emails,
            'sentiment_counts': sentiment_counts,
            'priority_counts': priority_counts
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/emails/<int:email_id>/response', methods=['POST'])
def update_response(email_id):
    try:
        db = next(get_db())
        email = db.query(Email).filter(Email.id == email_id).first()
        
        if not email:
            return jsonify({'error': 'Email not found'}), 404
        
        data = request.get_json()
        if 'response' not in data:
            return jsonify({'error': 'Response text is required'}), 400
        
        email.response = data['response']
        db.commit()
        
        return jsonify({'message': 'Response updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=config.Config.DEBUG, port=5000)