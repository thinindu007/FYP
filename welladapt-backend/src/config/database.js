const mongoose = require('mongoose');
const config = require('./config');

const connectDB = async () => {
  try {
    const options = {
      dbName: config.database.name,
      // Use new URL parser
      useNewUrlParser: true,
      useUnifiedTopology: true,
      // Auto-create indexes
      autoIndex: true,
      // Set timeout
      serverSelectionTimeoutMS: 5000,
    };

    await mongoose.connect(config.database.uri, options);

    console.log('✅ MongoDB Connected Successfully');
    console.log(`📊 Database: ${mongoose.connection.name}`);
    console.log(`🔗 Host: ${mongoose.connection.host}`);

    // Handle connection events
    mongoose.connection.on('error', (err) => {
      console.error('❌ MongoDB connection error:', err);
    });

    mongoose.connection.on('disconnected', () => {
      console.warn('⚠️  MongoDB disconnected');
    });

    // Graceful shutdown
    process.on('SIGINT', async () => {
      await mongoose.connection.close();
      console.log('MongoDB connection closed through app termination');
      process.exit(0);
    });

  } catch (error) {
    console.error('❌ MongoDB connection failed:', error.message);
    process.exit(1);
  }
};

module.exports = connectDB;