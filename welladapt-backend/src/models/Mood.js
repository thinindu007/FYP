const mongoose = require('mongoose');

const MoodSchema = new mongoose.Schema({
  sessionId: { type: String, required: true, index: true },
  mood: { type: Number, required: true, min: 1, max: 5 },
  note: { type: String, maxlength: 500 },
  activities: [String],
  triggers: [String],
  detectedEmotion: { type: String }, // Linked from chat analysis
  timestamp: { type: Date, default: Date.now }
});

module.exports = mongoose.model('Mood', MoodSchema);