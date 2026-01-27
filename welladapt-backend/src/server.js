const app = require('./app');
const config = require('./config/config');
const connectDB = require('./config/database');

const PORT = config.server.port;

// Connect to MongoDB first
connectDB().then(() => {
  // Start server after DB connection
  const server = app.listen(PORT, () => {
    console.log(`🚀 WellAdapt Backend running on port ${PORT}`);
    console.log(`📊 Environment: ${config.server.env}`);
    console.log(`🔒 Privacy-first mode: ${config.privacy.enableLogging ? 'Logging enabled' : 'Zero logging'}`);
    console.log(`⏱️  Max response time: ${config.model.maxResponseTime}ms`);
  });

  // Graceful shutdown
  process.on('SIGTERM', () => {
    console.log('SIGTERM signal received: closing HTTP server');
    server.close(() => {
      console.log('HTTP server closed');
    });
  });

  process.on('SIGINT', () => {
    console.log('SIGINT signal received: closing HTTP server');
    server.close(() => {
      console.log('HTTP server closed');
    });
  });
}).catch((error) => {
  console.error('Failed to connect to database:', error);
  process.exit(1);
});