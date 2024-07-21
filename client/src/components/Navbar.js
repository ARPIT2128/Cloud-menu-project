import React from "react";
import { NavLink } from "react-router-dom";

const Navbar = () => {
  return (
    <nav>
      <div className="nav-leading-text">🚀Imagine Manu</div>
      <ul>
        <li>
          <NavLink
            className={({ isActive }) => (isActive ? "NavClass" : "")}
            to="/"
          >
            Home
          </NavLink>
        </li>
        <li>
          <NavLink
            className={({ isActive }) => (isActive ? "NavClass" : "")}
            to="/Vision"
          >
            Vision
          </NavLink>
        </li>
        <li>
          <NavLink
            className={({ isActive }) => (isActive ? "NavClass" : "")}
            to="/AWS"
          >
            AWS
          </NavLink>
        </li>
        <li>
          <NavLink
            className={({ isActive }) => (isActive ? "NavClass" : "")}
            to="/Audio"
          >
            Audio
          </NavLink>
        </li>
        <li>
          <NavLink
            className={({ isActive }) => (isActive ? "NavClass" : "")}
            to="/Message"
          >
            Message
          </NavLink>
        </li>
      </ul>
    </nav>
  );
};

export default Navbar;
