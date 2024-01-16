import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

function SavedGrimoires() {
  const [grimoires, setGrimoires] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    window.electron.send("read-markdown-files");

    const handleResponse = (data) => {
      if (data.error) {
        console.error("Error:", data.error);
        return;
      }
      setGrimoires(data);
    };

    const unsubscribe = window.electron.on(
      "markdown-files-response",
      handleResponse
    );

    return () => unsubscribe();
  }, []);

  const goToGrimoire = (title) => {
    navigate(`/grimoire/${encodeURIComponent(title)}`);
  };

  return (
    <div className="flex flex-wrap justify-center">
      {grimoires.map((grimoire, index) => (
        <div
          key={index}
          className="m-4 w-48 h-48 bg-gray-200 rounded-lg shadow-md hover:shadow-lg hover:scale-105 transition-transform cursor-pointer flex items-center justify-center"
          onClick={() => goToGrimoire(grimoire.title)}
        >
          <h2 className="text-center text-xl font-semibold">
            {grimoire.title}
          </h2>
        </div>
      ))}
    </div>
  );
}

export default SavedGrimoires;
