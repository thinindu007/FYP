const express = require('express');
const router = express.Router();
const chatHistoryController = require('../controllers/chatHistoryController');

// Save a chat message
router.post('/save', chatHistoryController.saveMessage);

// Get chat history
router.get('/history/:sessionId', chatHistoryController.getChatHistory);

// Delete chat history
router.delete('/history/:sessionId', chatHistoryController.deleteChatHistory);

module.exports = router;