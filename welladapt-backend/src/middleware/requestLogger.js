const requestLogger = (req, res, next) => {
  // Only log non-sensitive metadata
  const logData = {
    timestamp: new Date().toISOString(),
    method: req.method,
    path: req.path,
    // DO NOT LOG: req.body (may contain sensitive conversation data)
  };

  console.log('Request:', logData);
  next();
};

module.exports = requestLogger;