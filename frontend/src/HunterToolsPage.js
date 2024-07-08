import React, { useState, useEffect } from 'react';
import axios from 'axios';

function HunterToolsPage() {
  const [hunterTools, setHunterTools] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('/api/hunterTools');
        // Replace null values with dashes and convert filepath to Data URL
        const toolsWithBase64 = response.data.map(tool => {
          const updatedTool = { ...tool, filepath: `data:image/png;base64,${tool.filepath}` };
          return Object.fromEntries(
            Object.entries(updatedTool).map(([key, value]) => [key, value || 'N/A'])
          );
        });
        setHunterTools(toolsWithBase64);
      } catch (error) {
        console.error('Error fetching Hunter Tools:', error);
      }
    };

    fetchData();
  }, []);

  return (
    <div>
      <h2>Hunter Tools</h2>
      <div className="hunter-tools-container">
        {hunterTools.map((tool) => (
          <div key={tool.toolID} className="hunter-tool-item" style={{ marginTop: '60px' }}>
            <h3>{tool.toolName}</h3>
            <img src={tool.filepath} alt={tool.toolName} />
            <p>{tool.toolDescription}</p>
            <p>Bullet Use: {tool.bulletUse}</p>
            <p>Arcane Requirement: {tool.arcaneRequirements}</p>
            <p>Arcane Scaling: {tool.arcaneScaling}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default HunterToolsPage;