import React from 'react';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const StatsDashboard = ({ stats }) => {
  const sentimentData = [
    { name: 'Positive', value: stats.sentiment_counts?.Positive || 0 },
    { name: 'Negative', value: stats.sentiment_counts?.Negative || 0 },
    { name: 'Neutral', value: stats.sentiment_counts?.Neutral || 0 },
  ];

  const priorityData = [
    { name: 'Urgent', value: stats.priority_counts?.Urgent || 0 },
    { name: 'Not Urgent', value: stats.priority_counts?.['Not Urgent'] || 0 },
  ];

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];
  const SENTIMENT_COLORS = {
    Positive: '#00C49F',
    Negative: '#FF8042',
    Neutral: '#FFBB28'
  };

  return (
    <div className="stats-dashboard">
      <h2>Dashboard Overview</h2>
      
      <div className="stats-cards">
        <div className="stat-card">
          <h3>Total Emails (24h)</h3>
          <p className="stat-number">{stats.total_emails || 0}</p>
        </div>
        
        <div className="stat-card">
          <h3>Processed</h3>
          <p className="stat-number">{stats.processed_emails || 0}</p>
        </div>
        
        <div className="stat-card">
          <h3>Pending</h3>
          <p className="stat-number">{stats.pending_emails || 0}</p>
        </div>
      </div>
      
      <div className="charts-container">
        <div className="chart">
          <h3>Email Sentiment</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={sentimentData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {sentimentData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={SENTIMENT_COLORS[entry.name]} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
        
        <div className="chart">
          <h3>Email Priority</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={priorityData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="value" fill="#8884d8" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
};

export default StatsDashboard;