const privacyMiddleware = (req, res, next) => {
  // Add privacy headers
  res.setHeader('X-Privacy-Mode', 'on-device-first');
  res.setHeader('X-Data-Retention', 'zero-default');
  
  // Remove identifying headers
  res.removeHeader('X-Powered-By');
  
  req.startTime = Date.now();
  
  // Intercept response to add response time header
  const originalSend = res.send;
  res.send = function(data) {
    const responseTime = Date.now() - req.startTime;
    res.setHeader('X-Response-Time', `${responseTime}ms`);
    originalSend.call(this, data);
  };
  
  next();
};

module.exports = privacyMiddleware;