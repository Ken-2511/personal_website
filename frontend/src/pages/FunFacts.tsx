// filename: FunFacts.js

import React from "react";
import "./FunFacts.css";

interface FunFactCardProps {
    title: string;
    description: string;
    image?: string;
}

// function FunFactCard({ title, description, image}) {
const FunFactCard: React.FC<FunFactCardProps> = ({ title, description, image }) => {
    // title and dectiprion are required

    const [isImageLoaded, setIsImageLoaded] = React.useState(true);

    const handleImageLoadError = () => {
        setIsImageLoaded(false);
    }

    return (
        <div className="fun-fact-card">
            <div className="text-container">
            <h2>{title}</h2>
            <p>{description}</p>
            </div>
            {image && isImageLoaded && (
            <div className="img-container">
                <img src={image} alt={title} onError={handleImageLoadError} />
            </div>)}
        </div>
    );
}

function FunFacts() {
    const funFactsData = [
        {
            title: "I Have a Raspberry Pi",
            description: "Powered by a Raspberry Pi 5 with 4GB RAM, this website is served from a tiny computer inside a deliciously red-and-white case that looks almost good enough to eat. It’s running React+Vite on the front end, FastAPI+OpenAI API on the back end, and even hosts a piece of my personal diary!",
            image: "/assets/raspberry-pi.jpg",
        },
        {
            title: "My Hobbies",
            description: "A casual table tennis player, a tech enthusiast on Bilibili (big fan of 稚晖君), and a sweets addict—my life is all about chasing tech trends while indulging my sweet tooth. Balance, right?",
            image: "/assets/ice-cream.jpg",
        },
        {
            title: "Casual Gamer",
            description: "When I’m not busy coding, I’m usually saving Teyvat as Hu Tao in Genshin Impact or laughing my heart out in Party Animals. Who wouldn’t love a lively, mischievous girl like Hu Tao?",
            image: "/assets/genshin-impact.jpg",
        },
        {
            title: "Always Open to New Things",
            description: "I dream of working in Silicon Valley one day, drawn to its culture, tech innovation, and vibrant urban life. High salaries? Oh no, not at all (*wink*). My ultimate goal: creating a Super AI that changes the world.",
            // image: "/assets/exploration.jpg",
        },
        {
            title: "What is IWMAIN",
            description: "My email, iwmain@outlook.com, stands for \"I Will Make an AI Nova.\" Nova is a nod to a brilliant classmate and also represents intelligence and brilliance. My dream is to create a robot that looks human, thinks independently, and feels emotions. Perfection isn’t the goal, but she will be.",
            // image: "/assets/nova.jpg",
        },
        {
            title: "Headphones Lover",
            description: "Equipped with my Bose QC-45 headphones (thanks to my friend 黄琎’s recommendation), I dive into tracks like \"If I Can Stop One Heart From Breaking\" - a beautiful song that never fails to move me.",
            // image: "/assets/headphones.jpg",
        },
        {
            title: "Written by ChatGPT",
            description: "Every fun fact you see here was crafted by ChatGPT, with a little help from my answers to its clever questions. Proof that AI can be personal, too!",
        },
    ];
    
    
    
    
    return (
        <section className="fun-facts-section" id="fun-facts">
            <h1 className="fun-facts-title">Fun Facts</h1>
            <div className="fun-facts-container">
                {funFactsData.map((funFact, index) => (
                    <FunFactCard key={index} {...funFact} />
                ))}
            </div>
        </section>
    );
}

export default FunFacts;