const express = require('express');
const cors = require('cors');
const config = require('./config/config');

// Import middleware
const errorHandler = require('./middleware/errorHandler');
const requestLogger = require('./middleware/requestLogger');
const privacyMiddleware = require('./middleware/privacyMiddleware');

// Import routes
const chatRoutes = require('./routes/chatRoutes');
const healthRoutes = require('./routes/healthRoutes');
const resourceRoutes = require('./routes/resourceRoutes');

const app = express();

// Middleware
app.use(cors(config.cors));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Privacy-first: Only log if explicitly enabled
if (config.privacy.enableLogging) {
  app.use(requestLogger);
}

// Apply privacy middleware to all routes
app.use(privacyMiddleware);

// Routes
app.use('/api/health', healthRoutes);
app.use('/api/chat', chatRoutes);
app.use('/api/resources', resourceRoutes);

// Error handling (must be last)
app.use(errorHandler);

module.exports = app;