const jwt = require('jsonwebtoken');

const protect = (req, res, next) => {
  let token;

  // Check if token exists in headers
  if (req.headers.authorization && req.headers.authorization.startsWith('Bearer')) {
    token = req.headers.authorization.split(' ')[1];
  }

  if (!token) {
    return res.status(401).json({ success: false, message: 'Not authorized, no token' });
  }

  try {
    // Verify token
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = decoded; // Attach user ID to the request
    next();
  } catch (error) {
    return res.status(401).json({ success: false, message: 'Token is invalid' });
  }
};

module.exports = protect;