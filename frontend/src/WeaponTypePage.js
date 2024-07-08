import React, { useState, useEffect } from 'react';
import axios from 'axios';

function WeaponTypePage() {
  const [weapons, setWeapons] = useState([]);

  useEffect(() => {
    const fetchWeapons = async () => {
      try {
 	// Fetch all weapons regardless of type form the backend
        const responseItems = await axios.get('/api/allWeaponItems');
        setWeapons(responseItems.data.map(weapon => {
        // Replace null values with 'N/A'
        return Object.fromEntries(
          Object.entries(weapon).map(([key, value]) => [key, value || 'N/A'])
        );
      }));
      } catch (error) {
        console.error('Error fetching weapon types and weapons:', error);
      }
    };

    fetchWeapons();
  }, []);

  // Mapping of weapon types to their corresponding IDs
  const weaponTypeIDs = {
    "Trick Weapon": 1,
    "Sidearm": 2
  };

  // Fetch weapons of a specific type from the backend
  const handleSelectWeaponType = async (weaponType) => {
    const weaponTypeID = weaponTypeIDs[weaponType]; // Get the corresponding ID
    try {
      const response = await axios.get(`/api/weaponsByType/${weaponTypeID}`);
      setWeapons(response.data.map(weapon => {
        // Replace null values with 'N/A'
        return Object.fromEntries(
          Object.entries(weapon).map(([key, value]) => [key, value || 'N/A'])
        );
      }));
    } catch (error) {
      console.error('Error fetching weapons by type:', error);
      setWeapons([]);
    }
  };

  // Function to handle clicking on the "reset" button
  const handleWeaponButtonClick = async () => {
    try {
      const response = await axios.get('/api/allWeaponItems');
      setWeapons(response.data.map(weapon => {
        // Replace null values with 'N/A'
        return Object.fromEntries(
          Object.entries(weapon).map(([key, value]) => [key, value || 'N/A'])
        );
      }));
    } catch (error) {
      console.error('Error fetching weapons by type:', error);
      setWeapons([]);
    }
  };

  return (
    <div>
      <h2>Select Weapon Type</h2>
      <div className="buttons">
        {/* Render buttons for Weapon Types */}
        <button className="button" onClick={() => handleSelectWeaponType('Trick Weapon')}>Trick Weapon</button>
        <button className="button" onClick={() => handleSelectWeaponType('Sidearm')}>Sidearm</button>
      </div>
      <div>
        <h2>Weapons</h2>
        <button className="button" onClick={handleWeaponButtonClick}>Reset</button>
        <div className="weapons">
          {weapons.map((weapon) => (
            <div key={weapon.weaponID} className="weapon" style={{ marginTop: '60px' }}>
              <h3>{weapon.weaponName}</h3>
              <img src={`data:image/png;base64,${weapon.filepath}`} alt={weapon.weaponName} />
              <p>Weapon Type: {weapon.weaponTypeName}</p>
              <p>Physical Attack: {weapon.physicalAttack}</p>
              <p>Blood Attack: {weapon.bloodAttack}</p>
              <p>Arcane Attack: {weapon.arcaneAttack}</p>
              <p>Fire Attack: {weapon.fireAttack}</p>
              <p>Bolt Attack: {weapon.boltAttack}</p>
              <p>Slow Poison Attack: {weapon.slowPoisonAttack}</p>
              <p>Rapid Poison Attack: {weapon.rapidPoisonAttack}</p>
              <p>Kin Damage: {weapon.kinDamage}</p>
              <p>Beast Damage: {weapon.beastDamage}</p>
              <p>Strength Requirement: {weapon.strengthRequirement}</p>
              <p>Skill Requirement: {weapon.skillRequirement}</p>
              <p>Bloodtinge Requirement: {weapon.bloodtingeRequirement}</p>
              <p>Arcane Requirement: {weapon.arcaneRequirement}</p>
              <p>Durability: {weapon.durability}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default WeaponTypePage;