import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import './App.css';
import Users from './components/Users';
import Teams from './components/Teams';
import Activities from './components/Activities';
import Leaderboard from './components/Leaderboard';
import Workouts from './components/Workouts';

function App() {
  // Dark mode state with localStorage persistence
  const [darkMode, setDarkMode] = useState(() => {
    const savedMode = localStorage.getItem('darkMode');
    return savedMode === 'true';
  });

  // Apply dark mode class to App div and save to localStorage
  useEffect(() => {
    localStorage.setItem('darkMode', darkMode);
  }, [darkMode]);

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
  };

  return (
    <Router>
      <div className={`App ${darkMode ? 'dark-mode' : ''}`}>
        <nav className="navbar navbar-expand-lg navbar-dark bg-dark sticky-top">
          <div className="container">
            <Link className="navbar-brand" to="/">
              <img src="/octofitapp-logo.png" alt="OctoFit Logo" className="navbar-logo" />
              OctoFit Tracker
            </Link>
            <button 
              className="navbar-toggler" 
              type="button" 
              data-bs-toggle="collapse" 
              data-bs-target="#navbarNav"
              aria-controls="navbarNav"
              aria-expanded="false"
              aria-label="Toggle navigation"
            >
              <span className="navbar-toggler-icon"></span>
            </button>
            <div className="collapse navbar-collapse" id="navbarNav">
              <ul className="navbar-nav ms-auto">
                <li className="nav-item">
                  <Link className="nav-link" to="/users">Users</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/teams">Teams</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/activities">Activities</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/leaderboard">Leaderboard</Link>
                </li>
                <li className="nav-item">
                  <Link className="nav-link" to="/workouts">Workouts</Link>
                </li>
              </ul>
            </div>
          </div>
        </nav>

        <Routes>
          <Route path="/" element={
            <div className="container mt-4">
              <div className="hero-section text-center">
                <h1 className="display-3">Welcome to OctoFit Tracker!</h1>
                <p className="lead">Track your fitness journey, compete with your team, and achieve your goals.</p>
                <hr className="my-4" style={{borderColor: 'rgba(255,255,255,0.3)'}} />
                <p className="mb-4">Use the navigation menu above to explore users, teams, activities, leaderboard, and workout suggestions.</p>
                <div className="d-flex justify-content-center gap-3">
                  <Link to="/leaderboard" className="btn btn-light btn-lg">
                    View Leaderboard
                  </Link>
                  <Link to="/workouts" className="btn btn-outline-light btn-lg">
                    Explore Workouts
                  </Link>
                </div>
              </div>
            </div>
          } />
          <Route path="/users" element={<Users />} />
          <Route path="/teams" element={<Teams />} />
          <Route path="/activities" element={<Activities />} />
          <Route path="/leaderboard" element={<Leaderboard />} />
          <Route path="/workouts" element={<Workouts />} />
        </Routes>

        {/* Dark Mode Toggle Button */}
        <button 
          className="dark-mode-toggle"
          onClick={toggleDarkMode}
          aria-label="Toggle dark mode"
          title={darkMode ? "Switch to Light Mode" : "Switch to Dark Mode"}
        >
          {darkMode ? '☀️' : '🌙'}
        </button>
      </div>
    </Router>
  );
}

export default App;
