import React, { useState } from 'react';

function  Navbar() {
    const [searchTerm, setSearchTerm] = useState('');
    return (
        <div>
            <h3>Grimoire</h3>
            <input
                type="text"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
            />
        </div>
    );
}

export default Navbar;
