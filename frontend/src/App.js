import React, { useState, useEffect } from 'react';
import axios from 'axios';
import EmailList from './components/EmailList';
import StatsDashboard from './components/StatsDashboard';
import './App.css';

function App() {
  const [emails, setEmails] = useState([]);
  const [stats, setStats] = useState({});
  const [activeTab, setActiveTab] = useState('dashboard');

  useEffect(() => {
    fetchEmails();
    fetchStats();
    
    // Refresh data every minute
    const interval = setInterval(() => {
      fetchEmails();
      fetchStats();
    }, 60000);
    
    return () => clearInterval(interval);
  }, []);

  const fetchEmails = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/emails');
      setEmails(response.data);
    } catch (error) {
      console.error('Error fetching emails:', error);
    }
  };

  const fetchStats = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/emails/stats');
      setStats(response.data);
    } catch (error) {
      console.error('Error fetching stats:', error);
    }
  };

  const updateResponse = async (emailId, response) => {
    try {
      await axios.post(`http://localhost:5000/api/emails/${emailId}/response`, {
        response
      });
      fetchEmails(); // Refresh the list
    } catch (error) {
      console.error('Error updating response:', error);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>AI-Powered Communication Assistant</h1>
        <nav>
          <button 
            className={activeTab === 'dashboard' ? 'active' : ''} 
            onClick={() => setActiveTab('dashboard')}
          >
            Dashboard
          </button>
          <button 
            className={activeTab === 'emails' ? 'active' : ''} 
            onClick={() => setActiveTab('emails')}
          >
            Emails ({emails.length})
          </button>
        </nav>
      </header>
      
      <main>
        {activeTab === 'dashboard' && <StatsDashboard stats={stats} />}
        {activeTab === 'emails' && (
          <EmailList emails={emails} onUpdateResponse={updateResponse} />
        )}
      </main>
    </div>
  );
}

export default App;