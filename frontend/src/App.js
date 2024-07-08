import React, { useState } from 'react';
import ArmorTypePage from './ArmorTypePage';
import CaryllRunesPage from './CaryllRunesPage';
import HunterToolsPage from './HunterToolsPage';
import WeaponTypePage from './WeaponTypePage';
import './App.css';

function App() {
  // State to keep track of the active page
  const [activePage, setActivePage] = useState(null);

  // Function to reset the page to its default state
  const resetPage = () => {
    setActivePage(null); // Reset activePage state to null
  };

  return (
    <div className="App">
      <header className="App-header" onClick={resetPage}>
        <h1>Bloodborne Wiki</h1>
      </header>
      <div className="content">
        <div className="links">
          {/* Use anchor tags for navigation */}
          <a href="#armor" onClick={() => setActivePage('armor')}>Armor</a>
          <a href="#caryll-runes" onClick={() => setActivePage('caryllRunes')}>Caryll Runes</a>
          <a href="#hunter-tools" onClick={() => setActivePage('hunterTools')}>Hunter Tools</a>
          <a href="#weapons" onClick={() => setActivePage('weapons')}>Weapons</a>
        </div>
        {/* Conditionally render the active page */}
        {activePage === 'armor' && <ArmorTypePage />}
        {activePage === 'caryllRunes' && <CaryllRunesPage />}
        {activePage === 'hunterTools' && <HunterToolsPage />}
        {activePage === 'weapons' && <WeaponTypePage />}
      </div>
    </div>
  );
}

export default App;