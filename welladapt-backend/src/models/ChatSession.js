const mongoose = require('mongoose');

const chatMessageSchema = new mongoose.Schema({
  sender: {
    type: String,
    enum: ['user', 'bot'],
    required: true,
  },
  text: {
    type: String,
    required: true,
    maxlength: 1000,
  },
  language: {
    type: String,
    enum: ['si', 'en', 'mixed'],
    default: 'mixed',
  },
  emotion: {
    label: String,
    confidence: Number,
  },
  timestamp: {
    type: Date,
    default: Date.now,
  },
});

const chatSessionSchema = new mongoose.Schema(
  {
    sessionId: {
      type: String,
      required: true,
      unique: true,
      index: true,
    },
    messages: [chatMessageSchema],
    lastActive: {
      type: Date,
      default: Date.now,
    },
    // Privacy: Auto-delete after retention period
    expiresAt: {
      type: Date,
      index: true,
    },
  },
  {
    timestamps: true,
    collection: 'chat_sessions',
  }
);

// Update lastActive on message add
chatSessionSchema.methods.addMessage = function(messageData) {
  this.messages.push(messageData);
  this.lastActive = new Date();
  return this.save();
};

// Static method to clean expired sessions
chatSessionSchema.statics.cleanExpiredSessions = async function() {
  const result = await this.deleteMany({
    expiresAt: { $lt: new Date() },
  });
  return result.deletedCount;
};

const ChatSession = mongoose.model('ChatSession', chatSessionSchema);

module.exports = ChatSession;