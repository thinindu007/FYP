const axios = require('axios');
const config = require('../config/config');

class MLService {
  constructor() {
    this.baseURL = config.model.endpoint || 'http://localhost:8000';
    this.timeout = config.model.maxResponseTime || 5000;
    
    // Create axios instance for ML server
    this.client = axios.create({
      baseURL: this.baseURL,
      timeout: this.timeout,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }

  /**
   * Check if ML server is healthy and ready
   */
  async checkHealth() {
    try {
      const response = await this.client.get('/ml/health');
      return response.data;
    } catch (error) {
      console.error('ML Server health check failed:', error.message);
      return { status: 'offline', error: error.message };
    }
  }

  /**
   * Detect emotion from text using Python ML server
   * 
   * @param {string} text - The text to analyze
   * @param {string} language - Language code: 'en', 'si', or 'mixed'
   * @returns {Promise<Object>} Emotion detection result
   */
  async detectEmotion(text, language = 'mixed') {
    try {
      console.log(`🤖 Calling ML server for emotion detection...`);
      
      const response = await this.client.post('/ml/detect-emotion', {
        text,
        language,
      });

      console.log(`✅ ML server response in ${response.data.processing_time_ms}ms`);
      
      return {
        success: true,
        emotion: response.data.data.emotion,
        confidence: response.data.data.confidence,
        allEmotions: response.data.data.all_emotions,
        mixedFeeling: response.data.data.mixed_feeling,
        emojiEmotion: response.data.data.emoji_emotion,
        explanation: response.data.data.explanation,
        processingTime: response.data.processing_time_ms,
      };
    } catch (error) {
      console.error('ML Server emotion detection failed:', error.message);
      
      // Fallback to simple keyword-based detection
      return this.fallbackEmotionDetection(text);
    }
  }

  /**
   * Generate empathetic response based on detected emotion
   * 
   * @param {string} text - User's message
   * @param {string} language - Language preference
   * @returns {Promise<Object>} Generated response
   */
  async generateResponse(text, language = 'mixed') {
    try {
      // Step 1: Detect emotion
      const emotionResult = await this.detectEmotion(text, language);
      
      // Step 2: Generate appropriate response based on emotion
      const response = this.selectResponse(
        emotionResult.emotion,
        emotionResult.mixedFeeling,
        language
      );

      return {
        success: true,
        response,
        emotion: {
          label: emotionResult.emotion,
          confidence: emotionResult.confidence,
          mixedFeeling: emotionResult.mixedFeeling,
        },
        language,
        processingTime: emotionResult.processingTime,
      };
    } catch (error) {
      console.error('Response generation failed:', error.message);
      return this.fallbackResponse(language);
    }
  }

  /**
   * Select appropriate empathetic response based on emotion
   */
  selectResponse(emotion, mixedFeeling, language) {
    // Response templates for each emotion
    const responses = {
      stress: {
        en: "I understand you're feeling stressed. Many students experience this, especially during exam periods. Let's talk about what's causing this stress.",
        si: "මට තේරෙනවා ඔබ stress එකක් දැනෙනවා කියලා. බොහෝ students ලට මේ අත්දැකීම තියෙනවා, විශේෂයෙන්ම exam කාලේ. අපි කතා කරමු මේ stress එකට හේතුව ගැන.",
        mixed: "මට understand වෙනවා ඔබට stress එකක් දැනෙනවා කියලා. Let's talk about what's causing this stress එක.",
      },
      anxiety: {
        en: "It sounds like you're feeling anxious. That's a natural response, and you're not alone. Would you like to talk about what's worrying you?",
        si: "ඔබට anxiety එකක් දැනෙනවා වගේ. ඒක natural response එකක්, ඔබ එකා නෙමෙයි. ඔබට කනස්සල්ලට පත් කරන දේ ගැන කතා කරන්න කැමති ද?",
        mixed: "It sounds like ඔබට anxious feel වෙනවා. That's natural, and you're not alone. කතා කරමු ද what's worrying you?",
      },
      sadness: {
        en: "I hear that you're feeling down. It takes courage to share how you're feeling. I'm here to listen and support you.",
        si: "මට ඇහෙනවා ඔබට sad feel එකක් තියෙනවා කියලා. ඔබේ feelings share කරන්න courage එක අවශ්‍යයි. මම මෙහෙ ඉන්නේ listen කරන්න සහ support කරන්න.",
        mixed: "I hear that ඔබට down feel වෙනවා. It takes courage to share කියලා. I'm here to listen සහ support කරන්න.",
      },
      neutral: {
        en: "Thanks for sharing. How can I help you today?",
        si: "share කිරීමට ස්තූතියි. අද මම ඔබට කොහොමද උදව් කරන්න පුළුවන්?",
        mixed: "Thanks for sharing කිරීමට. අද I can help you කොහොමද?",
      },
      happiness: {
        en: "I'm glad to hear you're feeling positive! What's making you feel good today?",
        si: "ඔබට positive feel එකක් තියෙනවා කියලා ඇහුණාට සතුටුයි! අද ඔබට හොඳ feel එකක් දෙන්නේ මොකද්ද?",
        mixed: "I'm glad ඔබට positive feel වෙනවා! අද what's making you feel good?",
      },
    };

    // Handle mixed feelings
    if (mixedFeeling) {
      const mixedResponses = {
        en: "I notice you might be experiencing mixed feelings. That's completely okay - emotions can be complex. Let's explore what you're going through.",
        si: "මට පේනවා ඔබට mixed feelings තියෙන්න පුළුවන් කියලා. ඒක completely okay - emotions complex වෙන්න පුළුවන්. අපි explore කරමු ඔබ experience කරන දේ.",
        mixed: "I notice ඔබට mixed feelings තියෙන්න පුළුවන්. That's completely okay - emotions complex වෙන්න පුළුවන්. Let's explore කරමු.",
      };
      return mixedResponses[language] || mixedResponses.mixed;
    }

    // Get response for detected emotion
    const emotionResponses = responses[emotion] || responses.neutral;
    return emotionResponses[language] || emotionResponses.mixed;
  }

  /**
   * Fallback emotion detection (simple keyword-based)
   * Used when ML server is unavailable
   */
  fallbackEmotionDetection(text) {
    const lowerText = text.toLowerCase();
    
    // Simple keyword matching
    const keywords = {
      stress: ['stress', 'stressed', 'pressure', 'exam', 'test', 'පරීක්ෂණ'],
      anxiety: ['anxious', 'anxiety', 'worry', 'worried', 'nervous', 'කනස්සල්ල'],
      sadness: ['sad', 'depressed', 'lonely', 'down', 'unhappy', 'දුක'],
      happiness: ['happy', 'great', 'good', 'excellent', 'wonderful', 'සතුටු'],
    };

    for (const [emotion, words] of Object.entries(keywords)) {
      for (const word of words) {
        if (lowerText.includes(word)) {
          return {
            success: true,
            emotion,
            confidence: 0.6,
            allEmotions: {},
            mixedFeeling: false,
            emojiEmotion: null,
            explanation: 'Fallback detection (ML server unavailable)',
            processingTime: 0,
          };
        }
      }
    }

    return {
      success: true,
      emotion: 'neutral',
      confidence: 0.5,
      allEmotions: {},
      mixedFeeling: false,
      emojiEmotion: null,
      explanation: 'Fallback detection (ML server unavailable)',
      processingTime: 0,
    };
  }

  /**
   * Fallback response when ML server is unavailable
   */
  fallbackResponse(language) {
    const responses = {
      en: "I understand. Please tell me more about what's on your mind.",
      si: "මට තේරෙනවා. කරුණාකර ඔබේ mind එකේ තියෙන දේ ගැන තවත් කියන්න.",
      mixed: "මට understand වෙනවා. Please tell me more about what's on your mind.",
    };

    return {
      success: true,
      response: responses[language] || responses.mixed,
      emotion: { label: 'neutral', confidence: 0.5, mixedFeeling: false },
      language,
      processingTime: 0,
    };
  }
}

module.exports = new MLService();