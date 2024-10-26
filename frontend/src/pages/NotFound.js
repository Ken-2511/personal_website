import React from "react";
import "./NotFound.css";

function NotFound() {
    return (
        <div className="NotFound">
        <h1>404</h1>
        <p>Page not found!</p>
        <a href="/">Go back to the main page</a>
        </div>
    );
}

export default NotFound;