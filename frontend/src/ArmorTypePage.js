import React, { useState, useEffect } from 'react';
import axios from 'axios';

function ArmorTypePage() {
  // State variables
  const [armorItems, setArmorItems] = useState([]);

  // Effect hook to fetch armor types from the backend
  useEffect(() => {
    const fetchArmor = async () => {
      try {
        // Fetch all armor regardless of type
        const responseItems = await axios.get('/api/allArmorItems');
        setArmorItems(responseItems.data);
      } catch (error) {
        console.error('Error fetching armor types and armor:', error);
      }
    };
    fetchArmor();
  }, []);

  // Mapping of armor types to their corresponding IDs
  const armorTypeIDs = {
    Head: 50,
    Torso: 51,
    Arms: 52,
    Legs: 53
  };

  // Fetch armor of a specific type from the backend
  const handleSelectArmorType = async (armorType) => {
    const armorTypeID = armorTypeIDs[armorType];
    try {
      const response = await axios.get(`/api/armorByType/${armorTypeID}`);
      setArmorItems(response.data);
    } catch (error) {
      console.error('Error fetching armor items by type:', error);
      setArmorItems([]);
    }
  };

  // Function to handle clicking on the "reset" button
  const handleArmorButtonClick = async () => {
    try {
      const response = await axios.get('/api/allArmorItems');
      setArmorItems(response.data);
    } catch (error) {
      console.error('Error fetching all armor items:', error);
      setArmorItems([]);
    }
  };

  return (
    <div>
      <h2>Select Armor Type</h2>
      <div className="buttons">
        {/* Render buttons for Head, Torso, Arms, and Legs */}
        <button className="button" onClick={() => handleSelectArmorType('Head')}>Head</button>
        <button className="button" onClick={() => handleSelectArmorType('Torso')}>Torso</button>
	<button className="button" onClick={() => handleSelectArmorType('Arms')}>Arms</button>
        <button className="button" onClick={() => handleSelectArmorType('Legs')}>Legs</button>
      </div>
      <div>
        <h2>Armor</h2>
	<button className="button" onClick={handleArmorButtonClick}>Reset</button>
        <div className="armor-items">
          {armorItems.map((armorItem) => (
            <div key={armorItem.armorID} className="armor-item" style={{ marginTop: '60px' }}>
              <h3>{armorItem.armorName}</h3>
              <img src={`data:image/png;base64,${armorItem.filepath}`} alt={armorItem.armorName} />
              <p>Armor Type: {armorItem.armorTypeName}</p>
              <p>Physical Defense: {armorItem.physicalDefense}</p>
              <p>Blunt Defense: {armorItem.bluntDefense}</p>
              <p>Thrust Defense: {armorItem.thrustDefense}</p>
              <p>Bloodtinge Defense: {armorItem.bloodtingeDefense}</p>
              <p>Arcane Defense: {armorItem.arcaneDefense}</p>
              <p>Fire Defense: {armorItem.fireDefense}</p>
              <p>Bolt Defense: {armorItem.boltDefense}</p>
              <p>Slow Poison Resistance: {armorItem.slowPoisonResistance}</p>
              <p>Fast Poison Resistance: {armorItem.fastPoisonResistance}</p>
              <p>Frenzy Resistance: {armorItem.frenzyResistance}</p>
              <p>Beasthood Resistance: {armorItem.beasthoodResistance}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default ArmorTypePage;