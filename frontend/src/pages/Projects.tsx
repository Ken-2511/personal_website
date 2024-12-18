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
                "Trained a neural network with transfer learning and data augmentation on IAM and CVL datasets, achieving 87% word-level and 95% character-level accuracy. Optimized CRNN by adjusting the architecture and adding a learning rate scheduler for enhanced model performance and stability. Developed a Tkinter GUI for real-time handwriting recognition.",
            tech: "Python, PyTorch, Tkinter",
        },
        {
            title: "The Voluntrack Project",
            duration: "May 2024 - Present | Voluntrack.org",
            description:
                "Worked as Frontend Manager in an NPO, utilizing React Native and React JS to develop a mobile app and web page. Hosted team meetings biweekly, assigned new tasks, and updated the website regularly.",
            tech: "React, React Native, JavaScript",
        },
        {
            title: "Engineering Strategy and Practice Project",
            duration: "Jan 2024 - April 2024 | University of Toronto",
            description:
                "Managed a client's proposal project with a team of 6 students to revamp the wellness room in Chestnut Residence. Conducted weekly meetings, set deadlines, and managed timelines with Gantt charts.",
            tech: "Project Management, Team Leadership",
        },
        {
            title: "Diary with ChatGPT Comment Project",
            duration: "Sep 2023 - Present | Personal Project",
            description:
                "Developed a diary web application that integrates with ChatGPT to provide AI-generated feedback on journal entries, enhancing user reflections and insights. Built with a full-stack approach using Python, JavaScript, and HTML/CSS, utilizing OpenAI's API for real-time comment generation.",
            tech: "Python, JavaScript, HTML/CSS, OpenAI API",
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
