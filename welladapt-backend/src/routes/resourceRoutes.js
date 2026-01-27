const express = require('express');
const router = express.Router();
const resourceController = require('../controllers/resourceController');

// Get mental health resources
router.get('/', resourceController.getResources);

// Get crisis helplines
router.get('/crisis', resourceController.getCrisisResources);

// Get academic stress resources
router.get('/academic', resourceController.getAcademicResources);

module.exports = router;