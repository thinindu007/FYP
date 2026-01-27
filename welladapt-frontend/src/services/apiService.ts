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
      
      // Return error in expected format
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
};

export default apiService;