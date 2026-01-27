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

const validateMoodEntry = (req, res, next) => {
  const { mood, note, sessionId } = req.body;

  // Validate mood score (1-5)
  if (!mood || typeof mood !== 'number') {
    return res.status(400).json({
      success: false,
      error: { message: 'Mood is required and must be a number' },
    });
  }

  if (mood < 1 || mood > 5) {
    return res.status(400).json({
      success: false,
      error: { message: 'Mood must be between 1 and 5' },
    });
  }

  // Validate note (optional)
  if (note && typeof note !== 'string') {
    return res.status(400).json({
      success: false,
      error: { message: 'Note must be a string' },
    });
  }

  if (note && note.length > 500) {
    return res.status(400).json({
      success: false,
      error: { message: 'Note too long (max 500 characters)' },
    });
  }

  // Validate sessionId
  if (!sessionId || typeof sessionId !== 'string') {
    return res.status(400).json({
      success: false,
      error: { message: 'Session ID is required' },
    });
  }

  next();
};

module.exports = { validateChatMessage, validateMoodEntry };