import React from "react";
import {useLocation} from "react-router-dom";
import './navbar.css'

const Navbar = ({transfer}) => {
    const location = useLocation();

    const renderNavbar = () => {
        switch (location.pathname) {
            case '/':
                return (
                    <nav className="mc-navbar" id="navbar-home">
                        <p className="mc-navbar-title" id="Header">Skyblock Mining Resource Reader</p>
                        <div className="nav-items">
                            <p id="Sandbox">
                                <button className="mc-button" onClick={() => window.location.href='/sandbox'}>
                                    Forge Menu
                                </button>
                            </p>
                            <p id="resource">
                                <button className="mc-button" onClick={transfer}>
                                    Modify Resources
                                </button>
                            </p>
                        </div>
                    </nav>
                );
            case '/sandbox':
                return (
                    <nav className="mc-navbar" id="navbar-forge">
                        <p className="mc-navbar-title" id="Header">Forge Menu</p>
                        <div className="nav-items">
                            <p id="Home">
                                <button className="mc-button" onClick={() => window.location.href='/'}>
                                    Home
                                </button>
                            </p>
                        </div>
                    </nav>
                );
            case '/sandbox/forge':
                return (
                    <nav className="mc-navbar" id="navbar-forge">
                        <p className="mc-navbar-title" id="Header">Forge Menu</p>
                        <div className="nav-items">
                            <p id="Home">
                                <button className="mc-button" onClick={() => window.location.href='/'}>
                                    Home
                                </button>
                            </p>
                        </div>
                    </nav>
                );
            default:
                return (
                    <nav className="mc-navbar" id="navbar-default">
                        <p className="mc-navbar-title" id="Header">Skyblock Mining Resource Reader</p>
                        <div className="nav-items">
                            <p id="Sandbox">
                                <button className="mc-button" onClick={() => window.location.href='/sandbox'}>
                                    Forge Menu
                                </button>
                            </p>
                            <p id="Home">
                                <button className="mc-button" onClick={() => window.location.href='/'}>
                                    Home
                                </button>
                            </p>
                        </div>
                    </nav>
                );
        }
    }

    return renderNavbar();
}

export default Navbar;