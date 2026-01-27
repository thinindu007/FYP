require('dotenv').config();

module.exports = {
  server: {
    port: process.env.PORT || 5000,
    env: process.env.NODE_ENV || 'development',
  },
  cors: {
    origin: process.env.FRONTEND_URL || 'http://localhost:3000',
    credentials: true,
  },
  privacy: {
    enableLogging: process.env.ENABLE_LOGGING === 'true',
    dataRetentionDays: parseInt(process.env.DATA_RETENTION_DAYS) || 0,
  },
  model: {
    endpoint: process.env.MODEL_ENDPOINT,
    emotionThreshold: parseFloat(process.env.EMOTION_THRESHOLD) || 0.75,
    maxResponseTime: parseInt(process.env.MAX_RESPONSE_TIME) || 3000,
  },
  //database configuration 
  database: {
    uri: process.env.MONGODB_URI || 'mongodb://localhost:27017/welladapt',
    name: process.env.DB_NAME || 'welladapt',
  },
};