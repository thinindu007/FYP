import React, { useState } from 'react';
import { apiService } from '../services/apiService';
import './Login.css';

interface LoginProps {
  onLogin: () => void;
}

const Login: React.FC<LoginProps> = ({ onLogin }) => {
  const [isRegistering, setIsRegistering] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    // Basic Validation
    if (password.length < 6) {
      setError('Password must be at least 6 characters');
      setLoading(false);
      return;
    }

    try {
      let response;
      if (isRegistering) {
        response = await apiService.register({ email, password });
      } else {
        response = await apiService.login({ email, password });
      }

      if (response.success) {
        onLogin(); // Signal to App.tsx that we are in!
      }
    } catch (err: any) {
      setError(err.error?.message || err.message || 'Authentication failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <div className="login-header">
          <h1 className="login-title">🌱 WellAdapt</h1>
          <p className="login-subtitle">
            {isRegistering ? 'Create your student account' : 'Welcome back, Student'}
          </p>
        </div>

        <form className="login-form" onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label">University Email</label>
            <input
              type="email"
              className="form-input"
              placeholder="e.g. name@student.lk"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label">Password</label>
            <input
              type="password"
              className="form-input"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          {error && <div className="error-message">{error}</div>}

          <button type="submit" className="login-button" disabled={loading}>
            {loading ? 'Processing...' : isRegistering ? 'Register' : 'Login'}
          </button>
        </form>

        <div className="login-footer">
          <p onClick={() => setIsRegistering(!isRegistering)} style={{ cursor: 'pointer', color: '#6366f1' }}>
            {isRegistering ? 'Already have an account? Login' : 'New student? Register here'}
          </p>
          <p className="privacy-note">Your data is encrypted and private.</p>
        </div>
      </div>
    </div>
  );
};

export default Login;