const mongoose = require('mongoose');
const bcrypt = require('bcryptjs');

const UserSchema = new mongoose.Schema({
  email: { type: String, required: true, unique: true, lowercase: true },
  password: { type: String, required: true },
});

/**
 * Pre-save hook: Automatically hash password before saving to DB.
 * For async hooks, do not use the 'next' callback.
 */
UserSchema.pre('save', async function() {
  // Only hash the password if it has been modified (or is new)
  if (!this.isModified('password')) return;

  try {
    // Generate salt and hash
    this.password = await bcrypt.hash(this.password, 12);
    // No next() call needed; the hook completes when the function resolves
  } catch (err) {
    // Re-throwing the error allows Mongoose to catch it and 
    // pass it to the controller's catch block
    throw err;
  }
});

module.exports = mongoose.model('User', UserSchema);