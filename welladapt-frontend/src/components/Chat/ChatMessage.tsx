import React from 'react';
import { ChatMessage as ChatMessageType } from '../../types/chat.types';
import './ChatMessage.css';

interface ChatMessageProps {
  message: ChatMessageType;
}

const ChatMessage: React.FC<ChatMessageProps> = ({ message }) => {
  const isUser = message.sender === 'user';
  
  return (
    <div className={`chat-message ${isUser ? 'user-message' : 'bot-message'}`}>
      <div className="message-content">
        <div className="message-text">{message.text}</div>
        
        {message.emotion && !isUser && (
          <div className="emotion-indicator">
            <span className="emotion-label">
              Detected: {message.emotion.label}
            </span>
            <span className="emotion-confidence">
              ({(message.emotion.confidence * 100).toFixed(0)}%)
            </span>
          </div>
        )}
        
        <div className="message-timestamp">
          {message.timestamp.toLocaleTimeString([], { 
            hour: '2-digit', 
            minute: '2-digit' 
          })}
        </div>
      </div>
    </div>
  );
};

export default ChatMessage;