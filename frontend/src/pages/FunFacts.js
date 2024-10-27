import React from "react";
import "./FunFacts.css";
import Header from "../components/Header";

function FunFactCard({ title, description, image}) {
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
            description: "I run this website on my Raspberry Pi! Yes, it's a tiny computer doing a big job.",
            // image: "/assets/raspberry-pi.jpg",
        },
        {
            title: "My Hobbies",
            description: "Playing table tennis, coding little apps, binge-watching Bilibili, and indulging in sweets—life is all about balance, right?",
            // image: "/assets/hobbies.jpg",
        },
        {
            title: "Casual Gamer",
            description: "Sometimes I dive into the worlds of Genshin Impact and Party Animals, just for fun.",
            // image: "/assets/gaming.jpg",
        },
        {
            title: "Always Open to New Things",
            description: "Whether it's trying out a new university or making new friends, I'm always up for an adventure.",
            // image: "/assets/exploration.jpg",
        },
        {
            title: "Silicon Valley Dreamer",
            description: "One day, you'll find me working in Silicon Valley. Until then, I'm putting in the work!",
            // image: "/assets/silicon-valley.jpg",
        },
        {
            title: "Headphones Lover",
            description: "I love wearing headphones and getting lost in music—especially instrumental tracks and songs by sweet-voiced singers.",
            // image: "/assets/headphones.jpg",
        },
        {
            title: "Written by ChatGPT",
            description: "Yes, all these fun facts were crafted with a little help from ChatGPT!",
        },
    ];
    
    
    
    return (
        <>
        <Header />
        <section className="fun-facts-section" id="fun-facts">
            <h1>Fun Facts</h1>
            <div className="fun-facts-container">
                {funFactsData.map((funFact, index) => (
                    <FunFactCard key={index} {...funFact} />
                ))}
            </div>
        </section>
        </>
    );
}

export default FunFacts;