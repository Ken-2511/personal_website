import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import './App.css'
import Header from './components/Header'
import Home from './pages/Home'
import Skills from './pages/Skills'
import Projects from './pages/Projects'
import FunFacts from './pages/FunFacts'
import Chat from './pages/Chat'
import NotFound from './pages/NotFound'

function App() {

  return (
    <Router>
      <Header />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/skills" element={<Skills />} />
        <Route path="/projects" element={<Projects />} />
        <Route path="/fun-facts" element={<FunFacts />} />
        <Route path="/chat" element={<Chat />} />
        {/* <Route path="/3ace6bf23d0dceb63ef7ad28469f336465ef6ce7f818a355cbb1f71907becc39" element={<PureChat />} /> */}
        <Route path="*" element={<NotFound />} />
      </Routes>
    </Router>
  )
}

export default App
