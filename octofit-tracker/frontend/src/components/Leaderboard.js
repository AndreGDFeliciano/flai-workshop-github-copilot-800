import React, { useState, useEffect } from 'react';

const Leaderboard = () => {
  const [topUsers, setTopUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const API_URL = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/users/top_performers/`;

  useEffect(() => {
    console.log('Fetching leaderboard from:', API_URL);
    
    fetch(API_URL)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Leaderboard API response:', data);
        // Handle both paginated (.results) and plain array responses
        const usersList = data.results || data;
        console.log('Processed leaderboard data:', usersList);
        setTopUsers(usersList);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching leaderboard:', error);
        setError(error.message);
        setLoading(false);
      });
  }, [API_URL]);

  const getMedalClass = (index) => {
    if (index === 0) return 'gold-medal';
    if (index === 1) return 'silver-medal';
    if (index === 2) return 'bronze-medal';
    return '';
  };

  if (loading) {
    return (
      <div className="container mt-4">
        <div className="loading-spinner">
          <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          <p className="mt-3">Loading leaderboard...</p>
        </div>
      </div>
    );
  }
  
  if (error) {
    return (
      <div className="container mt-4">
        <div className="alert alert-danger error-message" role="alert">
          <h4 className="alert-heading">Error!</h4>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="container mt-4">
      <div className="page-header">
        <h2>🏆 Leaderboard - Top Performers</h2>
        <p>See who's leading the fitness challenge!</p>
      </div>
      
      <div className="table-container">
        <div className="table-responsive">
          <table className="table table-hover align-middle">
            <thead>
              <tr>
                <th scope="col" className="text-center" style={{width: '100px'}}>Rank</th>
                <th scope="col">Name</th>
                <th scope="col">Alias</th>
                <th scope="col">Team</th>
                <th scope="col" className="text-center">Total Points</th>
                <th scope="col" className="text-center">Fitness Level</th>
              </tr>
            </thead>
            <tbody>
              {topUsers.map((user, index) => (
                <tr key={user.id} className={getMedalClass(index)}>
                  <td className="text-center">
                    <div className="leaderboard-rank">
                      {index + 1}
                      {index === 0 && ' 🥇'}
                      {index === 1 && ' 🥈'}
                      {index === 2 && ' 🥉'}
                    </div>
                  </td>
                  <td><strong>{user.name}</strong></td>
                  <td><span className="badge bg-secondary">{user.alias}</span></td>
                  <td>{user.team_name || <span className="text-muted">No Team</span>}</td>
                  <td className="text-center">
                    <h5 className="mb-0">
                      <span className="badge bg-primary">{user.total_points}</span>
                    </h5>
                  </td>
                  <td className="text-center"><span className="badge bg-info">{user.fitness_level}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Leaderboard;
