import React from "react";
import "./Header.css";
import { Link } from "react-router-dom";

function Header() {
    return (
        <header className="header">
        <div className="header-left">
          <h1 className="name">Yongkang Cheng</h1>
        </div>
        <nav className="header-right">
          <Link to="/">
            <span role="img" aria-label="home">🏠</span> Home
          </Link>
          <Link to="/skills">
            <span role="img" aria-label="muscle">💪</span> Skills
          </Link>
          <Link to="/projects">
            <span role="img" aria-label="rocket">🚀</span> Projects
          </Link>
          <Link to="/fun-facts">
            <span role="img" aria-label="fun">😝</span> Fun Facts
          </Link>
        </nav>
      </header>
    );
}

export default Header;