import React from 'react';
import './App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import HomePage from './pages/HomePage';
import SimulationPage from './pages/SimulationPage';
import RiskAnalysisPage from './pages/RiskAnalysisPage';
import AsteroidLauncherPage from './pages/AsteroidLauncherPage';
import NavBar from './components/NavBar';

const darkTheme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#00ff88',
    },
    secondary: {
      main: '#ff6b35',
    },
    background: {
      default: '#0c1445',
      paper: '#1a1a2e',
    },
  },
  typography: {
    fontFamily: "'Roboto', 'Arial', sans-serif",
    h1: {
      fontSize: '3rem',
      fontWeight: 600,
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={darkTheme}>
      <CssBaseline />
      <Router>
        <div className="App">
          <NavBar />
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/simulation" element={<SimulationPage />} />
            <Route path="/risk-analysis" element={<RiskAnalysisPage />} />
            <Route path="/asteroid-launcher" element={<AsteroidLauncherPage />} />
          </Routes>
        </div>
      </Router>
    </ThemeProvider>
  );
}

export default App;