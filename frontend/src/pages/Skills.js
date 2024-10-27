import React from "react";
import "./Skills.css";
import Header from "../components/Header";

function Skills() {
    return (
        <>
        <Header />
        <section className="skills-section" id="skills">
            <h2 className="skills-title">Technical Skills</h2>
            <div className="skills-container">
                <div className="skill-category">
                    <h3>Programming Languages</h3>
                    <ul>
                        <li>Python</li>
                        <li>JavaScript</li>
                        <li>C</li>
                        <li>C++</li>
                        <li>Java</li>
                        <li>C#</li>
                    </ul>
                </div>
                <div className="skill-category">
                    <h3>Tools & Software</h3>
                    <ul>
                        <li>PyTorch</li>
                        <li>React</li>
                        <li>MatLab</li>
                        <li>Linux</li>
                        <li>Git</li>
                        <li>SSH</li>
                        <li>Tkinter</li>
                        <li>Pygame</li>
                        <li>Unity</li>
                        <li>Web Scraping</li>
                        <li>3D Modeling & Printing</li>
                        <li>Arduino</li>
                        <li>Raspberry Pi</li>
                    </ul>
                </div>
            </div>
        </section>
        </>
    );
}

export default Skills;
