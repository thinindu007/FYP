const express = require('express');
const router = express.Router();

// System health check
router.get('/', (req, res) => {
  res.status(200).json({
    success: true,
    status: 'healthy',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
    service: 'WellAdapt Backend',
  });
});

// Model health check (for future ML integration)
router.get('/model', (req, res) => {
  // TODO: Check if ML model endpoint is accessible
  res.status(200).json({
    success: true,
    modelStatus: 'not_implemented',
    message: 'Model health check will be implemented with ML integration',
  });
});

module.exports = router;