import React, { useState, useEffect } from 'react';
import { apiService } from '../../services/apiService';
import './CrisisResources.css';

interface CrisisResourcesProps {
  onClose: () => void;
}

const CrisisResources: React.FC<CrisisResourcesProps> = ({ onClose }) => {
  const [resources, setResources] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadResources();
  }, []);

  const loadResources = async () => {
    try {
      const data = await apiService.getCrisisResources();
      setResources(data.data);
    } catch (error) {
      console.error('Failed to load resources:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="crisis-modal">
        <div className="crisis-content">
          <p>Loading resources...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="crisis-modal" onClick={onClose}>
      <div className="crisis-content" onClick={(e) => e.stopPropagation()}>
        <div className="crisis-header">
          <h2> Crisis Resources</h2>
          <button className="close-button" onClick={onClose}>✕</button>
        </div>
        
        {resources?.urgent && (
          <div className="urgent-message">
             {resources.urgent.message}
          </div>
        )}
        
        <div className="helplines">
          <h3>24/7 Helplines</h3>
          {resources?.helplines?.map((helpline: any, index: number) => (
            <div key={index} className="helpline-card">
              <h4>{helpline.name}</h4>
              <p className="phone-number">📞 {helpline.number}</p>
              <p className="availability">{helpline.available}</p>
              <p className="languages">
                Languages: {helpline.language.join(', ')}
              </p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default CrisisResources;