import axios from 'axios';
import { ChatResponse, ApiError } from '../types/chat.types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

// Configure axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * INTERCEPTOR: Automatically attach the JWT token to every request 
 * if it exists in localStorage.
 */
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('welladapt-token');
  if (token && config.headers) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

/**
 * INTERCEPTOR: Global Error Handling
 * If the server returns 401 (Unauthorized), it means the token expired.
 */
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('welladapt-token');
      localStorage.removeItem('welladapt-session-id');
      window.location.reload(); // Force back to login
    }
    return Promise.reject(error);
  }
);

export const apiService = {
  
  // --- Authentication Methods ---

  async login(credentials: { email: string; password: string }): Promise<any> {
    try {
      const response = await api.post('/auth/login', credentials);
      if (response.data.success) {
        localStorage.setItem('welladapt-token', response.data.token);
        localStorage.setItem('welladapt-session-id', response.data.sessionId);
      }
      return response.data;
    } catch (error: any) {
      throw error.response?.data || { message: 'Login connection failed' };
    }
  },

  async register(credentials: { email: string; password: string }): Promise<any> {
    try {
      const response = await api.post('/auth/register', credentials);
      if (response.data.success) {
        localStorage.setItem('welladapt-token', response.data.token);
        localStorage.setItem('welladapt-session-id', response.data.sessionId);
      }
      return response.data;
    } catch (error: any) {
      throw error.response?.data || { message: 'Registration failed' };
    }
  },

  logout(): void {
    localStorage.removeItem('welladapt-token');
    localStorage.removeItem('welladapt-session-id');
  },

  // --- Chat & NLP Methods ---

  async checkHealth(): Promise<any> {
    return (await api.get('/health')).data;
  },

  async sendMessage(message: string, language: 'si' | 'en' | 'mixed' = 'mixed'): Promise<ChatResponse> {
    try {
      const response = await api.post<ChatResponse>('/chat/message', { message, language });
      return response.data;
    } catch (error: any) {
      throw error.response?.data || { success: false, error: { message: 'Connection lost' } };
    }
  },

  // --- Resources & Mood ---

  async getCrisisResources(): Promise<any> {
    return (await api.get('/resources/crisis')).data;
  },

  async submitMoodEntry(moodData: any): Promise<any> {
    return (await api.post('/mood/entry', moodData)).data;
  },

  async getMoodHistory(sessionId: string, limit = 30): Promise<any> {
    return (await api.get(`/mood/history/${sessionId}`, { params: { limit } })).data;
  },

  async getMoodStats(sessionId: string, period = '7d'): Promise<any> {
    return (await api.get(`/mood/stats/${sessionId}`, { params: { period } })).data;
  }
};

export default apiService;