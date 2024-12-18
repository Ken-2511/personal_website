// filename: Skills.tsx

import React from "react";
import "./Skills.css";

// 定义 Skill 组件的 Props 类型
interface SkillProps {
    name: string;
}

const Skill: React.FC<SkillProps> = ({ name }) => {
    return <li>{name}</li>;
};

// 定义 SkillGroup 组件的 Props 类型
interface SkillGroupProps {
    category: string;
    skills: string[];
}

const SkillGroup: React.FC<SkillGroupProps> = ({ category, skills }) => {
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
};

// Skills 组件不接受任何 Props
const Skills: React.FC = () => {
    // 将技能数据分成两列
    const firstColumn: SkillGroupProps[] = [
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

    const secondColumn: SkillGroupProps[] = [
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
};

export default Skills;
