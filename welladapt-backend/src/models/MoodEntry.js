const mongoose = require('mongoose');

const moodEntrySchema = new mongoose.Schema(
  {
    sessionId: {
      type: String,
      required: true,
      index: true,
    },
    mood: {
      type: Number,
      required: true,
      min: 1,
      max: 5,
    },
    note: {
      type: String,
      maxlength: 500,
      default: '',
    },
    activities: {
      type: [String],
      default: [],
    },
    triggers: {
      type: [String],
      default: [],
    },
    // Metadata
    createdAt: {
      type: Date,
      default: Date.now,
      index: true,
    },
    // Privacy: Auto-delete after retention period
    expiresAt: {
      type: Date,
      index: true,
    },
  },
  {
    timestamps: true, // Automatically adds createdAt and updatedAt
    collection: 'mood_entries',
  }
);

// Index for efficient queries
moodEntrySchema.index({ sessionId: 1, createdAt: -1 });

// Virtual for mood label
moodEntrySchema.virtual('moodLabel').get(function() {
  const labels = {
    1: 'Very Bad',
    2: 'Bad',
    3: 'Okay',
    4: 'Good',
    5: 'Very Good',
  };
  return labels[this.mood];
});

// Method to check if entry is expired
moodEntrySchema.methods.isExpired = function() {
  if (!this.expiresAt) return false;
  return this.expiresAt < new Date();
};

// Static method to clean expired entries
moodEntrySchema.statics.cleanExpiredEntries = async function() {
  const result = await this.deleteMany({
    expiresAt: { $lt: new Date() },
  });
  return result.deletedCount;
};

const MoodEntry = mongoose.model('MoodEntry', moodEntrySchema);

module.exports = MoodEntry;