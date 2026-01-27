const config = require('../config/config');
const { MoodEntry } = require('../models');

class MoodController {
  /**
   * Submit a new mood entry
   */
  async submitMoodEntry(req, res, next) {
    try {
      const { mood, note, sessionId, activities, triggers } = req.body;

      // Calculate expiration date if retention policy is set
      let expiresAt = null;
      if (config.privacy.dataRetentionDays > 0) {
        expiresAt = new Date();
        expiresAt.setDate(expiresAt.getDate() + config.privacy.dataRetentionDays);
      }

      // Create mood entry
      const entry = new MoodEntry({
        sessionId,
        mood,
        note: note || '',
        activities: activities || [],
        triggers: triggers || [],
        expiresAt,
      });

      await entry.save();

      // Privacy-first: Don't log sensitive mood data
      if (config.privacy.enableLogging) {
        console.log('Mood entry created:', { id: entry._id, mood: entry.mood });
      }

      res.status(201).json({
        success: true,
        data: {
          entry: {
            id: entry._id,
            sessionId: entry.sessionId,
            mood: entry.mood,
            note: entry.note,
            activities: entry.activities,
            triggers: entry.triggers,
            timestamp: entry.createdAt,
          },
          message: 'Mood entry recorded successfully',
        },
      });
    } catch (error) {
      next(error);
    }
  }

  /**
   * Get mood history for a session
   */
  async getMoodHistory(req, res, next) {
    try {
      const { sessionId } = req.params;
      const { limit = 30, offset = 0 } = req.query;

      // Find entries, sorted by most recent first
      const entries = await MoodEntry.find({ sessionId })
        .sort({ createdAt: -1 })
        .skip(parseInt(offset))
        .limit(parseInt(limit))
        .select('-__v')
        .lean();

      // Get total count
      const total = await MoodEntry.countDocuments({ sessionId });

      res.status(200).json({
        success: true,
        data: {
          entries: entries.map((entry) => ({
            id: entry._id,
            sessionId: entry.sessionId,
            mood: entry.mood,
            note: entry.note,
            activities: entry.activities,
            triggers: entry.triggers,
            timestamp: entry.createdAt,
          })),
          total,
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
      const { period = '7d' } = req.query;

      // Calculate date range
      const now = new Date();
      const periodMap = {
        '7d': 7,
        '30d': 30,
        '90d': 90,
      };
      const days = periodMap[period] || 7;
      const startDate = new Date(now.getTime() - days * 24 * 60 * 60 * 1000);

      // Find relevant entries
      const entries = await MoodEntry.find({
        sessionId,
        createdAt: { $gte: startDate },
      })
        .sort({ createdAt: 1 })
        .lean();

      if (entries.length === 0) {
        return res.status(200).json({
          success: true,
          data: {
            stats: {
              average: 0,
              trend: 'neutral',
              totalEntries: 0,
              distribution: { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0 },
            },
            message: 'No mood entries found for this period',
          },
        });
      }

      // Calculate statistics
      const moods = entries.map((e) => e.mood);
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

      // Common triggers and activities using aggregation
      const triggerCounts = {};
      const activityCounts = {};

      entries.forEach((entry) => {
        entry.triggers?.forEach((trigger) => {
          triggerCounts[trigger] = (triggerCounts[trigger] || 0) + 1;
        });
        entry.activities?.forEach((activity) => {
          activityCounts[activity] = (activityCounts[activity] || 0) + 1;
        });
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
            totalEntries: entries.length,
            distribution,
            topTriggers,
            topActivities,
            recentEntries: entries
              .slice(-7)
              .reverse()
              .map((entry) => ({
                id: entry._id,
                sessionId: entry.sessionId,
                mood: entry.mood,
                note: entry.note,
                activities: entry.activities,
                triggers: entry.triggers,
                timestamp: entry.createdAt,
              })),
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

      const result = await MoodEntry.findByIdAndDelete(entryId);

      if (!result) {
        return res.status(404).json({
          success: false,
          error: { message: 'Mood entry not found' },
        });
      }

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

  /**
   * Clean expired entries (can be called by cron job)
   */
  async cleanExpiredEntries(req, res, next) {
    try {
      const deletedCount = await MoodEntry.cleanExpiredEntries();

      res.status(200).json({
        success: true,
        data: {
          message: `Cleaned ${deletedCount} expired entries`,
          deletedCount,
        },
      });
    } catch (error) {
      next(error);
    }
  }
}

module.exports = new MoodController();