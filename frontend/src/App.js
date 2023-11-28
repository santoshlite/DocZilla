import './App.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faMagicWandSparkles } from '@fortawesome/free-solid-svg-icons';
import React, { useState } from 'react';
import SearchBar from './Navbar';
import Navbar from './Navbar';

function App() {
  return (
    <div className="App">
        <Navbar />
        <button><FontAwesomeIcon icon={faMagicWandSparkles} /> New Grimoire</button>
    </div>
  );
}

export default App;
