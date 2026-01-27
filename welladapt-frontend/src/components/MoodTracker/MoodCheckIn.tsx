import React, { useState } from 'react';

const MoodCheckIn: React.FC = () => {
  const [mood, setMood] = useState<string | null>(null);

  return (
    <div style={{ border: '1px solid #eee', padding: 12, borderRadius: 8, maxWidth: 420 }}>
      <h4>Mood Check-In</h4>
      <div style={{ display: 'flex', gap: 8 }}>
        {['Great', 'Okay', 'Not good'].map(m => (
          <button key={m} onClick={() => setMood(m)} style={{ padding: '8px 10px' }}>
            {m}
          </button>
        ))}
      </div>
      {mood && <div style={{ marginTop: 12 }}>You selected: <strong>{mood}</strong></div>}
    </div>
  );
};

export default MoodCheckIn;
