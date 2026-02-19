import React, { useState, useEffect } from 'react';

const Activities = () => {
  const [activities, setActivities] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const API_URL = `https://${process.env.REACT_APP_CODESPACE_NAME}-8000.app.github.dev/api/activities/`;

  useEffect(() => {
    console.log('Fetching activities from:', API_URL);
    
    fetch(API_URL)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Activities API response:', data);
        // Handle both paginated (.results) and plain array responses
        const activitiesList = data.results || data;
        console.log('Processed activities data:', activitiesList);
        setActivities(activitiesList);
        setLoading(false);
      })
      .catch(error => {
        console.error('Error fetching activities:', error);
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
          <p className="mt-3">Loading activities...</p>
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
        <h2>📊 Activity Log</h2>
        <p>Track all fitness activities logged by users</p>
      </div>
      
      <div className="table-container">
        <div className="d-flex justify-content-between align-items-center mb-3">
          <h5 className="mb-0">Total Activities: <span className="badge bg-primary">{activities.length}</span></h5>
        </div>
        <div className="table-responsive">
          <table className="table table-striped table-hover align-middle">
            <thead>
              <tr>
                <th scope="col">User</th>
                <th scope="col">Type</th>
                <th scope="col">Date</th>
                <th scope="col" className="text-center">Duration (min)</th>
                <th scope="col" className="text-center">Distance (km)</th>
                <th scope="col" className="text-center">Points</th>
                <th scope="col">Notes</th>
              </tr>
            </thead>
            <tbody>
              {activities.map(activity => (
                <tr key={activity.id}>
                  <td><span className="badge bg-secondary">{activity.user_alias}</span></td>
                  <td><span className="badge bg-success">{activity.activity_type}</span></td>
                  <td>{new Date(activity.date).toLocaleDateString()}</td>
                  <td className="text-center"><strong>{activity.duration_minutes}</strong></td>
                  <td className="text-center">{activity.distance_km || <span className="text-muted">N/A</span>}</td>
                  <td className="text-center"><span className="badge bg-primary">{activity.points}</span></td>
                  <td><small className="text-muted">{activity.notes || '-'}</small></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Activities;
