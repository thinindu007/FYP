import React, { useState, useEffect, useRef } from 'react';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';
import ChatHeader from './ChatHeader';
import { ChatMessage as ChatMessageType } from '../../types/chat.types';
import { apiService } from '../../services/apiService';
import './ChatInterface.css';

interface ChatInterfaceProps {
  onShowResources: () => void;
}

const ChatInterface: React.FC<ChatInterfaceProps> = ({ onShowResources }) => {
  const [messages, setMessages] = useState<ChatMessageType[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Welcome message
  useEffect(() => {
    const welcomeMessage: ChatMessageType = {
      id: 'welcome-1',
      text: 'Hello! I\'m here to support you. You can talk to me in English, Sinhala, or mix both languages. How are you feeling today?',
      sender: 'bot',
      timestamp: new Date(),
    };
    
    setMessages([welcomeMessage]);
  }, []);

  const handleSendMessage = async (
    text: string,
    language: 'si' | 'en' | 'mixed'
  ) => {
    // Add user message
    const userMessage: ChatMessageType = {
      id: `user-${Date.now()}`,
      text,
      sender: 'user',
      timestamp: new Date(),
      language,
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);
    setError(null);

    try {
      // Call backend API
      const response = await apiService.sendMessage(text, language);

      // Add bot response
      const botMessage: ChatMessageType = {
        id: `bot-${Date.now()}`,
        text: response.data.response,
        sender: 'bot',
        timestamp: new Date(),
        emotion: response.data.emotion,
        language: response.data.language as any,
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (err: any) {
      setError(err.error?.message || 'Failed to get response');
      
      // Add error message
      const errorMessage: ChatMessageType = {
        id: `error-${Date.now()}`,
        text: 'Sorry, I encountered an error. Please try again.',
        sender: 'bot',
        timestamp: new Date(),
      };
      
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chat-interface">
      <ChatHeader onShowResources={onShowResources} />
      
      <div className="messages-container">
        {messages.map((message) => (
          <ChatMessage key={message.id} message={message} />
        ))}
        
        {isLoading && (
          <div className="typing-indicator">
            <span></span>
            <span></span>
            <span></span>
          </div>
        )}
        
        {error && (
          <div className="error-message">
             {error}
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>
      
      <ChatInput onSendMessage={handleSendMessage} isLoading={isLoading} />
    </div>
  );
};

export default ChatInterface;