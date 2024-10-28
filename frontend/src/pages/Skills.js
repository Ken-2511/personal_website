// filename: Skills.js

import React from "react";
import "./Skills.css";

function Skill({ name }) {
    return <li>{name}</li>;
}

function SkillGroup({ category, skills }) {
    return (
        <div className="skill-group">
            <h3>{category}</h3>
            <ul>
                {skills.map((skill, index) => (
                    <Skill key={index} name={skill} />
                ))}
            </ul>
        </div>
    );
}

function Skills() {
    // 将技能数据分成两列
    const firstColumn = [
        {
            category: "Programming Languages",
            skills: ["Python", "JavaScript", "C", "C++", "Java", "C#", "Verilog"],
        },
        {
            category: "Web Development",
            skills: ["HTML/CSS", "React", "Node.js"],
        },
        {
            category: "Machine Learning & Data Science",
            skills: ["PyTorch", "OpenCV", "NumPy", "MatplotLib", "Pillow", "Pandas", "Scikit-learn"],
        },
        {
            category: "Databases",
            skills: ["NoSQL/MongoDB", "SQLite"],
        },
        {
            category: "Languages",
            skills: ["English (Fluent)", "Mandarin (Native)"],
        },
    ];
    
    const secondColumn = [
        {
            category: "Tools & Technologies",
            skills: [
                "Linux", "Git", "SSH", "Docker", "VS Code", "Jupyter",
                "Web Scraping", "Arduino", "Raspberry Pi", "MatLab"
            ],
        },
        {
            category: "3D Design & Game Development",
            skills: [
                "Blender", "Unity", "Rhino", "3Ds Max", "3D Printing"
            ],
        },
        {
            category: "Other Skills",
            skills: ["Machine Learning", "Data Structures", "Algorithms", "OOP", "RESTful APIs"],
        },
        {
            category: "Cloud & Deployment",
            skills: ["Certbot", "FastAPI"],
        },
    ];
    

    return (
        <section className="skills-section" id="skills">
            <h2 className="skills-title">Technical Skills</h2>
            <div className="skills-container">
                {/* 第一列 */}
                <div className="skill-column">
                    {firstColumn.map((group, index) => (
                        <SkillGroup key={index} {...group} />
                    ))}
                </div>
                {/* 第二列 */}
                <div className="skill-column">
                    {secondColumn.map((group, index) => (
                        <SkillGroup key={index} {...group} />
                    ))}
                </div>
            </div>
        </section>
    );
}

export default Skills;
