// filename: App.js

import React from 'react';
import './App.css';
import Header from './components/Header';
import Home from './pages/Home';
import Skills from './pages/Skills';
import Projects from './pages/Projects';
import FunFacts from './pages/FunFacts';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

function App() {
  return (
    <Router>
      <Header />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/skills" element={<Skills />} />
        <Route path="/projects" element={<Projects />} />
        <Route path="/fun-facts" element={<FunFacts />} />
      </Routes>
    </Router>
  );
}

export default App;
