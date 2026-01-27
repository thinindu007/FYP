const config = require('../config/config');
const { ChatSession } = require('../models');

class ChatHistoryController {
  /**
   * Save a chat message
   */
  async saveMessage(req, res, next) {
    try {
      const { sessionId, sender, text, language, emotion } = req.body;

      // Calculate expiration date
      let expiresAt = null;
      if (config.privacy.dataRetentionDays > 0) {
        expiresAt = new Date();
        expiresAt.setDate(expiresAt.getDate() + config.privacy.dataRetentionDays);
      }

      // Find or create session
      let session = await ChatSession.findOne({ sessionId });

      if (!session) {
        session = new ChatSession({
          sessionId,
          messages: [],
          expiresAt,
        });
      }

      // Add message
      await session.addMessage({
        sender,
        text,
        language,
        emotion,
      });

      res.status(201).json({
        success: true,
        data: {
          message: 'Chat message saved',
        },
      });
    } catch (error) {
      next(error);
    }
  }

  /**
   * Get chat history
   */
  async getChatHistory(req, res, next) {
    try {
      const { sessionId } = req.params;
      const { limit = 50 } = req.query;

      const session = await ChatSession.findOne({ sessionId })
        .select('messages')
        .lean();

      if (!session) {
        return res.status(200).json({
          success: true,
          data: {
            messages: [],
            total: 0,
          },
        });
      }

      // Get last N messages
      const messages = session.messages.slice(-parseInt(limit));

      res.status(200).json({
        success: true,
        data: {
          messages,
          total: session.messages.length,
        },
      });
    } catch (error) {
      next(error);
    }
  }

  /**
   * Delete chat history
   */
  async deleteChatHistory(req, res, next) {
    try {
      const { sessionId } = req.params;

      await ChatSession.deleteOne({ sessionId });

      res.status(200).json({
        success: true,
        data: {
          message: 'Chat history deleted successfully',
        },
      });
    } catch (error) {
      next(error);
    }
  }
}

module.exports = new ChatHistoryController();