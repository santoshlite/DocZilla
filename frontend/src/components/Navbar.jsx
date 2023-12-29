import React from "react";
import { NavLink } from "react-router-dom";
import {
  HiOutlineBookOpen,
  HiOutlinePlus,
  HiOutlineMenu,
} from "react-icons/hi";

function Navbar({ isSidebarOpen, toggleSidebar }) {
  const sidebarWidth = isSidebarOpen ? "w-64" : "w-20";
  const linkStyle =
    "flex items-center space-x-2 cursor-pointer p-2 rounded-md justify-center";
  const activeLinkStyle = "bg-gray-700";

  return (
    <div
      className={`bg-gray-800 text-white ${sidebarWidth} transition-width duration-300 ease-in-out flex flex-col items-center rounded-r-lg`}
    >
      <button onClick={toggleSidebar} className="m-4">
        <HiOutlineMenu className="text-2xl" />
      </button>
      <ul className="w-full">
        <li>
          <NavLink
            to="/saved-grimoires"
            className={({ isActive }) =>
              isActive ? `${linkStyle} ${activeLinkStyle}` : linkStyle
            }
          >
            <HiOutlineBookOpen className="text-xl" />
            {isSidebarOpen && (
              <span className="text-base font-medium">Saved Grimoires</span>
            )}
          </NavLink>
        </li>
        <li>
          <NavLink
            to="/new-grimoire"
            className={({ isActive }) =>
              isActive ? `${linkStyle} ${activeLinkStyle}` : linkStyle
            }
          >
            <HiOutlinePlus className="text-xl" />
            {isSidebarOpen && (
              <span className="text-base font-medium">New Grimoire</span>
            )}
          </NavLink>
        </li>
        {/* Add more nav items here if needed */}
      </ul>
    </div>
  );
}

export default Navbar;
