import React from "react";
import "./FixedBackground.css";

function FixedBackground() {
    return (
        <div className="fixed-background">
            <img className="background-image"
                src={process.env.PUBLIC_URL + "/assets/background.png"}
                alt="background"
            />
        </div>
    );
}

export default FixedBackground;