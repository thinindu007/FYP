const config = require('../config/config');

let moodEntries = [];

class MoodController {
 
  async submitMoodEntry(req, res, next) {
    try {
      const { mood, note, sessionId, activities, triggers } = req.body;

      const entry = {
        id: `mood_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
        sessionId,
        mood,
        note: note || '',
        activities: activities || [],
        triggers: triggers || [],
        timestamp: new Date().toISOString(),
      };

      // Store entry
      moodEntries.push(entry);

      // Privacy-first:
      if (config.privacy.enableLogging) {
        console.log('Mood entry created:', { id: entry.id, mood: entry.mood });
      }

      res.status(201).json({
        success: true,
        data: {
          entry,
          message: 'Mood entry recorded successfully',
        },
      });
    } catch (error) {
      next(error);
    }
  }

  
  async getMoodHistory(req, res, next) {
    try {
      const { sessionId } = req.params;
      const { limit = 30, offset = 0 } = req.query;

      // Filter entries by sessionId
      const userEntries = moodEntries
        .filter((entry) => entry.sessionId === sessionId)
        .sort((a, b) => new Date(b.timestamp) - new Date(a.timestamp))
        .slice(parseInt(offset), parseInt(offset) + parseInt(limit));

      res.status(200).json({
        success: true,
        data: {
          entries: userEntries,
          total: moodEntries.filter((e) => e.sessionId === sessionId).length,
          limit: parseInt(limit),
          offset: parseInt(offset),
        },
      });
    } catch (error) {
      next(error);
    }
  }

  /**
   * Get mood statistics
   */
  async getMoodStats(req, res, next) {
    try {
      const { sessionId } = req.params;
      const { period = '7d' } = req.query; // 7d, 30d, 90d

      // Calculate date range
      const now = new Date();
      const periodMap = {
        '7d': 7,
        '30d': 30,
        '90d': 90,
      };
      const days = periodMap[period] || 7;
      const startDate = new Date(now.getTime() - days * 24 * 60 * 60 * 1000);

      // Filter entries
      const relevantEntries = moodEntries.filter(
        (entry) =>
          entry.sessionId === sessionId &&
          new Date(entry.timestamp) >= startDate
      );

      if (relevantEntries.length === 0) {
        return res.status(200).json({
          success: true,
          data: {
            stats: {
              average: 0,
              trend: 'neutral',
              totalEntries: 0,
              distribution: {},
            },
            message: 'No mood entries found for this period',
          },
        });
      }

      // Calculate statistics
      const moods = relevantEntries.map((e) => e.mood);
      const average = moods.reduce((sum, m) => sum + m, 0) / moods.length;

      // Calculate trend 
      const midpoint = Math.floor(moods.length / 2);
      const firstHalf = moods.slice(0, midpoint);
      const secondHalf = moods.slice(midpoint);

      const firstAvg = firstHalf.reduce((sum, m) => sum + m, 0) / firstHalf.length;
      const secondAvg = secondHalf.reduce((sum, m) => sum + m, 0) / secondHalf.length;

      let trend = 'stable';
      const difference = secondAvg - firstAvg;
      if (difference > 0.3) trend = 'improving';
      else if (difference < -0.3) trend = 'declining';

      // Mood distribution
      const distribution = {
        1: moods.filter((m) => m === 1).length,
        2: moods.filter((m) => m === 2).length,
        3: moods.filter((m) => m === 3).length,
        4: moods.filter((m) => m === 4).length,
        5: moods.filter((m) => m === 5).length,
      };

      // Common triggers and activities
      const allTriggers = relevantEntries.flatMap((e) => e.triggers || []);
      const allActivities = relevantEntries.flatMap((e) => e.activities || []);

      const triggerCounts = {};
      allTriggers.forEach((t) => {
        triggerCounts[t] = (triggerCounts[t] || 0) + 1;
      });

      const activityCounts = {};
      allActivities.forEach((a) => {
        activityCounts[a] = (activityCounts[a] || 0) + 1;
      });

      const topTriggers = Object.entries(triggerCounts)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 5)
        .map(([trigger, count]) => ({ trigger, count }));

      const topActivities = Object.entries(activityCounts)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 5)
        .map(([activity, count]) => ({ activity, count }));

      res.status(200).json({
        success: true,
        data: {
          stats: {
            period,
            average: parseFloat(average.toFixed(2)),
            trend,
            trendValue: parseFloat(difference.toFixed(2)),
            totalEntries: relevantEntries.length,
            distribution,
            topTriggers,
            topActivities,
            recentEntries: relevantEntries.slice(0, 7),
          },
        },
      });
    } catch (error) {
      next(error);
    }
  }

  /**
   * Delete a mood entry
   */
  async deleteMoodEntry(req, res, next) {
    try {
      const { entryId } = req.params;

      const index = moodEntries.findIndex((entry) => entry.id === entryId);

      if (index === -1) {
        return res.status(404).json({
          success: false,
          error: { message: 'Mood entry not found' },
        });
      }

      moodEntries.splice(index, 1);

      res.status(200).json({
        success: true,
        data: {
          message: 'Mood entry deleted successfully',
        },
      });
    } catch (error) {
      next(error);
    }
  }
}

module.exports = new MoodController();