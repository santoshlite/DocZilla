import React, { useState } from "react";
import Navbar from "./components/Navbar";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

// Import your page components
import SavedGrimoires from "./components/SavedGrimoires";
import NewGrimoire from "./components/NewGrimoire";

function App() {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  const toggleSidebar = () => {
    setIsSidebarOpen(!isSidebarOpen);
  };

  return (
    <Router>
      <div className="flex h-screen bg-slate-200">
        <Navbar isSidebarOpen={isSidebarOpen} toggleSidebar={toggleSidebar} />
        <div className="flex-1 p-4">
          <Routes>
            <Route path="/saved-grimoires" element={<SavedGrimoires />} />
            <Route path="/new-grimoire" element={<NewGrimoire />} />
            {/* Add more routes as needed */}
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
