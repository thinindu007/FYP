const express = require('express');
const cors = require('cors');
const mongoose = require('mongoose');
const config = require('./config/config');

// Import middleware
const errorHandler = require('./middleware/errorHandler');
const privacyMiddleware = require('./middleware/privacyMiddleware');

// Import routes
const authRoutes = require('./routes/authRoutes'); // 1. Import Auth Routes

const chatRoutes = require('./routes/chatRoutes');
const healthRoutes = require('./routes/healthRoutes');
const resourceRoutes = require('./routes/resourceRoutes');
const moodRoutes = require('./routes/moodRoutes');

const app = express();

// Database Connection
mongoose.connect(config.database.uri)
  .then(() => console.log('✅ Connected to MongoDB successfully'))
  .catch((err) => console.error('❌ MongoDB connection error:', err.message));

// Standard Middleware
app.use(cors(config.cors));
app.use(express.json());

// Apply privacy headers
app.use(privacyMiddleware);

// 2. Register Auth Routes (placed before privacy check if needed)
app.use('/api/auth', authRoutes);

// Protected/Standard Routes
app.use('/api/health', healthRoutes);
app.use('/api/chat', chatRoutes);
app.use('/api/resources', resourceRoutes);
app.use('/api/mood', moodRoutes);

// Error handling
app.use(errorHandler);

module.exports = app;