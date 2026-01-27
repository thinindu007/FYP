const express = require('express');
const router = express.Router();
const moodController = require('../controllers/moodController');
const { validateMoodEntry } = require('../middleware/validators');

// Submit a mood entry
router.post('/entry', validateMoodEntry, moodController.submitMoodEntry);

// Get mood history for a user (by sessionId)
router.get('/history/:sessionId', moodController.getMoodHistory);

// Get mood statistics
router.get('/stats/:sessionId', moodController.getMoodStats);

// Delete a mood entry
router.delete('/entry/:entryId', moodController.deleteMoodEntry);

module.exports = router;