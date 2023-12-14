import './App.css';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faMagicWandSparkles } from '@fortawesome/free-solid-svg-icons';
import React from 'react';
import Navbar from './Navbar';

function App() {
  return (
    <div className="flex">
      <div className="mt-10">
        <Navbar />

        <button>
           <FontAwesomeIcon icon={faMagicWandSparkles} /> New Grimoire
        </button>

    </div>
    </div>  
  );
}


export default App;
