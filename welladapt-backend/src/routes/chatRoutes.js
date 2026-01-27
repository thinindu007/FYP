const express = require('express');
const router = express.Router();
const chatController = require('../controllers/chatController');
const { validateChatMessage } = require('../middleware/validators');

// Main chat endpoint
router.post('/message', validateChatMessage, chatController.processMessage);

// Emotion classification (on-device backup)
router.post('/classify-emotion', chatController.classifyEmotion);

// Get suggested responses (for hybrid inference)
router.post('/suggestions', chatController.getSuggestions);

module.exports = router;