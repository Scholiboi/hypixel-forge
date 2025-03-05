import React from "react";
import { Link } from "react-router-dom";

const NotFound = () => {
    return (
        <div style={{ textAlign: 'center' }}>
            <h1>404 - Page Not Found</h1>
            <p>Sorry, this page doesn't exist.</p>
            <Link to="/" style={{ color: 'blue', textDecoration: 'underline' }}>
                Go back to Home
            </Link>
        </div>
    );
};

export default NotFound;