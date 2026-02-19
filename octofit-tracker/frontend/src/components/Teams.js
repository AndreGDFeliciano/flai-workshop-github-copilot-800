import React, { useState, useEffect } from 'react';

const Teams = () => {
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const API_URL = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/teams/`;

  useEffect(() => {
    console.log('Fetching teams from:', API_URL);
    
    fetch(API_URL)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Teams API response:', data);
        // Handle both paginated (.results) and plain array responses
        const teamsList = data.results || data;
        console.log('Processed teams data:', teamsList);
        setTeams(teamsList);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching teams:', error);
        setError(error.message);
        setLoading(false);
      });
  }, [API_URL]);

  if (loading) {
    return (
      <div className="container mt-4">
        <div className="loading-spinner">
          <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          <p className="mt-3">Loading teams...</p>
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
        <h2>🏆 Teams</h2>
        <p>Browse all fitness teams in the OctoFit community</p>
      </div>
      
      <div className="mb-3">
        <h5>Total Teams: <span className="badge bg-primary">{teams.length}</span></h5>
      </div>

      <div className="row">
        {teams.map(team => (
          <div key={team.id} className="col-md-6 col-lg-4 mb-4">
            <div className="card h-100">
              <div className="card-header bg-primary text-white">
                <h5 className="card-title mb-0">{team.name}</h5>
              </div>
              <div className="card-body">
                <p className="card-text">{team.description}</p>
                <div className="mt-3">
                  <span className="badge bg-success">
                    👥 {team.member_count || 0} Members
                  </span>
                </div>
              </div>
              <div className="card-footer text-muted">
                <small>
                  Created: {new Date(team.created_at).toLocaleDateString()}
                </small>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Teams;
