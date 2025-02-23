import { useState, useEffect } from "react";
import "./Header.css";
import { Link, useLocation } from "react-router-dom";

function Header() {
    const [isMenuOpen, setIsMenuOpen] = useState(false);

    const toggleMenu = () => {
        setIsMenuOpen(!isMenuOpen);
    };

    // 判断是否是主页
    const [isHome, setIsHome] = useState(false);

    const location = useLocation();

    useEffect(() => {
        setIsHome(location.pathname !== "/");
    }, [location]);

    return (
        <header className="header">
            <div className="header-left">
                <h1 className="name">Yongkang Cheng</h1>
                
            </div>
            <div className="header-right">
                <button className="hamburger" onClick={toggleMenu}>
                    {/* 汉堡按钮图标 */}
                    <span className="bar"></span>
                    <span className="bar"></span>
                    <span className="bar"></span>
                </button>
                <nav className={`navi ${isMenuOpen ? "open" : ""}`}>
                    {isHome && (
                    <Link to="/" onClick={() => setIsMenuOpen(false)}>
                        <span role="img" aria-label="home">🏠</span> Home
                    </Link>
                    )}
                    <Link to="/skills" onClick={() => setIsMenuOpen(false)}>
                        <span role="img" aria-label="muscle">💪</span> Skills
                    </Link>
                    <Link to="/projects" onClick={() => setIsMenuOpen(false)}>
                        <span role="img" aria-label="rocket">🚀</span> Projects
                    </Link>
                    <Link to="/fun-facts" onClick={() => setIsMenuOpen(false)}>
                        <span role="img" aria-label="fun">😝</span> Fun Facts
                    </Link>
                    <Link to="/resume" onClick={() => setIsMenuOpen(false)}>
                        <span role="img" aria-label="document">📄</span> Resume
                    </Link>
                    <Link to="/chat" onClick={() => setIsMenuOpen(false)}>
                        <span role="img" aria-label="chat">💬</span> Chat
                    </Link>
                </nav>
            </div>
        </header>
    );
}

export default Header;
