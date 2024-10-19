// filename: App.js

import React from 'react';
import './App.css';
import FixedBackground from './components/FixedBackground';
import Home from './pages/Home';
import Skills from './pages/Skills';
import Projects from './pages/Projects';

function App() {
  return (
    <>
      {/* <FixedBackground /> */}
      <Home />
      <Skills />
      <Projects />
    </>
  );
}

export default App;
