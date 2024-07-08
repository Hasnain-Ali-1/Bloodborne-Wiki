import React, { useState, useEffect } from 'react';
import axios from 'axios';

function CaryllRunesPage() {
  const [caryllRunes, setCaryllRunes] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('/api/caryllRunes');
        // Convert filepath to Data URL
        const runesWithBase64 = response.data.map(rune => ({
          ...rune,
          filepath: `data:image/png;base64,${rune.filepath}`
        }));
        setCaryllRunes(runesWithBase64);
      } catch (error) {
        console.error('Error fetching Caryll Runes:', error);
      }
    };

    fetchData();
  }, []);

  return (
    <div>
      <h2>Caryll Runes</h2>
      <div className="caryll-runes-container">
        {caryllRunes.map((rune) => (
          <div key={rune.runeID} className="caryll-rune-item" style={{ marginTop: '60px' }}>
            <h3>{rune.runeName}</h3>
            {/* Use Data URL as the source for the image */}
            <img src={rune.filepath} alt={rune.runeName} />
            <p>{rune.runeEffect}</p>
            <p>Rune Type: {rune.runeTypeName}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default CaryllRunesPage;