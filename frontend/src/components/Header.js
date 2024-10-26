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
          <Link to="/">🏠 Home</Link>
          <Link to="/skills">💪 Skills</Link>
          <Link to="/projects">🚀 Projects</Link>
          <Link to="/fun-facts">😝 Fun Facts</Link>
          {/* <a href="#skills">💪 Skills</a>
          <a href="#projects">🚀 Projects</a>
          <a href="#fun-facts">😝 Fun Facts</a> */}
        </nav>
      </header>
    );
}

export default Header;