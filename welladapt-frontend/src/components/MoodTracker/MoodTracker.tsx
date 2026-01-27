import React, { useState } from 'react';
import MoodCheckIn from './MoodCheckIn';
import MoodHistory from './MoodHistory';
import './MoodTracker.css';

interface MoodTrackerProps {
  sessionId: string;
}

const MoodTracker: React.FC<MoodTrackerProps> = ({ sessionId }) => {
  const [activeTab, setActiveTab] = useState<'checkin' | 'history'>('checkin');
  const [refreshHistory, setRefreshHistory] = useState(0);

  const handleMoodSubmitted = () => {
    // Trigger history refresh
    setRefreshHistory((prev) => prev + 1);
    setActiveTab('history');
  };

  return (
    <div className="mood-tracker-container">
      <div className="mood-tracker-tabs">
        <button
          className={`tab ${activeTab === 'checkin' ? 'active' : ''}`}
          onClick={() => setActiveTab('checkin')}
        >
          📝 Check-in
        </button>
        <button
          className={`tab ${activeTab === 'history' ? 'active' : ''}`}
          onClick={() => setActiveTab('history')}
        >
          📊 History
        </button>
      </div>

      <div className="mood-tracker-content">
        {activeTab === 'checkin' ? (
          <MoodCheckIn sessionId={sessionId} onMoodSubmitted={handleMoodSubmitted} />
        ) : (
          <MoodHistory key={refreshHistory} sessionId={sessionId} />
        )}
      </div>
    </div>
  );
};

export default MoodTracker;