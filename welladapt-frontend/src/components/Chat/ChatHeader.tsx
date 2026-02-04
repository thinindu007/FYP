import React from 'react';
import './ChatHeader.css';

interface ChatHeaderProps {
  onShowResources: () => void;
}

const ChatHeader: React.FC<ChatHeaderProps> = ({ onShowResources }) => {
  return (
    <div className="chat-header">
      <div className="header-content">
        <h1 className="app-title"> WellAdapt</h1>
        <p className="app-subtitle">Your Bilingual Mental Wellness Companion</p>
      </div>
      
      <button className="crisis-button" onClick={onShowResources}>
         Crisis Resources
      </button>
    </div>
  );
};

export default ChatHeader;