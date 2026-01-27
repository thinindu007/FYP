// Type definitions for chat functionality
export interface ChatMessage {
  id: string;
  text: string;
  sender: 'user' | 'bot';
  timestamp: Date;
  emotion?: EmotionData;
  language?: 'si' | 'en' | 'mixed';
}

export interface EmotionData {
  label: string;
  confidence: number;
}

export interface ChatResponse {
  success: boolean;
  data: {
    response: string;
    emotion?: EmotionData;
    language: string;
    processingTime: number;
  };
}

export interface ApiError {
  success: false;
  error: {
    message: string;
  };
}

export interface MoodEntry {
  mood: number; // 1-5 scale
  note?: string;
  timestamp: Date;
}