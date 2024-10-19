// filename: Home.js

import React from 'react';
import './Home.css';
import MyPhoto from '../components/MyPhoto';

function Home() {
    return (
        <>
        <div className='gap'/>
        <div className="body">
            <div className="left">
                <h1>Yongkang Cheng</h1>
                <h1>程永康</h1>
                <h2>University of Toronto</h2>
                <h2>Computer Engineering</h2>
            </div>
            <div className="right">
            <MyPhoto />
            </div>
        </div>
        </>
    );
}

export default Home;