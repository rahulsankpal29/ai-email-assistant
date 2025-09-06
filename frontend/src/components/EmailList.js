import React, { useState } from 'react';

const EmailList = ({ emails, onUpdateResponse }) => {
  const [editingId, setEditingId] = useState(null);
  const [editedResponse, setEditedResponse] = useState('');

  const handleEditClick = (email) => {
    setEditingId(email.id);
    setEditedResponse(email.response || '');
  };

  const handleSaveClick = (emailId) => {
    onUpdateResponse(emailId, editedResponse);
    setEditingId(null);
  };

  const handleCancelClick = () => {
    setEditingId(null);
    setEditedResponse('');
  };

  // Sort emails: urgent first, then by date
  const sortedEmails = [...emails].sort((a, b) => {
    if (a.priority === 'Urgent' && b.priority !== 'Urgent') return -1;
    if (a.priority !== 'Urgent' && b.priority === 'Urgent') return 1;
    return new Date(b.received_at) - new Date(a.received_at);
  });

  return (
    <div className="email-list">
      <h2>Support Emails</h2>
      <div className="emails-container">
        {sortedEmails.map(email => (
          <div key={email.id} className={`email-card ${email.priority?.toLowerCase()}`}>
            <div className="email-header">
              <div className="email-sender">{email.sender}</div>
              <div className="email-date">
                {new Date(email.received_at).toLocaleString()}
              </div>
              <div className={`priority-badge ${email.priority?.toLowerCase()}`}>
                {email.priority}
              </div>
              <div className={`sentiment-badge ${email.sentiment?.toLowerCase()}`}>
                {email.sentiment}
              </div>
            </div>
            
            <div className="email-subject">{email.subject}</div>
            <div className="email-body">{email.body}</div>
            
            {email.extracted_info && (
              <div className="extracted-info">
                <h4>Extracted Information:</h4>
                <pre>{email.extracted_info}</pre>
              </div>
            )}
            
            <div className="email-response">
              <h4>AI-Generated Response:</h4>
              {editingId === email.id ? (
                <div>
                  <textarea
                    value={editedResponse}
                    onChange={(e) => setEditedResponse(e.target.value)}
                    rows="6"
                  />
                  <div className="response-actions">
                    <button onClick={() => handleSaveClick(email.id)}>Save</button>
                    <button onClick={handleCancelClick}>Cancel</button>
                  </div>
                </div>
              ) : (
                <div>
                  <p>{email.response || 'No response generated yet.'}</p>
                  <button onClick={() => handleEditClick(email)}>
                    Edit Response
                  </button>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default EmailList;