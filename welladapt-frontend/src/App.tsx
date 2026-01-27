import React, { useState, useEffect } from 'react';
import ChatInterface from './components/Chat/ChatInterface';
import CrisisResources from './components/Resources/CrisisResources';
import { apiService } from './services/apiService';
import './App.css';

function App() {
  const [showResources, setShowResources] = useState(false);
  const [backendStatus, setBackendStatus] = useState<'checking' | 'online' | 'offline'>('checking');

  useEffect(() => {
    checkBackendHealth();
  }, []);

  const checkBackendHealth = async () => {
    try {
      await apiService.checkHealth();
      setBackendStatus('online');
    } catch (error) {
      setBackendStatus('offline');
    }
  };

  if (backendStatus === 'checking') {
    return (
      <div className="loading-screen">
        <h2>Connecting to WellAdapt...</h2>
        <div className="spinner"></div>
      </div>
    );
  }

  if (backendStatus === 'offline') {
    return (
      <div className="error-screen">
        <h2> Cannot connect to backend</h2>
        <p>Please make sure the backend server is running on port 5000</p>
        <button onClick={checkBackendHealth} className="retry-button">
          Retry Connection
        </button>
      </div>
    );
  }

  return (
    <div className="App">
      <ChatInterface onShowResources={() => setShowResources(true)} />
      
      {showResources && (
        <CrisisResources onClose={() => setShowResources(false)} />
      )}
    </div>
  );
}

export default App;