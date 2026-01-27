const config = require('../config/config');

const errorHandler = (err, req, res, next) => {
  const statusCode = err.statusCode || 500;
  
  // Privacy-first: Don't expose detailed errors in production
  const message = config.server.env === 'development' 
    ? err.message 
    : 'An error occurred';
  
  // Never log sensitive information
  if (config.privacy.enableLogging && config.server.env === 'development') {
    console.error('Error:', {
      status: statusCode,
      message: err.message,
      stack: err.stack,
    });
  }

  res.status(statusCode).json({
    success: false,
    error: {
      message,
      ...(config.server.env === 'development' && { stack: err.stack }),
    },
  });
};

module.exports = errorHandler;