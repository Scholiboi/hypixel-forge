import React from "react";
import {useLocation} from "react-router-dom";
import './navbar.css'

const Navbar = ({transfer}) => {
    const location = useLocation();

    const renderNavbar = () => {
        switch (location.pathname) {
            case '/':
                return (
                    <nav id="navbar-home">
                        <p id="Header">Your resources</p>
                        <div className="nav-items">
                            <p id="Sandbox">
                                <a href='/sandbox'>Forge Menu</a>
                            </p>
                            <p id="resource">
                                <a onClick={transfer}>Modify Resources</a>
                            </p>
                        </div>
                    </nav>
                );
            case '/sandbox':
                return (
                    <nav id="navbar-forge">
                        <p id="Header">Forge Menu</p>
                        <div className="nav-items">
                            <p id="Home">
                                <a href='/'>Home</a>
                            </p>
                        </div>
                    </nav>
                );
            case '/sandbox/forge':
                return (
                    <nav id="navbar-forge">
                        <p id="Header">Forge Menu</p>
                        <div className="nav-items">
                            <p id="Home">
                                <a href='/'>Home</a>
                            </p>
                        </div>
                    </nav>
                );
            default:
                return (
                    <nav id="navbar-default">
                        <p id="Header">Forge Calculator</p>
                        <div className="nav-items">
                            <p id="Sandbox">
                                <a href='/sandbox'>Forge Menu</a>
                            </p>
                            <p id="Home">
                                <a href='/'>Home</a>
                            </p>
                        </div>
                    </nav>
                );
        }
    }

    return renderNavbar();
}

export default Navbar;