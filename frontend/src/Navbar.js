import React from 'react';
import { InputGroup } from "@blueprintjs/core";

function  Navbar() {
    return (
        <div className="h-screen w-screen p-5 flex justify-center">
            <div className="flex justify-center w-3/5">
                <InputGroup
                placeholder="Search an Object..."
                fill={true}
                round={false}
                leftIcon="search"
                type="search" 
                className="!z-5"/>
            </div>
        </div>
    );
}

export default Navbar;
