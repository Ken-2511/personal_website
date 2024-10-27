import React from "react";
import "./Projects.css";

function Projects() {
    return (
        <section className="projects-section" id="projects">
            <h2 className="projects-title">Projects</h2>
            <div className="projects-container">
                <div className="project">
                    <h3>Handwritten Text Recognition Project</h3>
                    <p className="project-duration">June 2024 - Aug 2024 | University of Toronto</p>
                    <p>
                        Trained a neural network with transfer learning and data augmentation on IAM and CVL datasets, achieving
                        87% word-level and 95% character-level accuracy. Optimized CRNN by adjusting the architecture and
                        adding a learning rate scheduler for enhanced model performance and stability. Developed a Tkinter GUI
                        for real-time handwriting recognition.
                    </p>
                    <p className="project-tech">Tech: Python, PyTorch, Tkinter</p>
                </div>

                <div className="project">
                    <h3>The Voluntrack Project</h3>
                    <p className="project-duration">May 2024 - Present | Voluntrack.org</p>
                    <p>
                        Worked as Frontend Manager in an NPO, utilizing React Native and React JS to develop a mobile app and web page.
                        Hosted team meetings biweekly, assigned new tasks, and updated the website regularly.
                    </p>
                    <p className="project-tech">Tech: React, React Native, JavaScript</p>
                </div>

                <div className="project">
                    <h3>Engineering Strategy and Practice Project</h3>
                    <p className="project-duration">Jan 2024 - April 2024 | University of Toronto</p>
                    <p>
                        Managed a client's proposal project with a team of 6 students to revamp the wellness room in Chestnut Residence.
                        Conducted weekly meetings, set deadlines, and managed timelines with Gantt charts.
                    </p>
                    <p className="project-tech">Tech: Project Management, Team Leadership</p>
                </div>

                <div className="project">
                    <h3>Diary with ChatGPT Comment Project</h3>
                    <p className="project-duration">Sep 2023 - Present | Personal Project</p>
                    <p>
                        Developed a diary web application that integrates with ChatGPT to provide AI-generated feedback on journal entries,
                        enhancing user reflections and insights. Built with a full-stack approach using Python, JavaScript, and HTML/CSS,
                        utilizing OpenAI's API for real-time comment generation.
                    </p>
                    <p className="project-tech">Tech: Python, JavaScript, HTML/CSS, OpenAI API</p>
                </div>
            </div>
        </section>
    );
}

export default Projects;
