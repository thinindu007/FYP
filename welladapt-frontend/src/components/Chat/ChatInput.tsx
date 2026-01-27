import React, { useState, KeyboardEvent } from 'react';
import './ChatInput.css';

interface ChatInputProps {
  onSendMessage: (message: string, language: 'si' | 'en' | 'mixed') => void;
  isLoading: boolean;
}

const ChatInput: React.FC<ChatInputProps> = ({ onSendMessage, isLoading }) => {
  const [message, setMessage] = useState('');
  const [language, setLanguage] = useState<'si' | 'en' | 'mixed'>('mixed');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (message.trim() && !isLoading) {
      onSendMessage(message.trim(), language);
      setMessage('');
    }
  };

  const handleKeyPress = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e as any);
    }
  };

  return (
    <form className="chat-input-container" onSubmit={handleSubmit}>
      <div className="language-selector">
        <button
          type="button"
          className={`lang-btn ${language === 'en' ? 'active' : ''}`}
          onClick={() => setLanguage('en')}
        >
          English
        </button>
        <button
          type="button"
          className={`lang-btn ${language === 'si' ? 'active' : ''}`}
          onClick={() => setLanguage('si')}
        >
          සිංහල
        </button>
        <button
          type="button"
          className={`lang-btn ${language === 'mixed' ? 'active' : ''}`}
          onClick={() => setLanguage('mixed')}
        >
          Mixed
        </button>
      </div>
      
      <div className="input-area">
        <textarea
          className="message-input"
          placeholder="Type your message... (Press Enter to send, Shift+Enter for new line)"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyPress={handleKeyPress}
          disabled={isLoading}
          rows={1}
        />
        
        <button
          type="submit"
          className="send-button"
          disabled={!message.trim() || isLoading}
        >
          {isLoading ? '⏳' : '➤'}
        </button>
      </div>
    </form>
  );
};

export default ChatInput;