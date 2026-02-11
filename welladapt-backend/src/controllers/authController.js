const User = require('../models/User');
const jwt = require('jsonwebtoken');
const bcrypt = require('bcryptjs');

const signToken = (id) => {
  return jwt.sign({ id }, process.env.JWT_SECRET || 'fallback', { expiresIn: '7d' });
};

// const register = async (req, res, next) => {
//   try {
//     const { email, password } = req.body;
    
//     // Safety check: Prevent duplicate users
//     const userExists = await User.findOne({ email });
//     if (userExists) {
//       return res.status(400).json({ success: false, message: 'User already exists' });
//     }

//     const newUser = await User.create({ email, password });
//     const token = signToken(newUser._id);

//     res.status(201).json({ success: true, token, sessionId: newUser._id });
//   } catch (err) {
//     // If we reach here, 'next' MUST be a function provided by Express
//     next(err); 
//   }
// };
const register = async (req, res, next) => {
  try {
    const { email, password } = req.body;
    
    const userExists = await User.findOne({ email });
    if (userExists) {
      return res.status(400).json({ success: false, message: 'User already exists' });
    }

    // This triggers the pre-save hook in the User Model
    const newUser = await User.create({ email, password });
    
    const token = signToken(newUser._id);

    return res.status(201).json({ 
      success: true, 
      token, 
      sessionId: newUser._id 
    });
  } catch (err) {
    console.error("Caught error in register:", err);
    // Safety check to pinpoint the issue
    if (typeof next === 'function') {
      next(err);
    } else {
      res.status(500).json({ success: false, message: "Internal Server Error - 'next' missing" });
    }
  }
};

const login = async (req, res, next) => {
  try {
    const { email, password } = req.body;
    const user = await User.findOne({ email });

    if (!user || !(await bcrypt.compare(password, user.password))) {
      return res.status(401).json({ success: false, message: 'Invalid credentials' });
    }

    const token = signToken(user._id);
    res.status(200).json({ success: true, token, sessionId: user._id });
  } catch (err) {
    next(err);
  }
};

// Exporting as an object
module.exports = { register, login };