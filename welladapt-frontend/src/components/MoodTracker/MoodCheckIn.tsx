import React, { useState } from 'react';
import { apiService } from '../../services/apiService';
import './MoodCheckIn.css';

interface MoodCheckInProps {
  sessionId: string;
  onMoodSubmitted: () => void;
}

const MOOD_LABELS = {
  1: { emoji: '😢', label: 'Very Bad', color: '#ef5350' },
  2: { emoji: '😔', label: 'Bad', color: '#ff7043' },
  3: { emoji: '😐', label: 'Okay', color: '#ffa726' },
  4: { emoji: '🙂', label: 'Good', color: '#66bb6a' },
  5: { emoji: '😄', label: 'Very Good', color: '#26a69a' },
};

const COMMON_ACTIVITIES = [
  'Studying', 'Exercise', 'Sleep', 'Social', 'Exams', 
  'Reading', 'Gaming', 'Music', 'Meditation', 'Walking'
];

const COMMON_TRIGGERS = [
  'Exam Stress', 'Assignment', 'Financial Worry', 'Social Pressure',
  'Family Issues', 'Sleep Deprivation', 'Loneliness', 'Health Concerns'
];

const MoodCheckIn: React.FC<MoodCheckInProps> = ({ sessionId, onMoodSubmitted }) => {
  const [selectedMood, setSelectedMood] = useState<number | null>(null);
  const [note, setNote] = useState('');
  const [selectedActivities, setSelectedActivities] = useState<string[]>([]);
  const [selectedTriggers, setSelectedTriggers] = useState<string[]>([]);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showSuccess, setShowSuccess] = useState(false);

  const toggleActivity = (activity: string) => {
    setSelectedActivities((prev) =>
      prev.includes(activity)
        ? prev.filter((a) => a !== activity)
        : [...prev, activity]
    );
  };

  const toggleTrigger = (trigger: string) => {
    setSelectedTriggers((prev) =>
      prev.includes(trigger)
        ? prev.filter((t) => t !== trigger)
        : [...prev, trigger]
    );
  };

  const handleSubmit = async () => {
    if (!selectedMood) return;

    setIsSubmitting(true);

    try {
      await apiService.submitMoodEntry({
        mood: selectedMood,
        note: note.trim(),
        sessionId,
        activities: selectedActivities,
        triggers: selectedTriggers,
      });

      setShowSuccess(true);
      
      // Reset form
      setTimeout(() => {
        setSelectedMood(null);
        setNote('');
        setSelectedActivities([]);
        setSelectedTriggers([]);
        setShowSuccess(false);
        onMoodSubmitted();
      }, 2000);
    } catch (error) {
      console.error('Failed to submit mood:', error);
      alert('Failed to save mood entry. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  if (showSuccess) {
    return (
      <div className="mood-success">
        <div className="success-icon">✓</div>
        <h3>Mood Recorded!</h3>
        <p>Thank you for checking in</p>
      </div>
    );
  }

  return (
    <div className="mood-checkin">
      <h2>How are you feeling today?</h2>
      
      {/* Mood Selection */}
      <div className="mood-selector">
        {Object.entries(MOOD_LABELS).map(([value, data]) => (
          <button
            key={value}
            className={`mood-button ${selectedMood === parseInt(value) ? 'selected' : ''}`}
            onClick={() => setSelectedMood(parseInt(value))}
            style={{
              borderColor: selectedMood === parseInt(value) ? data.color : '#ddd',
            }}
          >
            <span className="mood-emoji">{data.emoji}</span>
            <span className="mood-label">{data.label}</span>
          </button>
        ))}
      </div>

      {selectedMood && (
        <>
          {/* Activities */}
          <div className="section">
            <h3>What did you do today?</h3>
            <div className="tag-grid">
              {COMMON_ACTIVITIES.map((activity) => (
                <button
                  key={activity}
                  className={`tag ${selectedActivities.includes(activity) ? 'selected' : ''}`}
                  onClick={() => toggleActivity(activity)}
                >
                  {activity}
                </button>
              ))}
            </div>
          </div>

          {/* Triggers (only show if mood is low) */}
          {selectedMood <= 3 && (
            <div className="section">
              <h3>What's affecting your mood?</h3>
              <div className="tag-grid">
                {COMMON_TRIGGERS.map((trigger) => (
                  <button
                    key={trigger}
                    className={`tag trigger ${selectedTriggers.includes(trigger) ? 'selected' : ''}`}
                    onClick={() => toggleTrigger(trigger)}
                  >
                    {trigger}
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Note */}
          <div className="section">
            <h3>Anything else? (Optional)</h3>
            <textarea
              className="mood-note"
              placeholder="Write a note about your day..."
              value={note}
              onChange={(e) => setNote(e.target.value)}
              maxLength={500}
              rows={3}
            />
            <div className="char-count">{note.length}/500</div>
          </div>

          {/* Submit */}
          <button
            className="submit-mood-button"
            onClick={handleSubmit}
            disabled={isSubmitting}
          >
            {isSubmitting ? 'Saving...' : 'Save Mood Check-in'}
          </button>
        </>
      )}
    </div>
  );
};

export default MoodCheckIn;