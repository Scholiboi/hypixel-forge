import React from "react";
import './navbar.css'
const Navbar = ({ transfer }) => {
    return (
        <nav id="navbar">
            <p id="Header">Forge Calculator</p>
            <p id="Sandbox">
                <a href='/sandbox'>Forge Menu</a>
            </p>
            <p id="resource">
                <a onClick={transfer}>Modify Resources</a>
            </p>
        </nav>
    );
}

export default Navbar;