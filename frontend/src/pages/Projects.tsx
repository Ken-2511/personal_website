// filename: Projects.tsx

import React from "react";
import "./Projects.css";

// 定义 ProjectCard 组件的 Props 类型
interface ProjectCardProps {
    title: string;        // 项目标题，必填
    duration: string;     // 项目时间范围，必填
    description: string;  // 项目描述，必填
    tech: string;         // 技术栈，必填
}

const ProjectCard: React.FC<ProjectCardProps> = ({ title, duration, description, tech }) => {
    return (
        <div className="project-card">
            <h3>{title}</h3>
            <p className="project-duration">{duration}</p>
            <p>{description}</p>
            <p className="project-tech">Tech: {tech}</p>
        </div>
    );
};

// 定义项目数据的类型
interface ProjectData {
    title: string;
    duration: string;
    description: string;
    tech: string;
}

const Projects: React.FC = () => {
    // 项目数据数组
    const projectsData: ProjectData[] = [
        {
            title: "Handwritten Text Recognition Project",
            duration: "June 2024 - Aug 2024 | University of Toronto",
            description:
                "Designed and trained a CRNN in PyTorch, achieving 87% word-level and 95% character-level accuracy. Developed a connected-pixels algorithm for efficient image preprocessing, processing 1024x1024 images in under 4 seconds. Built a Tkinter-based GUI for real-time handwriting recognition, capable of transcribing 100 words in 10 seconds.",
            tech: "Python, PyTorch, Tkinter, NumPy",
        },
        {
            title: "The Voluntrack Project",
            duration: "May 2024 - Present | Voluntrack.org",
            description:
                "Led frontend development for a Non-Profit Organization, utilizing React Native and React.js to create a mobile app and web interface. Organized biweekly tech team meetings, improved app design, and enhanced user experience with clear interface layouts.",
            tech: "React, React Native, JavaScript",
        },
        {
            title: "Engineering Strategy and Practice Project",
            duration: "Jan 2024 - April 2024 | University of Toronto",
            description:
                "Led a team of 6 students to redesign the wellness room in Chestnut Residence. Managed client communications, organized tasks with Gantt charts, and self-learned Blender to produce 3D models and visuals, improving client understanding and approval of the final design.",
            tech: "Project Management, Blender, Team Collaboration",
        },
        {
            title: "Diary with ChatGPT Comment Project",
            duration: "Sep 2023 - Present | Personal Project",
            description:
                "Developed a diary application that integrates OpenAI GPT models for AI-generated feedback, enabling contextual scoring and word frequency analysis. Designed a secure backend with text encryption and optimized API calls to ensure performance efficiency and data privacy.",
            tech: "Python, OpenAI API, Encryption, Backend Development",
        },
        {
            title: "Verilog Pac-Man Game",
            duration: "Nov 2024 | University of Toronto",
            description:
                "Developed a Pac-Man-inspired FPGA game with over 1,620 lines of Verilog code, achieving high-quality VGA visuals using parameterized design. Debugged and optimized graphical rendering and game logic with ModelSim, ensuring stable gameplay and smooth VGA output.",
            tech: "Verilog, ModelSim, FPGA",
        },
        {
            title: "Build Personal Website",
            duration: "Oct 2024 - Present | Personal Project",
            description:
                "Self-hosted a personal website on Raspberry Pi, built using React.js, FastAPI, and Nginx with TLS encryption and DDNS for remote access. Implemented an interactive chatbot powered by OpenAI API for real-time Q&A, leveraging NoSQL for context management.",
            tech: "React.js, FastAPI, Nginx, Raspberry Pi, OpenAI API",
        },
    ];    

    return (
        <section className="projects-section" id="projects">
            <h2 className="projects-title">Projects</h2>
            <div className="projects-container">
                {projectsData.map((project, index) => (
                    <ProjectCard key={index} {...project} />
                ))}
            </div>
        </section>
    );
};

export default Projects;
