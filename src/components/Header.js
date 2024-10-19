import React from "react";
import "./Header.css";

function Header() {
    return (
        <header className="header">
        <div className="header-left">
          <h1 className="name">Yongkang Cheng</h1>
        </div>
        <nav className="header-right">
          <a href="#skills">💪 Skills</a>
          <a href="#projects">🚀 Projects</a>
          <a href="#fun-facts">😝 Fun Facts</a>
        </nav>
      </header>
    );
}

export default Header;