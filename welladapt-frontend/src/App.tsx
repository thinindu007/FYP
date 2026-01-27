import React, { useState, useEffect } from 'react';
import ChatInterface from './components/Chat/ChatInterface';
import CrisisResources from './components/Resources/CrisisResources';
import MoodTracker from './components/MoodTracker/MoodTracker';
import { apiService } from './services/apiService';
import './App.css';

// Generate session ID (in production, this would be more sophisticated)
const getSessionId = () => {
  let sessionId = localStorage.getItem('welladapt-session-id');
  if (!sessionId) {
    sessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    localStorage.setItem('welladapt-session-id', sessionId);
  }
  return sessionId;
};

function App() {
  const [showResources, setShowResources] = useState(false);
  const [activeView, setActiveView] = useState<'chat' | 'mood'>('chat');
  const [backendStatus, setBackendStatus] = useState<'checking' | 'online' | 'offline'>('checking');
  const [sessionId] = useState(getSessionId());

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
      {/* Navigation */}
      <div className="app-navigation">
        <button
          className={`nav-button ${activeView === 'chat' ? 'active' : ''}`}
          onClick={() => setActiveView('chat')}
        >
          💬 Chat
        </button>
        <button
          className={`nav-button ${activeView === 'mood' ? 'active' : ''}`}
          onClick={() => setActiveView('mood')}
        >
          📊 Mood
        </button>
      </div>

      {/* Main Content */}
      {activeView === 'chat' ? (
        <ChatInterface onShowResources={() => setShowResources(true)} />
      ) : (
        <MoodTracker sessionId={sessionId} />
      )}
      
      {showResources && (
        <CrisisResources onClose={() => setShowResources(false)} />
      )}
    </div>
  );
}

export default App;