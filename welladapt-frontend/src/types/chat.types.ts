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
// Existing types...
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

// NEW: Mood tracking types
export interface MoodEntry {
  id: string;
  sessionId: string;
  mood: number; // 1-5 scale
  note?: string;
  activities?: string[];
  triggers?: string[];
  timestamp: Date;
}

export interface MoodStats {
  period: '7d' | '30d' | '90d';
  average: number;
  trend: 'improving' | 'stable' | 'declining';
  trendValue: number;
  totalEntries: number;
  distribution: {
    1: number;
    2: number;
    3: number;
    4: number;
    5: number;
  };
  topTriggers?: { trigger: string; count: number }[];
  topActivities?: { activity: string; count: number }[];
  recentEntries: MoodEntry[];
}