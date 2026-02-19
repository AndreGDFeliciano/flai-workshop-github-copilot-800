import React, { useState, useEffect } from 'react';

const Users = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const API_URL = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/users/`;

  useEffect(() => {
    console.log('Fetching users from:', API_URL);
    
    fetch(API_URL)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Users API response:', data);
        // Handle both paginated (.results) and plain array responses
        const usersList = data.results || data;
        console.log('Processed users data:', usersList);
        setUsers(usersList);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching users:', error);
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
          <p className="mt-3">Loading users...</p>
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
        <h2>👥 All Users</h2>
        <p>View all registered users and their fitness profiles</p>
      </div>
      
      <div className="table-container">
        <div className="d-flex justify-content-between align-items-center mb-3">
          <h5 className="mb-0">Total Users: <span className="badge bg-primary">{users.length}</span></h5>
        </div>
        <div className="table-responsive">
          <table className="table table-striped table-hover align-middle">
            <thead>
              <tr>
                <th scope="col">Name</th>
                <th scope="col">Alias</th>
                <th scope="col">Email</th>
                <th scope="col">Team</th>
                <th scope="col">Fitness Level</th>
                <th scope="col" className="text-center">Total Points</th>
              </tr>
            </thead>
            <tbody>
              {users.map(user => (
                <tr key={user._id}>
                  <td><strong>{user.name}</strong></td>
                  <td><span className="badge bg-secondary">{user.alias}</span></td>
                  <td>{user.email}</td>
                  <td>{user.team_name || <span className="text-muted">No Team</span>}</td>
                  <td><span className="badge bg-info">{user.fitness_level}</span></td>
                  <td className="text-center"><strong className="text-primary">{user.total_points}</strong></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Users;
