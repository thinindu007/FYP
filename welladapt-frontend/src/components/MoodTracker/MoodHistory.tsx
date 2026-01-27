import React, { useState, useEffect } from 'react';
import { apiService } from '../../services/apiService';
import { MoodStats, MoodEntry } from '../../types/chat.types';
import './MoodHistory.css';

interface MoodHistoryProps {
  sessionId: string;
}

const MOOD_EMOJIS: { [key: number]: string } = {
  1: '😢',
  2: '😔',
  3: '😐',
  4: '🙂',
  5: '😄',
};

const MoodHistory: React.FC<MoodHistoryProps> = ({ sessionId }) => {
  const [stats, setStats] = useState<MoodStats | null>(null);
  const [period, setPeriod] = useState<'7d' | '30d' | '90d'>('7d');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadStats();
  }, [period, sessionId]);

  const loadStats = async () => {
    setLoading(true);
    try {
      const response = await apiService.getMoodStats(sessionId, period);
      setStats(response.data.stats);
    } catch (error) {
      console.error('Failed to load mood stats:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="mood-history-loading">Loading your mood history...</div>;
  }

  if (!stats || stats.totalEntries === 0) {
    return (
      <div className="mood-history-empty">
        <p>📊 No mood entries yet</p>
        <p className="subtitle">Start tracking your mood to see insights here</p>
      </div>
    );
  }

  const getTrendIcon = () => {
    if (stats.trend === 'improving') return '📈';
    if (stats.trend === 'declining') return '📉';
    return '➡️';
  };

  const getTrendColor = () => {
    if (stats.trend === 'improving') return '#26a69a';
    if (stats.trend === 'declining') return '#ef5350';
    return '#ffa726';
  };

  return (
    <div className="mood-history">
      {/* Period Selector */}
      <div className="period-selector">
        <button
          className={period === '7d' ? 'active' : ''}
          onClick={() => setPeriod('7d')}
        >
          7 Days
        </button>
        <button
          className={period === '30d' ? 'active' : ''}
          onClick={() => setPeriod('30d')}
        >
          30 Days
        </button>
        <button
          className={period === '90d' ? 'active' : ''}
          onClick={() => setPeriod('90d')}
        >
          90 Days
        </button>
      </div>

      {/* Summary Cards */}
      <div className="stats-grid">
        <div className="stat-card">
          <div className="stat-label">Average Mood</div>
          <div className="stat-value">
            {MOOD_EMOJIS[Math.round(stats.average)]} {stats.average.toFixed(1)}
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-label">Trend</div>
          <div className="stat-value" style={{ color: getTrendColor() }}>
            {getTrendIcon()} {stats.trend}
          </div>
        </div>

        <div className="stat-card">
          <div className="stat-label">Total Entries</div>
          <div className="stat-value">{stats.totalEntries}</div>
        </div>
      </div>

      {/* Mood Distribution */}
      <div className="distribution-section">
        <h3>Mood Distribution</h3>
        <div className="distribution-bars">
          {Object.entries(stats.distribution).map(([mood, count]) => {
            const percentage = (count / stats.totalEntries) * 100;
            return (
              <div key={mood} className="distribution-bar">
                <span className="bar-label">
                  {MOOD_EMOJIS[parseInt(mood)]}
                </span>
                <div className="bar-container">
                  <div
                    className="bar-fill"
                    style={{ width: `${percentage}%` }}
                  />
                </div>
                <span className="bar-count">{count}</span>
              </div>
            );
          })}
        </div>
      </div>

      {/* Top Triggers */}
      {stats.topTriggers && stats.topTriggers.length > 0 && (
        <div className="insights-section">
          <h3>Common Stress Triggers</h3>
          <div className="tag-list">
            {stats.topTriggers.map((item, index) => (
              <div key={index} className="insight-tag trigger">
                {item.trigger} <span className="count">×{item.count}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Top Activities */}
      {stats.topActivities && stats.topActivities.length > 0 && (
        <div className="insights-section">
          <h3>Most Common Activities</h3>
          <div className="tag-list">
            {stats.topActivities.map((item, index) => (
              <div key={index} className="insight-tag activity">
                {item.activity} <span className="count">×{item.count}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Recent Entries */}
      <div className="recent-entries-section">
        <h3>Recent Entries</h3>
        <div className="recent-entries">
          {stats.recentEntries.map((entry) => (
            <div key={entry.id} className="entry-card">
              <div className="entry-header">
                <span className="entry-mood">{MOOD_EMOJIS[entry.mood]}</span>
                <span className="entry-date">
                  {new Date(entry.timestamp).toLocaleDateString()}
                </span>
              </div>
              {entry.note && <p className="entry-note">{entry.note}</p>}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default MoodHistory;