const validateChatMessage = (req, res, next) => {
  const { message, language, sessionId } = req.body;

  if (!message || typeof message !== 'string') {
    return res.status(400).json({
      success: false,
      error: { message: 'Message is required and must be a string' },
    });
  }

  if (message.trim().length === 0) {
    return res.status(400).json({
      success: false,
      error: { message: 'Message cannot be empty' },
    });
  }

  if (message.length > 1000) {
    return res.status(400).json({
      success: false,
      error: { message: 'Message too long (max 1000 characters)' },
    });
  }

  // Validate language (if provided)
  if (language && !['si', 'en', 'mixed'].includes(language)) {
    return res.status(400).json({
      success: false,
      error: { message: 'Invalid language code. Use: si, en, or mixed' },
    });
  }

  next();
};

module.exports = { validateChatMessage };