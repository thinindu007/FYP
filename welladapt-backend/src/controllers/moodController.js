const Mood = require('../models/Mood');
const config = require('../config/config');

class MoodController {
  /**
   * Submit a new entry - Now persisted to DB
   */
  async submitMoodEntry(req, res, next) {
    try {
      const { mood, note, sessionId, activities, triggers } = req.body;

      const entry = await Mood.create({
        sessionId,
        mood,
        note: note || '',
        activities: activities || [],
        triggers: triggers || [],
        // MongoDB usually handles timestamps, but we can be explicit if your model needs it
        timestamp: new Date() 
      });

      if (config.privacy.enableLogging) {
        console.log('Mood entry persisted:', { id: entry._id, mood: entry.mood });
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

  /**
   * Get History - Now supports DB-side pagination
   */
  async getMoodHistory(req, res, next) {
    try {
      const { sessionId } = req.params;
      const { limit = 30, offset = 0 } = req.query;

      // Fetch entries and total count in parallel for better performance
      const [userEntries, total] = await Promise.all([
        Mood.find({ sessionId })
          .sort({ timestamp: -1 })
          .skip(parseInt(offset))
          .limit(parseInt(limit)),
        Mood.countDocuments({ sessionId })
      ]);

      res.status(200).json({
        success: true,
        data: {
          entries: userEntries,
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
   * Get Mood Statistics - Filtered at the Database level
   */
  async getMoodStats(req, res, next) {
    try {
      const { sessionId } = req.params;
      const { period = '7d' } = req.query;

      const now = new Date();
      const periodMap = { '7d': 7, '30d': 30, '90d': 90 };
      const days = periodMap[period] || 7;
      const startDate = new Date(now.getTime() - days * 24 * 60 * 60 * 1000);

      // Only pull entries from the DB that fall within the date range
      const relevantEntries = await Mood.find({
        sessionId,
        timestamp: { $gte: startDate }
      }).sort({ timestamp: 1 }); // Sorted oldest to newest for trend calculation

      if (relevantEntries.length === 0) {
        return res.status(200).json({
          success: true,
          data: {
            stats: { average: 0, trend: 'neutral', totalEntries: 0, distribution: {} },
            message: 'No mood entries found for this period',
          },
        });
      }

      // -- Logic for Calculations (Keep your original logic) --
      const moods = relevantEntries.map((e) => e.mood);
      const average = moods.reduce((sum, m) => sum + m, 0) / moods.length;

      const midpoint = Math.floor(moods.length / 2);
      const firstHalf = moods.slice(0, midpoint);
      const secondHalf = moods.slice(midpoint);
      const firstAvg = firstHalf.length ? firstHalf.reduce((a, b) => a + b, 0) / firstHalf.length : average;
      const secondAvg = secondHalf.length ? secondHalf.reduce((a, b) => a + b, 0) / secondHalf.length : average;

      let trend = 'stable';
      const difference = secondAvg - firstAvg;
      if (difference > 0.3) trend = 'improving';
      else if (difference < -0.3) trend = 'declining';

      const distribution = {
        1: moods.filter((m) => m === 1).length,
        2: moods.filter((m) => m === 2).length,
        3: moods.filter((m) => m === 3).length,
        4: moods.filter((m) => m === 4).length,
        5: moods.filter((m) => m === 5).length,
      };

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
            recentEntries: relevantEntries.slice(-7), // Last 7 from the set
          },
        },
      });
    } catch (error) {
      next(error);
    }
  }

  /**
   * Delete a mood entry - Now using DB ID
   */
  async deleteMoodEntry(req, res, next) {
    try {
      const { entryId } = req.params;

      const result = await Mood.findByIdAndDelete(entryId);

      if (!result) {
        return res.status(404).json({
          success: false,
          error: { message: 'Mood entry not found' },
        });
      }

      res.status(200).json({
        success: true,
        data: { message: 'Mood entry deleted successfully' },
      });
    } catch (error) {
      next(error);
    }
  }
}

module.exports = new MoodController();