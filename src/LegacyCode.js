function Legacy() {
    return (
    <div className="container">
        <header>
        <meta name="Yongkang Cheng - University of Toronto" content="Personal Portfolio" />
        <h1>Yongkang Cheng</h1>
        <p>2nd year student in Computer Engineering at the University of Toronto</p>
        </header>

        <nav>
        <a href="#about">About Me</a>
        <a href="#skills">Skills</a>
        <a href="#projects">Projects</a>
        <a href="#contact">Contact</a>
        </nav>

        <main>
        <section id="about">
            <h2>About Me</h2>
            <p><strong>Education:</strong> Currently studying Computer Engineering at the University of Toronto.</p>
            <p><strong>Interests:</strong> Passionate about AI, deep learning, and computer vision. Enjoys working with Raspberry Pi to set up various services and exploring IoT applications. Enthusiastic about developing React applications and exploring frontend technologies.</p>
            <p><strong>Career Goals:</strong> Aspiring to become a leading AI engineer, driving innovation and technology applications.</p>
        </section>

        <section id="skills">
            <h2>Skills</h2>
            <h3>Programming Languages</h3>
            <ul>
            <li>Python (Proficient)</li>
            <li>C++ (Beginner, currently learning)</li>
            <li>JavaScript (Familiar)</li>
            </ul>

            <h3>Frameworks and Libraries</h3>
            <ul>
            <li>Deep Learning: PyTorch, TensorFlow</li>
            <li>Frontend Development: React</li>
            <li>Mobile Development: Android NDK</li>
            </ul>

            <h3>Tools</h3>
            <ul>
            <li>Docker (Familiar with containerization)</li>
            <li>Raspberry Pi (Experienced with practical projects)</li>
            </ul>

            <h3>Machine Learning and Deep Learning</h3>
            <ul>
            <li>Models & Algorithms: Attention Mechanisms, Graph Neural Networks (GCN, GNN, GAT), BERT, ViT, MobileNetV2</li>
            <li>Domains: Image Classification, Natural Language Processing, Computer Vision</li>
            </ul>
        </section>

        <section id="projects">
            <h2>Projects</h2>
            <div className="project">
            <h3>React-based Board Game Development</h3>
            <p><strong>Description:</strong> Developed an online board game using React, implementing real-time multiplayer and interactive features.</p>
            <p><strong>Tech Stack:</strong> React, JavaScript, HTML/CSS</p>
            </div>
            <div className="project">
            <h3>Image Classification with MobileNetV2</h3>
            <p><strong>Description:</strong> Conducted image classification research using PyTorch and the MobileNetV2 model, optimizing model performance.</p>
            <p><strong>Tech Stack:</strong> Python, PyTorch, Deep Learning</p>
            </div>
            <div className="project">
            <h3>Raspberry Pi Service Setup</h3>
            <p><strong>Description:</strong> Set up home automation services using Raspberry Pi, including media servers and IoT device control.</p>
            <p><strong>Tech Stack:</strong> Python, Raspberry Pi, IoT</p>
            </div>
        </section>

        <section id="contact">
            <h2>Contact</h2>
            <p><strong>Email:</strong><a href="mailto:yongkang.cheng@mail.utoronto.ca">yongkang.cheng@mail.utoronto.ca</a></p>
            <p><strong>LinkedIn:</strong><a href="https://www.linkedin.com/in/yongkang-cheng-b2407a2a6/">linkedin.com/in/yongkang-cheng-b2407a2a6/</a></p>
            <p><strong>GitHub:</strong><a href="https://github.com/Ken-2511">github.com/Ken-2511</a></p>
        </section>
        </main>

        <footer>
        <p>&copy; 2023 Yongkang Cheng</p>
        </footer>
    </div>
    );
}