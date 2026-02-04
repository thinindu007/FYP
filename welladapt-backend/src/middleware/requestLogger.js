const requestLogger = (req, res, next) => {
  
  const logData = {
    timestamp: new Date().toISOString(),
    method: req.method,
    path: req.path,
   
  };

  console.log('Request:', logData);
  next();
};

module.exports = requestLogger;