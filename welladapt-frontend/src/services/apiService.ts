import axios from 'axios';
import { ChatResponse, ApiError } from '../types/chat.types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

// Configure axios
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// API Service
export const apiService = {
  // Health check
  async checkHealth(): Promise<any> {
    try {
      const response = await api.get('/health');
      return response.data;
    } catch (error) {
      console.error('Health check failed:', error);
      throw error;
    }
  },

  // Send chat message
  async sendMessage(
    message: string,
    language: 'si' | 'en' | 'mixed' = 'mixed'
  ): Promise<ChatResponse> {
    try {
      const response = await api.post<ChatResponse>('/chat/message', {
        message,
        language,
      });
      return response.data;
    } catch (error: any) {
      console.error('Send message failed:', error);
      
      if (error.response?.data) {
        throw error.response.data;
      }
      
      throw {
        success: false,
        error: {
          message: 'Failed to send message. Please try again.',
        },
      } as ApiError;
    }
  },

  // Classify emotion
  async classifyEmotion(message: string): Promise<any> {
    try {
      const response = await api.post('/chat/classify-emotion', {
        message,
      });
      return response.data;
    } catch (error) {
      console.error('Emotion classification failed:', error);
      throw error;
    }
  },

  // Get crisis resources
  async getCrisisResources(): Promise<any> {
    try {
      const response = await api.get('/resources/crisis');
      return response.data;
    } catch (error) {
      console.error('Get crisis resources failed:', error);
      throw error;
    }
  },

  // Get academic resources
  async getAcademicResources(): Promise<any> {
    try {
      const response = await api.get('/resources/academic');
      return response.data;
    } catch (error) {
      console.error('Get academic resources failed:', error);
      throw error;
    }
  },

  // Submit mood entry
  async submitMoodEntry(moodData: {
    mood: number;
    note?: string;
    sessionId: string;
    activities?: string[];
    triggers?: string[];
  }): Promise<any> {
    try {
      const response = await api.post('/mood/entry', moodData);
      return response.data;
    } catch (error) {
      console.error('Submit mood entry failed:', error);
      throw error;
    }
  },

  // Get mood history
  async getMoodHistory(sessionId: string, limit = 30, offset = 0): Promise<any> {
    try {
      const response = await api.get(`/mood/history/${sessionId}`, {
        params: { limit, offset },
      });
      return response.data;
    } catch (error) {
      console.error('Get mood history failed:', error);
      throw error;
    }
  },

  // Get mood statistics
  async getMoodStats(sessionId: string, period: '7d' | '30d' | '90d' = '7d'): Promise<any> {
    try {
      const response = await api.get(`/mood/stats/${sessionId}`, {
        params: { period },
      });
      return response.data;
    } catch (error) {
      console.error('Get mood stats failed:', error);
      throw error;
    }
  },

  // Delete mood entry
  async deleteMoodEntry(entryId: string): Promise<any> {
    try {
      const response = await api.delete(`/mood/entry/${entryId}`);
      return response.data;
    } catch (error) {
      console.error('Delete mood entry failed:', error);
      throw error;
    }
  },
};

export default apiService;